# KCS Foundry 新版部署与运行指南

本文只介绍新版原生 KCS 流程，适用于把当前代码移交到另一台电脑、在内网提炼工单，以及后续维护知识库。命令默认从 `cloud-concept-skills` 仓库根目录执行。

## 一、这次修改了什么

新版流程：**选定工单／外部 skill → 原文快照与带行号文本 → OpenKB 原生 KCS 编译 → 结构和来源校验 → 人工复核 → 内部 Git 提交**。

| 部分 | 主要文件／目录 | 新行为 |
| --- | --- | --- |
| 原生 KCS 定义 | `vendor/openkb/openkb/kcs.py`、`schema.py`、`config.py` | 增加 KB 级 `knowledge_profile: kcs`；区分历史案例 `case` 与复用模式 `pattern`；正文采用 Issue、Environment、Resolution、Cause 四字段 |
| OpenKB 编译 | `vendor/openkb/openkb/agent/compiler.py` | 直接生成／更新 KCS 概念，保留 sources、summaries、entities、索引及 wikilinks；更新时保留旧证据，内容或来源变化使旧复核状态失效 |
| 命令与校验 | `vendor/openkb/openkb/cli.py`、`lint.py` | 支持 KCS 初始化、schema 刷新和无模型 `kcs-audit`；通用 profile 保留原有行为 |
| Foundry 接入 | `scripts/extract_kcs.py`、`native_kcs.py`、`validate_kcs.py` | 默认直接编译原生 KCS，保存跨批次来源映射并校验；不再二次调用 `run_skill()` 导出另一套卡片 |
| 诊断技能外挂 | `../huawei-cloud-fcaps-diagnostics/knowledge/`、该技能 `SKILL.md` | 特殊案例和模式放入 `knowledge/ecs-kb/`，排障时按需读取本地文件 |
| 构建与测试 | `vendor/openkb/pyproject.toml`、两层 `tests/` | 提供无上游 Git 元数据时的构建版本回退；增加原生编译、来源追溯及协议边界测试 |

表中未以 `../` 开头的路径相对本 Foundry 目录。独立元技能 `skills/kcs-extractor/` 仍可移交给 Agent 使用；本指南的新版默认流程由编译器直接执行 KCS 规则，不需要 Agent 自动触发元技能。

## 二、先确认运行条件

- Python 3.10+，建议先在目标环境用小包试点。
- 提炼机器能够访问获准的模型接口；安装依赖需使用可用的包源或预先准备的离线包。
- 输入先整理为 UTF-8 的 Markdown、文本、JSON、CSV 或支持的代码文件。PDF、Word、Excel、图片附件需另行转换；脚本不负责识图或附件转换。
- 仅使用获准处理的材料与内部模型。真实运行会把选中材料发送给配置的模型，程序不自动脱敏，也不执行材料里的脚本。

### 模型能力要求

| 使用场景 | 需要的能力 |
| --- | --- |
| 本指南的工单／skill 短文本编译 | 普通 chat completion，接受 `response_format: {type: json_object}`，能按提示输出 JSON；不传工具定义，不要求 function calling |
| OpenKB 自带问答、聊天、技能执行、语义 lint | function calling / tools；`parallel_tool_calls: false` 只是关闭并行，仍然需要工具调用 |
| 诊断技能读取已生成的本地 wiki | 不需要启动 OpenKB 服务，也不需要调用 OpenKB 的模型 |
| 材料整理、`--dry-run` 预演 | 无模型，只需 Python 标准库 |
| 原生结构和来源审计 | 无模型，需要安装 OpenKB 相关依赖 |

**不支持 function calling 不妨碍先试新版编译链路，但仍要验证 JSON 响应模式。** 如果内网接口拒绝 `response_format`，当前版本会报错，需另做兼容适配；不要把关闭工具并行当作修复方案。模型名、网关路径和鉴权方式需由目标部署确认。

## 三、换电脑首次部署

### 1. 移交完整代码

推荐移交整个 `cloud-concept-skills` 仓库，至少保留：

