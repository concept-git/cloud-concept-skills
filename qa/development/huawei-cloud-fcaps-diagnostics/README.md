# 验收与复核

运行文档是命令权威源；QA 不保存第二套运行契约。验证摘要由实际证据生成。PASS 只表示所列范围通过，不代表 Windows 或有条件采集已实测。

| 检查 | 通过条件 |
| --- | --- |
| hcloud 迁移 | 原 33 服务、1,282 操作版本完整且唯一；仅路径及导航变化 |
| 平台迁移 | 58 Linux、27 Windows、15 可选 Kubernetes 模式均有迁移决策及验证状态 |
| 契约 | 四列；具体模式、直接观测、必要输入、适用与影响约束 |
| 路由 | FCAPS→环境→命令；已知 ID 直接读取；工具入口不复制契约 |
| 依赖 | 云资源、OS 对象和集群对象类型分开；未证实的映射保持未解析 |
| 真实执行 | Linux 47 个可用查询、Kubernetes 15 个本地查询及 10 项云资源绑定通过 |
| 诚实范围 | Windows 27 项受阻；Linux 6 项缺依赖，5 项条件扫描／采集不自动执行；空记录与错误分开 |
| 证据绑定 | 从最终 Markdown 取命令；行摘要匹配；云复核绑定运行文档摘要 |
| 防漂移 | 9 个云错误和 5 个平台错误注入被拒绝；另有 6 个设备映射拒绝用例和 7 个 CLI 响应解析用例；仅操作临时副本 |
| 上下文 | 回归预算：入口小于 1,500 字符，新增单分册小于 14,000 字符；字符数不冒充 token 数 |
| 范围 | 九项 Recipe 保持规划；凭据、真实目标和原始日志不进入运行文档 |

## 真实验证

在仓库根目录执行。使用当前机器的授权目标与证据目录。SSH 先交互认证，密码不写文件；下面的主机占位符须替换。Windows 必须使用实际 Windows 会话。

```sh
rtk proxy python3 qa/development/huawei-cloud-fcaps-diagnostics/live/verify.py --catalog qa/development/huawei-cloud-fcaps-diagnostics/live/linux-cases.json --skill development/huawei-cloud-fcaps-diagnostics --host <authorized-host> --output .workspaces/fcaps-official-20261022/linux-after.json
rtk proxy python3 qa/development/huawei-cloud-fcaps-diagnostics/live/kubernetes.py --skill development/huawei-cloud-fcaps-diagnostics --kubeconfig .workspaces/fcaps-platforms-20261021/kubeconfig --output .workspaces/fcaps-official-20261022/kubernetes-after.json
rtk proxy python3 qa/development/huawei-cloud-fcaps-diagnostics/live/cloud.py --context .workspaces/hcloud-fcaps-validation-20261019/resource-context.json --skill development/huawei-cloud-fcaps-diagnostics --output .workspaces/fcaps-official-20261022/post-write-checks.json
```

`live/kubernetes.py --setup` 仅用于名为 fcaps-validation 的本地 kind 集群，创建 fcaps-contracts 命名空间及 Pod、Service、PVC、NetworkPolicy 测试资源。指标依赖官方 Metrics Server；本次用 v0.9.0，并仅在此本地集群允许自签名 kubelet 证书，不能移植为 CCE 默认配置。其他集群和默认 kubeconfig 不改变。

`live/linux-cases.json` 只保存帮助调用和自动执行范围，不保存诊断命令正文。抓包、跟踪和扫描保持有条件执行；缺工具不自动安装。

## 摘要与门禁

