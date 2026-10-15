# huaweicloud-ecs-troubleshooting 结构设计说明

**状态：开发阶段（结构设计稿，尚不可用）。** 本目录包含 15 个空的技能骨架文件及设计说明，尚未实现排障正文或采集脚本。空 `SKILL.md` 不具备可安装技能所需的 frontmatter 和指令。

建议名称为 `huaweicloud-ecs-troubleshooting`。第一版以 **华为云 ECS Linux 实例及其关联服务的故障定位** 为范围；Windows 专用诊断、完整安全取证和数据库内部诊断留给后续独立能力。这里的“其它云服务”优先指与 ECS 关联的华为云服务；跨云复用方式见后文。

开发稿独立放在 `development/huaweicloud-ecs-troubleshooting/`，与可安装的 `skills/en/`、`skills/cn/` 分开。完成实现与验证后，按仓库规范建立英文及中文成对技能，再登记正式技能目录。本开发稿未加入可安装技能清单。

## 1. 原技能：已核实的结构与组织思路

参考：[ClawHub 发布页及 Files 清单](https://clawhub.ai/sdk-team/skills/alibabacloud-ecs-linux-os-troubleshooting#files)，页面显示版本 **v0.0.1**，核查日期 **2026-10-13**。文件名以该发布页为准，不能把官方仓库的最新分支等同于这个发布版本。

原技能分为入口、现象路由、场景流程和组件参考四部分。先确定现象与故障边界，再获取诊断证据、深入 GuestOS，最后输出报告。它保留了按需读取组件资料的能力，但路由存在两张表，很多细分现象各占一个文件。

原技能的完整参考目录如下，仅在本文保留结构对照：

```text
alibabacloud-ecs-linux-os-troubleshooting/
├── SKILL.md
├── skill-card.md
└── references/
    ├── aliyun-cli-cheatsheet.md
    ├── clock-abnormal.md
    ├── cpu-high.md
    ├── create-diagnostic-report.md
    ├── degraded-mode.md
    ├── diagnosis-report-template.md
    ├── disk-attach-detach-failed.md
    ├── disk-expand-failed.md
    ├── disk-fs-damaged.md
    ├── disk-iops-high.md
    ├── disk-perf-unexpected.md
    ├── guestos-not-running.md
    ├── instance-stuck-starting.md
    ├── internal-network-failed.md
    ├── load-high.md
    ├── memory-oom.md
    ├── network-latency-high.md
    ├── network-packet-loss.md
    ├── network-perf-unexpected.md
    ├── password-reset-failed.md
    ├── phenomenon-domain.md
    ├── ram-policies.md
    ├── retransmit-high.md
    ├── secondary-eni-unavailable.md
    ├── ssh-keypair-not-applied.md
    ├── ssh-login-failed.md
    ├── symptom-to-domain.md
    ├── system-crash.md
    ├── system-hang.md
    ├── userdata-failed.md
    ├── vnc-login-failed.md
    └── utils/
        ├── cloudmonitor-metrics.md
        ├── guestos-boot.md
        ├── guestos-cloud-init.md
        ├── guestos-console-log.md
        ├── guestos-disk-fs.md
        ├── guestos-dns.md
        ├── guestos-firewall.md
        ├── guestos-grub.md
        ├── guestos-hotplug-disk.md
        ├── guestos-kernel-initrd.md
        ├── guestos-malware-mining.md
        ├── guestos-net-sysctl.md
        ├── guestos-nic-route.md
        ├── guestos-pam.md
        ├── guestos-pe-prep.md
        ├── guestos-shell.md
        ├── guestos-sshd.md
        ├── guestos-systemd.md
        ├── guestos-time.md
        ├── guestos-tty-getty.md
        └── tracepoint-perf-tools.md
```

合计：根目录 2 个文件、`references/` 直接下属 31 个文件、`utils/` 21 个文件，全部为 Markdown。`utils/` 的内容实际是参考文档，不是可执行工具。

## 2. 推荐结构：一个入口、八类现象、共享支撑

```text
huaweicloud-ecs-troubleshooting/
├── SKILL.md
└── references/
    ├── triage.md
    ├── cloud-context.md
    ├── cloud-access.md
    ├── observability.md
    ├── symptom-boot.md
    ├── symptom-login.md
    ├── symptom-network.md
    ├── symptom-storage.md
    ├── symptom-performance.md
    ├── symptom-crash.md
    ├── symptom-configuration.md
    ├── symptom-security.md
    ├── recovery.md
    └── report.md
```

上述 15 个空文件直接位于本开发目录下；同目录的 `README.md` 用于说明开发状态，本文用于说明结构设计，均不属于未来技能运行载荷。

核心选择：

- **按用户现象找入口。** “进不去、连不通、变慢、盘异常”比内核组件名更容易匹配；`triage.md` 是唯一的现象路由表。
- **按故障边界深入。** 同一场景同时考虑云平台资源、实例操作系统、应用与依赖、访问客户端，不预先把故障归到 GuestOS。
- **按需读取共享资料。** 云资源关系、访问权限、观测证据和恢复策略各有一处定义，场景文档通过明确条件引用。
- **合并同一路径的小文件。** CPU、内存、负载合为性能；丢包、延迟、重传合为网络；账号、密钥、sshd 合为登录。
- **保持浅目录。** `references/` 扁平存放，`symptom-` 前缀直接辨识场景文档，也符合当前仓库写作约定。

15 个文件是起点，不是永久上限。若网络或存储资料出现大量只适用于少数分支的细节，再抽出有明确读取条件的参考；不要把减少文件数变成巨大单文件。

## 3. 每个文件的目的、核心概念与简要流程

下面描述未来应写入的内容与职责；对应骨架文件目前均为空。

| 文件 | 解决的目的 / 何时读取 | 核心概念 | 简要流程与完成条件 |
| --- | --- | --- | --- |
| `SKILL.md` | 技能入口：界定范围、约束和整体路径 | 目标实例、现象、证据、诊断与恢复边界 | 锁定目标 → 进入 triage → 选场景 → 按需取证 → 输出报告；每个诊断都有证据或明确的缺口 |
| `references/triage.md` | 把自然语言描述分配到八类场景；所有事件先读取 | 时间窗、影响范围、主现象、近期变更、竞争假设 | 整理已有事实 → 补齐会改变路径的缺失信息 → 选主场景并记录次要现象；有下一项可执行检查即完成分诊 |
| `references/cloud-context.md` | 判断资源身份与关联关系；查询目标、跨服务故障时读取 | region、project、实例、可用区、资源拓扑、控制面与业务健康 | 确认 ECS 身份与状态 → 识别关联网络/磁盘/业务资源 → 对齐故障时间；输出只含相关资源的关系清单 |
| `references/cloud-access.md` | 确定能取得哪些证据；首次云查询、权限失败或实例不可达时读取 | IAM 权限、KooCLI/API、SSH、VNC、主机内执行、通道能力 | 验证身份与作用域 → 区分无权限/无资源/通道不可用 → 选择已有通道或用户提供材料；记录可用能力及限制 |
| `references/observability.md` | 把指标、日志、操作事件组织成一条时间线；需要历史证据或诊断能力时读取 | CES 指标、LTS 日志、CTS 操作事件、采集覆盖、证据时间 | 确认事件前已启用的数据源 → 查询同一窗口 → 标记异常与缺口 → 回到场景验证假设；证据绑定资源、时间和来源 |
| `references/symptom-boot.md` | 实例状态异常或系统无法启动 | ECS 生命周期、GuestOS 引导、GRUB/initrd、systemd、系统盘、IMS 镜像 | 比较实例状态与启动画面/可用日志 → 定位停在平台还是系统阶段 → 关联镜像、驱动、挂载配置；定位阶段或给出下一项证据 |
| `references/symptom-login.md` | SSH/VNC 登录失败、凭证或密码重置不生效 | 连接超时、连接拒绝、认证失败、sshd、PAM、账号、密钥、终端 | 按原始错误分支 → 检查访问通道 → 检查认证与服务 → 必要时转网络/启动；明确故障发生在连接还是认证阶段 |
| `references/symptom-network.md` | 内外网不通、端口不通、延迟/丢包、DNS 或 ELB 访问异常 | 源/目的/端口/方向、VPC 路由、安全组/ACL、EIP/NAT、DNS、ELB、主机网络 | 画实际访问路径 → 比较域名/IP、直连/经 ELB、内网/公网 → 查规则与主机监听 → 检查性能；定位失败段或界定证据范围 |
| `references/symptom-storage.md` | 磁盘不可见、挂载/扩容失败、容量满、文件系统或共享存储异常 | EVS 云容量、块设备、分区/LVM、文件系统、inode、IOPS/吞吐、SFS | 对齐云盘和设备身份 → 比较各层容量与状态 → 检查挂载/错误 → 关联性能；确定问题层和数据保护需求 |
| `references/symptom-performance.md` | CPU/内存/负载高、OOM、磁盘或带宽瓶颈、业务变慢 | 基线、峰值、饱和度、进程归因、资源规格、业务请求 | 对比故障前后指标 → 找资源瓶颈 → 关联进程/业务与规格限制 → 验证因果；输出瓶颈证据及待验证因素 |
| `references/symptom-crash.md` | 崩溃、卡死、非预期重启 | panic、lockup、OOM、kdump、重启时间线、平台操作 | 区分人工/平台操作与系统异常 → 对齐日志和事件 → 判断是否有转储 → 保留证据并定位；明确重启来源或证据缺口 |
| `references/symptom-configuration.md` | 用户数据、镜像初始化、网卡热插拔、配置及时间同步不生效 | 期望/实际状态、cloud-init、配置持久化、热插拔、NTP/chrony | 比较期望与实际 → 追踪下发/加载/持久化路径 → 检查适用性与日志；解释在哪一阶段未生效 |
| `references/symptom-security.md` | 异常高负载伴随未知进程、疑似挖矿或入侵迹象 | 迹象与确认、进程/连接/持久化、HSS 告警、证据保全 | 关联已有告警 → 采集最少必要现场 → 判断是否进入安全响应 → 交接；输出迹象和不确定性，不以高 CPU 单独判定入侵 |
| `references/recovery.md` | 需要提出恢复方案、在线通道不可用且涉及离线处理时读取 | 诊断/变更、CBR/快照、恢复点、离线挂盘、回滚、验证 | 保全证据 → 比较恢复选择 → 说明影响与前置条件 → 有相应授权再执行 → 验证/回滚；形成具体可审查方案或验证恢复结果 |
| `references/report.md` | 所有路径收尾；工单或跨团队交接时复用 | 事实、假设、结论、可信程度、排除项、下一步 | 汇总现象/边界/时间线 → 引用证据 → 区分确认与待验证 → 给建议和验证标准；受限诊断同样输出已查范围与缺口 |

## 4. 需要掌握的少量核心概念

**现象与根因分开。** “无法 SSH”可能涉及客户端、网络、系统未启动或认证；现象只决定先查哪里。允许主场景带次要现象，新增证据可以改变路径。

**资源状态与业务健康分开。** 查询到 ECS 处于运行状态后，仍需验证系统和业务是否工作；ELB 后端异常也只是定位入口。网络与系统检查应形成相互验证的证据链。[华为云 ECS 登录排查](https://support.huaweicloud.com/intl/zh-cn/ecs_faq/zh-cn_topic_0105127983.html)、[ELB 健康检查异常诊断](https://support.huaweicloud.com/intl/zh-cn/usermanual-elb/elb_ug_zd_0002.html)。

**资源关联与因果分开。** ECS 绑定了 EIP 或 EVS，并不能说明它们是故障原因。资源图帮助选择检查对象；时间线、路径对照和异常证据才支持归因。

**缺少数据与正常分开。** CES 基础监控与操作系统监控的采集能力不同；后者依赖 Agent。LTS 主机日志接入也需要相应采集配置。设计要求记录覆盖和权限，空结果不能直接解释为健康。[CES 主机监控简介](https://support.huaweicloud.com/intl/zh-cn/usermanual-ces/zh-cn_topic_0078721772.html)、[LTS 主机日志采集](https://support.huaweicloud.com/intl/zh-cn/usermanual-lts/lts_02_0014.html)。

**诊断与恢复分开。** 故障定位可以产出恢复建议；停止实例、改配置、离线挂盘或恢复备份则是另外的动作。先给出目标、证据、具体变更和验证方法，授权覆盖该动作后再执行。

## 5. 结合其它华为云服务的边界

以下是推荐的集成职责，不代表这些服务在每个账户、区域、镜像和权限组合中均可用。具体 API、CLI 参数、诊断能力及服务限制在实现时查验，骨架阶段不编造命令。

| 服务 / 能力 | 在 ECS 排障中的作用 | 进入文件 | 深入到什么程度 |
| --- | --- | --- | --- |
| ECS、IMS | 实例状态、规格、镜像及启动背景 | cloud-context、boot、configuration | 核实目标资源与兼容性，提供引导阶段线索 |
| VPC、安全组、网络 ACL、EIP、NAT、DNS、ELB | 入站、出站、内网和负载均衡访问路径 | network | 检查实际经过的资源与失败段；跨网场景按需加入 VPN/DC/ER |
| EVS、SFS | 块存储与共享文件存储的状态、容量和访问 | storage | 分开云盘、主机设备和文件系统；SFS 连接问题交叉引用 network |
| CES | 资源趋势、故障窗口与性能线索 | observability、performance | 区分基础与 Agent 指标，核实故障时是否有数据 |
| LTS、CTS | 系统/应用日志与云资源操作时间线 | observability、crash、configuration | 只使用已经采集且有权访问的记录，明确保留范围 |
| IAM、KooCLI/API | 查询身份、项目作用域、权限和云侧访问 | cloud-access | 选择当前任务需要的权限，不把全管理员权限作为默认 |
| CBR、快照及临时 ECS | 恢复点与离线处理条件 | recovery | 核实备份、可用区、磁盘关联及回滚条件后形成方案 |
| HSS | 疑似入侵时的告警线索 | security | 关联告警并交接安全响应，完整取证另立能力 |
| CCE、RDS 等业务依赖 | 识别 ECS 是否是节点或客户端、依赖是否异常 | cloud-context、network、report | 确定故障边界后交接服务专项诊断 |

网络路径以[华为云 VPC 使用指南](https://support.huaweicloud.com/intl/zh-cn/helppanel-vpc/vpc_help_0001.html)为基础；EVS 云端扩容后仍需处理主机分区与文件系统，参见[Linux 扩容说明](https://support.huaweicloud.com/usermanual-evs/evs_01_0109.html)。ELB、CES 和 CBR 与 ECS 故障恢复的关联见[华为云 ECS 常见故障模式](https://support.huaweicloud.com/intl/zh-cn/usermanual-architecture/architecture_02_0126.html)。离线系统盘修复路径有官方示例，但实现前必须按当前约束核实，见[错误系统配置恢复说明](https://support.huaweicloud.com/trouble-ecs/ecs_trouble_0375.html)。

CTS 操作记录必须区分控制台可查询窗口与已配置的历史转储，参见[查看云审计事件](https://support.huaweicloud.com/usermanual-cts/cts_02_0005.html)。华为云已有[智能诊断 ECS](https://support.huaweicloud.com/usermanual-ecs/ecs_03_2517.html)能力，可作为观测层的候选证据通道；实现时核实入口和调用条件，不假设它与阿里云诊断 API 一一对应。

跨云复用建议：保留“现象 → 责任层 → 证据 → 报告”的方法，以及 Linux 组件分析；替换资源身份、权限、API、观测与恢复能力。不要把阿里云 RAM、Cloud Assistant、DMS 诊断项或 CLI 参数直接改名后带入华为云。未来如要支持阿里云、AWS、Azure 等，再基于实际实现拆出云厂商适配；本次不增加多云空目录。

## 6. 简要运行流程与读取路径

```text
用户描述 + 已有材料
  → SKILL：确认目标与范围
  → triage：确定主现象和时间窗
  → cloud-context / cloud-access：按需确认资源与可用通道
  → 一个 symptom 文件：选择首个可验证假设
  → observability：按需补充历史指标、日志与操作事件
  → 用新证据验证、排除或切换假设
  → recovery：需要恢复或离线方案时读取
  → report：确认结论，或说明缺口及下一步
```

场景文档应统一包含：适用现象、故障边界、最少证据、分支判断、恢复引用、验证标准与交接条件。通用权限和证据规则用链接引用；sshd、GRUB、PAM 等组件解释与对应场景放在一起。

例如“SSH 超时”先读登录场景，随后根据证据转网络或启动；“扩容后容量没变”进入存储，对照云容量、块设备、分区与文件系统；“凌晨突然重启”进入崩溃场景，再读取观测资料对齐操作事件和系统日志。每次只加载当前分支涉及的资料。

实例不可达或已释放时仍沿用场景流程：记录丢失的实时通道，用已有日志、指标、操作记录或用户材料缩小范围。只有取证需要离线挂盘等恢复动作时才进入 `recovery.md`。这样不再增加一个平行的“降级模式”工作流。

## 7. 从原结构迁移到新结构

| 原文件组 | 新归属 | 合并理由 |
| --- | --- | --- |
| SKILL.md、skill-card.md | SKILL.md；市场卡片需要时由入口生成 | 运行时保留一个入口，减少重复维护 |
| symptom-to-domain、phenomenon-domain | triage.md | 现象描述、分支及入口集中在一张路由表 |
| aliyun-cli-cheatsheet、ram-policies | cloud-access.md | 重新建立华为云访问与权限契约 |
| create-diagnostic-report、cloudmonitor-metrics | observability.md | 统一证据职责；华为云具体诊断能力重新核验 |
| degraded-mode | cloud-access、各场景、report | 通道限制随场景处理，证据缺口随报告输出 |
| instance-stuck-starting、guestos-not-running；boot/grub/kernel-initrd/systemd | symptom-boot.md | 按启动阶段组织组件与证据 |
| ssh/vnc/password/keypair；sshd/pam/shell/tty-getty | symptom-login.md | 按连接、认证及终端阶段组织 |
| internal-network/latency/packet-loss/retransmit/network-perf；dns/firewall/net-sysctl/nic-route | symptom-network.md | 按访问路径、失败段及性能分支组织 |
| disk-attach/expand/fs-damaged；disk-fs/hotplug-disk | symptom-storage.md | 按云盘到文件系统的层次组织 |
| cpu-high/load-high/memory-oom/disk-iops-high/disk-perf；tracepoint-perf-tools | symptom-performance.md | 按瓶颈与归因组织；存储错误仍归 storage |
| system-crash/system-hang；console-log | symptom-crash.md；启动场景共享必要的控制台取证说明 | 按异常类型及时间线组织；重复取证段落实质增长时再抽取 |
| clock-abnormal/userdata-failed/secondary-eni-unavailable；cloud-init/time | symptom-configuration.md | 统一为期望配置未生效；实际连通性转 network |
| guestos-malware-mining | symptom-security.md | 保留初筛与证据交接边界 |
| guestos-pe-prep | recovery.md | 重新核验华为云离线流程和回滚条件 |
| diagnosis-report-template | report.md | 一个固定输出契约服务全部场景 |

新增 `cloud-context.md` 是本次结构调整的关键：原技能聚焦 Linux GuestOS，新技能需要先理解实例与关联云服务的关系，才能判断故障属于哪一层。

## 8. 后续实现边界

优先实现分诊、云身份/访问、登录、网络和报告，再补齐其它场景。场景的接口与完成标准先稳定，反复使用且需要可靠输出的采集逻辑出现后，再考虑 `scripts/`。

当前阶段仅保留结构与开发说明，尚未创建脚本、执行模板、UI 元数据、QA 或发布配置。后续成为正式技能时再填写 frontmatter、建立全部引用、核实 CLI/API、补充必要验证并检查真实请求下的路由行为。此结构稿的验收只包括目录与说明的一致性，不代表排障能力已经实现。