```text
cloud-concept-skills/
└── skills/drafts/
    ├── kcs-foundry/
    │   ├── scripts/
    │   ├── skills/kcs-extractor/
    │   ├── tests/
    │   └── vendor/openkb/          # 必须是本仓库中已改造的版本
    └── huawei-cloud-fcaps-diagnostics/
        ├── SKILL.md
        └── knowledge/
            ├── README.md
            ├── .gitignore
            └── ecs-kb/
                ├── .openkb/config.yaml
                ├── .openkb/hashes.json
                └── wiki/          # 包括 AGENTS.md、index.md、log.md
```

若用 Git 拉取，先确保这批修改及新增文件已提交并同步到目标可访问的仓库。**仅 clone 远端无法获得本机尚未提交的代码。** 内网无法访问远端时，按内部允许的方式移交当前工作目录快照，包含新增文件和隐藏目录。不要只复制诊断技能，也不要用官方 OpenKB 安装包替代这里的修改版。

已有知识时，完整保留 KB 的 wiki、raw、provenance 和 `.openkb/hashes.json`。凭据 `.env` 不随仓库迁移，由目标电脑重新配置。Python 虚拟环境不直接复制，在新电脑重建。

### 2. 创建环境并安装依赖

macOS／Linux 的 Bash 或 Zsh：

```bash
cd /path/to/cloud-concept-skills
python3 --version
python3 -m venv workspaces/kcs-env
source workspaces/kcs-env/bin/activate
python -m pip install --upgrade pip
python -m pip install -e skills/drafts/kcs-foundry/vendor/openkb
openkb --version
```

后续命令的 `python`、`openkb` 均指这个已激活的环境。重新打开终端后，先回到仓库根目录并重新激活。

Windows PowerShell 可用 `py -3 -m venv workspaces/kcs-env` 创建环境，然后执行 `workspaces\kcs-env\Scripts\Activate.ps1`。不能激活时直接使用该目录下的 `python.exe`，例如 `& .\workspaces\kcs-env\Scripts\python.exe -m pip install -e skills/drafts/kcs-foundry/vendor/openkb`。下面的多行命令使用 Bash 的反斜杠续行；在 PowerShell 中合并成一行执行。当前离线回归在 macOS／Python 3.10 环境完成，Windows 需在目标机验证。

#### 内网不能访问包源时

优先使用内部镜像。需要离线包时，在与目标机**操作系统、CPU 架构和 Python 版本一致**的可联网环境，用同一份新版源码准备 wheel：

```bash
python -m pip wheel --wheel-dir /path/to/kcs-wheels ./skills/drafts/kcs-foundry/vendor/openkb
```

该命令构建修改版 OpenKB 及其依赖；完成后移交 `kcs-wheels/` 和上述代码目录。目标机新建并激活虚拟环境，再执行：

```bash
python -m pip install --no-index --find-links /path/to/kcs-wheels openkb
openkb --version
```

离线安装使用构建好的 wheel，不再执行需要临时下载构建依赖的 editable 安装。若某个依赖在目标平台没有可用 wheel，需在相同目标环境完成构建后补齐；不要用其他平台的虚拟环境替代。完整隔离网络的离线安装尚需在目标机验收。

### 3. 配置知识库模型

仓库已提供知识库骨架：

```text
skills/drafts/huawei-cloud-fcaps-diagnostics/knowledge/ecs-kb/
```

直接编辑它的 `.openkb/config.yaml`，无需重新 init，也不要覆盖已有知识：

```yaml
knowledge_profile: kcs
language: zh
model: openai/实际模型名
pageindex_threshold: 20
```

`openai/` 是 OpenAI 兼容接口的 LiteLLM provider 前缀，替换实际模型名；其他协议按部署调整。模型必须明确配置在这个 KB 的文件中；初始 `model: null` 会阻止真实导入，避免误用全局默认模型。

在同一个 `ecs-kb/` 根目录创建 `.env`：

```dotenv
LLM_API_KEY=目标环境的实际凭据
OPENAI_API_BASE=https://内部网关地址/v1
```

按网关实际要求填写，地址示例不代表所有网关都使用 `/v1`。不要把密钥放到命令行或 Git。配置模型文件后，提交前也检查模型标识是否属于允许同步的信息。

### 4. 先做无模型检查

```bash
python -m unittest discover -s skills/drafts/kcs-foundry/tests -v
python skills/drafts/kcs-foundry/scripts/validate_kcs.py \
  --kb skills/drafts/huawei-cloud-fcaps-diagnostics/knowledge/ecs-kb
```

