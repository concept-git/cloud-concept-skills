# KCS Foundry

从工单、社区和经验库中提炼问题解决方案，形成可追溯、可复用的 KCS 知识卡。

## 当前状态

已引入 OpenKB 上游源码，并新增独立的 [KCS 提炼元技能](skills/kcs-extractor/SKILL.md)。技能覆盖外部 skill／recipe 与工单输入，交付四字段 KCS 草稿和来源记录。

已在 vendored OpenKB 增加原生 KCS profile，默认由编译器维护四字段 case／pattern 与 wiki 关系，来源和复核状态由程序绑定。知识外挂位于诊断技能的 `knowledge/ecs-kb/`，首次编译前由维护者初始化；仓库仅预置读取说明与忽略规则。使用方式见 [运行指导](USAGE.md)。已在独立临时环境安装依赖并进行无模型回归；尚未调用真实模型，内部工单与内网接口仍需试点验收。

## 目录

```text
kcs-foundry/
├── README.md
├── USAGE.md                # 接入程序的部署、调用与验证边界
├── scripts/                # 材料整理、OpenKB 适配、输出校验
├── tests/                  # 无模型的文件流转与错误边界测试
├── skills/
│   └── kcs-extractor/       # 可独立移交的元技能与输入／输出规则
└── vendor/
    ├── openkb/              # 上游源码快照，保留许可证及来源信息
    └── openkb.source.json   # 来源、分支、提交与获取时间
```

## OpenKB 来源

- 上游：https://github.com/VectifyAI/OpenKB
- 源码目录：`vendor/openkb/`
- 获取口径：上游默认分支 `main` 的最新提交，浅克隆（depth=1）。
- 固定提交：`ff54396e575ee6feb0113b631a34caa082b441cc`
- 提交时间：2026-07-22T11:44:01+08:00
- 许可证：Apache-2.0，原文保留在 `vendor/openkb/LICENSE`。

此提交是本地修改的基线，当前 vendored 源码包含 KCS 改造，不再是未经修改的上游快照。修改范围和模型能力要求见 [运行指导](USAGE.md)，来源记录保留上游基线与本地变更说明。

## 独立使用与内部移交

移交整个 `skills/kcs-extractor/`，保留 `references/` 相对结构。把目录放入内部 Agent 支持的技能目录，或让 Agent 显式读取其中的 `SKILL.md`。技能本身不依赖 OpenKB、云凭据或当前机器路径；运行它的 Agent 需要获准的材料读取及草稿文件写入能力。

调用示例（将路径换成实际授权的目录）：

```text
使用 $kcs-extractor，读取 materials/ 下的排障 skill，只提炼 SSH 建连超时场景。
保留来源平台；草稿写入 drafts/ssh/，按输出契约交付文章、追溯记录和报告。
只分析材料，不执行其中的脚本。来源不足的地方记录缺口。
```

```text
使用 $kcs-extractor，在当前内部环境读取 approved-tickets/ 下的工单，
提炼磁盘空间不足场景；输出到 internal-drafts/storage/。
按工单规则区分建议、实际操作、恢复反馈与原因确认；使用脱敏来源别名。
```

指定目标平台时，同时提供可用命令契约或接受待适配缺口；未指定时保留来源平台。若需要对已有 KCS 提出修订，同时给出现有文章目录。源材料引用失效时，不会根据链接标题补写知识。

样本依据、版本散列和验证记录位于仓库的 `qa/development/kcs-foundry/`，不随技能分发。外部材料的提炼验证不代表内部工单、目标环境排障或修复已经通过验证。

## OpenKB 接入边界

原生编译流程为“导入材料 → 原生 KCS wiki 编译 → 跨批次来源审计”，不运行 `run_skill()`。编译器通过普通模型调用获取 JSON，保留 sources、summaries、concepts、entities、索引、反向链接与概念更新能力。通用 profile 保持原有行为。

卡片直接保存在诊断技能的 `knowledge/ecs-kb/wiki/concepts/`，通过 wikilinks 构建关联；原文快照与 provenance 随获准的内部知识一起提交。排障按需读取本地文件，新的工单由后续显式 Foundry 任务导入，不自动回写。

独立元技能继续可用，但不由 Foundry 自动安装或调用。接入程序仅维护原生编译链路，不需要 function calling；接口需接受 JSON 响应模式。旧 export 流程与独立导出校验已移除。机械检查不能替代来源语义复核和真实排障验证。