```sh
rtk proxy python3 qa/development/huawei-cloud-fcaps-diagnostics/validate.py --evidence .workspaces/hcloud-fcaps-validation-20261019 --recheck .workspaces/fcaps-official-20261022/post-write-checks.json --write-verification
rtk proxy python3 qa/development/huawei-cloud-fcaps-diagnostics/platforms.py --skill development/huawei-cloud-fcaps-diagnostics --evidence .workspaces/fcaps-official-20261022 --write-verification
rtk proxy bash qa/development/huawei-cloud-fcaps-diagnostics/validate.sh --evidence .workspaces/hcloud-fcaps-validation-20261019 --recheck .workspaces/fcaps-official-20261022/post-write-checks.json --report-dir .workspaces/fcaps-official-20261022/cloud-gate
rtk proxy python3 qa/development/huawei-cloud-fcaps-diagnostics/platforms.py --skill development/huawei-cloud-fcaps-diagnostics --evidence .workspaces/fcaps-official-20261022
rtk proxy python3 qa/development/huawei-cloud-fcaps-diagnostics/test_validation.py --evidence .workspaces/hcloud-fcaps-validation-20261019 --recheck .workspaces/fcaps-official-20261022/post-write-checks.json
rtk proxy python3 qa/development/huawei-cloud-fcaps-diagnostics/test_platforms.py --skill development/huawei-cloud-fcaps-diagnostics --evidence .workspaces/fcaps-official-20261022
```

先保留 pre-write 候选范围、来源、帮助与执行记录，再生成 post-write 证据。来源审阅不算帮助通过；无 Windows 环境时保留 blocked。摘要独立于命令正文，不参与运行文档摘要计算。

门禁读证据，不调用云 API，也不是运行时拦截器。版本、范围、结果或摘要不匹配时失败。报告和原始输出位于忽略的工作区。

## 官方文档补充验收

来源与验证边界以当前命令契约、文档索引和 QA fixtures 为准。已核验的 virtio/VBD 分支不能外推 SCSI、WWN 或 XEN；前缀冲突、分区冒充整盘及 PCI 不符时保持未解析。

```sh
rtk proxy python3 qa/development/huawei-cloud-fcaps-diagnostics/live/device_binding.py --context .workspaces/hcloud-fcaps-validation-20261019/resource-context.json --host <authorized-host> --skill development/huawei-cloud-fcaps-diagnostics --output .workspaces/fcaps-official-20261022/device-after.json
rtk proxy python3 qa/development/huawei-cloud-fcaps-diagnostics/test_device_binding.py
rtk proxy python3 qa/development/huawei-cloud-fcaps-diagnostics/test_response.py
```

2026-10-22 的 Kubernetes 15 条契约没有修改，沿用 2026-10-21 的同一行摘要和真实集群证据，不伪装成本次重新执行。原 1,282 条 hcloud 帮助沿用历史证据，本次重新执行资源依赖链。新网络探测以回环验证命令和输出；不据此宣称公网链路健康。

## 文档索引

索引只含元数据。`documents.py build` 合并已下载归档与 `documents-links.json` 的人工核验链接，更新 catalog.jsonl、入口日期说明和 QA 来源散列；不访问网络、不执行原文。归档正文散列与补充元数据散列分开。下面 `<archive-root>` 替换为该机器上的归档目录。`--snapshot-date` 应使用真实归档日期。

```sh
rtk proxy python3 qa/development/huawei-cloud-fcaps-diagnostics/documents.py build --archive <archive-root> --snapshot-date 2026-10-21 --report .workspaces/fcaps-documents-20261022/source-changes.json
rtk proxy python3 qa/development/huawei-cloud-fcaps-diagnostics/documents.py check --archive <archive-root> --report .workspaces/fcaps-documents-20261022/documents-check.json
rtk proxy python3 qa/development/huawei-cloud-fcaps-diagnostics/test_documents.py
```

没有本地归档时，省略 `check` 的 `--archive` 可核验索引结构及引用；这不等于对比源正文。当前 459 条元数据包含 441 条归档与 18 条补充指引，共 28 个精选主题。10 类负例覆盖重复、非官方来源、混入正文、ID/URL 不符、正文漂移、未知精选来源、过期入口日期、错误命令定位、同页重复格式及补充元数据漂移。正例验证 Markdown 与 HTML 来源可合并登记。