预期测试通过；初始空 KB 的校验可返回 `valid: true`，同时提醒没有 KCS 卡片。这只证明骨架通过机械检查，**不代表模型连接正常或萃取成功**。模型连接与输出能力由下面的小批真实试点验证。

## 四、首次小批运行

### 1. 准备工单或外部 skill

建议先用 1～3 份同类工单，或一个明确范围的外部 skill。工单导出应保留症状、环境／版本、处理过程、实际操作、恢复反馈及原因确认；缺少的信息允许未知，不要补造。

工单示例：

```bash
python skills/drafts/kcs-foundry/scripts/prepare_materials.py \
  --source /path/to/approved-tickets \
  --kind ticket \
  --source-name internal-ticket-pilot \
  --output /path/to/material-pack-01
```

外部 skill 示例（二选一；若两者都跑，使用不同包目录）：

```bash
python skills/drafts/kcs-foundry/scripts/prepare_materials.py \
  --source /path/to/approved-skill \
  --kind skill \
  --source-name vendor/repository \
  --revision source-commit \
  --include SKILL.md \
  --include 'references/*.md' \
  --output /path/to/skill-pack-01
```

`--revision` 已知时填写实际版本，否则省略。`--include` 可重复，按相对输入根目录的路径匹配；不填时采集支持的非隐藏文本文件，包含目录下的支持文件。默认最多 200 文件、每文件 1 MiB，超限先缩小范围，也可显式设置 `--max-files`、`--max-file-bytes`。

原文包必须放在输入目录和知识库之外，已有包不覆盖。检查命令输出和 `manifest.json` 的 `skipped`，确认附件、不支持格式和排除项是否需要补充转换。

```text
material-pack-01/
├── manifest.json       # 来源别名、版本、原路径及两种哈希
├── sources/            # 逐字节原文快照，保留目录关系
└── documents/          # 带原行号的 Markdown 导入文本
```

隐藏文件、常见依赖目录不采集；选中范围内的符号链接拒绝跟随。原始材料包是独立核对依据，运行中不要改写它。

### 2. 预演

以下使用上面的工单包；若使用 skill 包，替换 `--materials`：

```bash
python skills/drafts/kcs-foundry/scripts/extract_kcs.py \
  --materials /path/to/material-pack-01 \
  --kb skills/drafts/huawei-cloud-fcaps-diagnostics/knowledge/ecs-kb \
  --run-id ssh-pilot-01 \
  --scenario 'SSH 建连超时试点' \
  --dry-run
```

预演检查材料哈希、路径和任务 ID，打印调用计划；不写文件、不调用模型。检查 `mode`、材料列表、目标 KB 和 run-id 是否符合预期。

**`--scenario` 只是本次任务标签，不是筛选器。** 导入范围由材料包决定，只想提炼 SSH 故障，就先选取对应工单／文件。默认保留来源平台；平台适配需有额外来源证据，接入程序只保留来源环境。

### 3. 正式编译

使用同一条命令，去掉 `--dry-run`：

```bash
python skills/drafts/kcs-foundry/scripts/extract_kcs.py \
  --materials /path/to/material-pack-01 \
  --kb skills/drafts/huawei-cloud-fcaps-diagnostics/knowledge/ecs-kb \
  --run-id ssh-pilot-01 \
  --scenario 'SSH 建连超时试点'
```

此步骤会实际请求配置的模型。程序逐份导入文本，生成摘要、创建／更新 KCS 概念和知识关联，记录原文来源，再校验全库。预期输出 `Run phase: completed`；其他状态或非零退出都需检查，不能仅凭 wiki 文件已生成判断成功。

## 五、产物在哪里，如何复核

所有 KB 路径均在诊断技能内：

```text
huawei-cloud-fcaps-diagnostics/knowledge/ecs-kb/
├── .openkb/
│   ├── config.yaml、hashes.json
│   └── kcs-foundry/ssh-pilot-01/   # 计划、逐文档结果及 state.json
├── raw/kcs-inputs/ssh-pilot-01/    # 清单、原文及导入文本的持久快照
├── provenance/batches/
│   └── ssh-pilot-01.json          # 原文→导入文本→wiki来源的哈希映射
├── wiki/
│   ├── AGENTS.md                 # KCS schema
│   ├── index.md、log.md           # 索引和维护日志
│   ├── sources/                  # 编译器读取的来源文本
│   ├── summaries/                # 文档摘要与来源入口
│   ├── concepts/                 # case／pattern，四字段 KCS 卡片
│   └── entities/                 # 产品、组件等实体
└── output/kcs/ssh-pilot-01/
    ├── extraction-report.md      # 本次变化节点与检查说明
    └── validation.json           # 程序生成的校验结果
```

**可检索的知识正文在 `wiki/concepts/`，运行报告在 `output/`。** 案例与模式通过 wikilinks 关联；不需要再复制一套案例到 `references/recipes/kcs/`。某份材料可能没有可复用排障知识，零卡片提示需人工检查材料与模型输出。

### 1. 独立校验

```bash
python skills/drafts/kcs-foundry/scripts/validate_kcs.py \
  --kb skills/drafts/huawei-cloud-fcaps-diagnostics/knowledge/ecs-kb
```

此命令不调用模型，跨批次检查四字段、证据结构、原文快照、来源哈希、内容哈希、索引和 wiki 链接；非零退出或 `valid: false` 表示未通过。

仅查 OpenKB wiki 内部绑定时，也可运行：

```bash
openkb --kb-dir skills/drafts/huawei-cloud-fcaps-diagnostics/knowledge/ecs-kb kcs-audit
```

后者不包含 Foundry 原始材料的跨批次追溯检查。模型不支持工具调用时，用上述结构审计；OpenKB 的语义 lint 还需要工具调用能力。

### 来源字段的模型兼容

生成阶段模型优先使用 `evidence.source_ref: S0`、`S1` 等短编号。程序逐卡片提供映射：`S0` 是当前文档，其他编号指向该卡片已有来源；模型按真实支持关系选择，程序在落盘前换成标准 `evidence.source: summaries/xxx.md`。短编号只在本次生成中有效，不作为持久来源身份。

兼容既有的标准路径输出，也接受 `source: S0`。仅有一个候选来源时允许省略来源字段并由程序补齐；多个来源时缺失、未知编号或相互冲突的字段仍会失败，不自动猜测或把所有证据绑定当前工单。此适配减少路径格式错误，不证明所选来源语义正确，仍需人工核对。更新源码后需重启提炼进程；原生流程无需重新安装或修改独立元技能，已有卡片的持久格式不变。

### 2. 人工核对

优先阅读 `wiki/index.md` 和本次报告中的变化卡片，再对照原文与证据检查：

- 工单实际发生的事与来源中的操作建议是否区分清楚。
- 环境、版本、处理分支和恢复验证是否保留，失败尝试是否被误写为有效方案。
- Cause 是否确有来源确认，未知原因是否仍写为未知。
- 多份工单的共同模式是否有证据支撑，矛盾或平台差异是否明确说明。
- 原文、正文及追溯信息是否适合当前内部仓库的权限范围。

`valid: true` 只表示机械检查通过；报告中的来源语义复核和运行验证仍为 `not_run`。新生成／有变化的卡片默认为 `draft`，不自动提升为已验证。已有的 `reviewed`／`validated` 状态仅在内容、来源及其 `validation_hash` 仍匹配时保留；不要只手改状态冒充复核完成。

### 3. 提交到内部 Git

复核后将技能与知识库作为一个版本提交，至少保留 wiki、raw、provenance、`.openkb/config.yaml` 及 `.openkb/hashes.json`。原文包可按内部材料保留要求单独归档，KB 内持久快照用于后续追溯。

在仓库根目录检查：

```bash
git status --short
git diff -- skills/drafts/huawei-cloud-fcaps-diagnostics
git add skills/drafts/huawei-cloud-fcaps-diagnostics
git diff --cached --stat
```

确认内容和内部权限后，再按团队流程 commit／push。密钥 `.env`、锁、缓存、临时状态和 `output/` 已有忽略规则，不应提交。本指南展示命令，Foundry 本身不会自动执行 Git 操作；改造程序本身需随首次代码移交一并提交。

## 六、后续如何使用与维护

### 排障电脑只消费已有知识

如果只需要运行诊断技能并读取现有知识，移交完整的诊断技能目录和其中的知识库即可。遵循 `knowledge/README.md` 按“索引 → 少量相关 case／pattern → 必要的来源”读取，无需安装 Foundry 的 Python 依赖或启动 OpenKB。运行诊断技能本身所需的 Agent／云工具按技能原有部署要求准备。

历史案例提供线索，不证明当前故障原因。一次排障不会自动回写 OpenKB；有值得沉淀的新工单后，再显式运行提炼任务。

### 提炼电脑增量导入新材料

继续使用同一 KB，重复“准备新包 → 预演 → 编译 → 校验 → 人工复核 → Git 提交”。不必每次安装依赖，也不重新 init。相同内容可跳过，新增材料会参与相关概念更新。

每次正式运行使用新的 `--run-id`，如 `ssh-pilot-02`；材料包也使用新目录。只在新增／修订材料或明确需要重编译时运行，不需要为读取知识定时运行 OpenKB。

## 七、常见问题与失败处理

| 现象 | 检查与处理 |
| --- | --- |
| 提示 OpenKB dependencies unavailable | 确认已激活正确虚拟环境，并安装仓库内修改版 OpenKB；不要混用系统 Python |
| 提示 Set an explicit KB-local model | 检查目标 KB 的 `.openkb/config.yaml`；`model` 不能为空或仅存在于全局配置 |
| 请求被网关拒绝／鉴权失败 | 在内部检查该 KB 的 `.env`、模型名、接口路径和凭据；不要向公开报告粘贴密钥或工单请求正文 |
| 接口不认识 `response_format` | 内网接口的 JSON 模式需适配，当前版本不能靠关闭 function calling 解决 |
| 只有 ask/chat 或技能执行失败 | 核实模型工具调用能力；它们不属于本指南默认的原生编译链路 |
| run-id 已存在 | 不覆盖旧任务；检查状态后选新 ID。`--dry-run` 不占用 ID |
| source hash／snapshot／provenance 校验失败 | 检查来源文件是否被改动、漏拷贝或缺少跨批次记录；不要删除哈希来让检查通过 |
| 生成失败或校验失败 | 查看 `.openkb/kcs-foundry/<run-id>/state.json`、运行终端及已有报告；保留现场，修复原因后用新 ID 重跑 |
| schema/profile 不一致 | 确认移交的是新版 KB 骨架与源码；已有通用 KB 的迁移需单独备份、刷新 schema 并重编译，不能只换配置标识 |

**单文档编译失败可回滚该文档；整批不是一个事务。** 后面某份失败时，前面成功的知识和来源映射仍会保留。程序不自动重试；运行状态只记录异常类型，避免将可能含请求资料的异常正文写入报告。重跑前检查已完成范围，相同内容可由 OpenKB 去重。

## 八、验证范围

此前改造在独立环境完成安装验证和无真实模型测试；清理旧导出流程后的测试以当前测试集为准。覆盖原生编译、更新合并、校验状态失效、wiki 关系、跨批次来源、输入篡改及调用协议边界。测试使用替代模型／后端；实际内网网关、真实工单提炼质量、Windows 及完全离线安装尚需目标环境试点验收。

## 接口收敛说明

Foundry 只维护“材料 → 原生 KCS wiki → 审计”一条链路，已删除旧 export 分支。运行 extract_kcs.py 不再传 `--mode`、`--max-turns` 或 `--target-platform`；校验只使用 `validate_kcs.py --kb`，不再支持 `--output/--materials` 的独立导出校验。现有 wiki、来源映射和持久原文不迁移、不删除。

独立元技能仍可手动移交内部 Agent，但不再由 Foundry 安装或执行。OpenKB 自带的 ask/chat、skill runner 和语义 lint 仍是其通用能力，未在这次清理中删除。

KCS profile 默认只在显式设置了 `knowledge_profile: kcs` 的知识库生效；通用 profile 不变。已有通用 KB 需备份、显式刷新 schema 并重新编译，不能仅换配置标识。KCS 证据与来源指纹由程序绑定，新内容为 draft；移除来源会使旧复核失效，需重新整理与核对。结构审计不是语义或运行验证。
