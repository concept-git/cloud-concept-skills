---
status: draft
---

# 配置已修改但未生效，或实际配置与预期不一致，如何核对？

## Issue

“配置已经改了，但行为没有变化；或者重启前后配置表现不同。”需要确认修改针对的对象，以及配置是否已下发、加载和持久化。

## Environment

- 华为云资源配置、Linux/Windows 主机配置或 Kubernetes 对象；按实际产品、版本和管理方式选择查询。
- 期望配置来自已确认的变更要求或配置基线；不从异常现象反推期望值。

## Resolution

1. 明确目标对象、配置项、期望值、原值及变更时间；将“提交了修改”“接口接受了请求”和“运行时已生效”分别记录。
2. 云侧按[配置分册](../../commands/index.md)读取目标资源和关联关系；异步修改仅查询已有任务结果。发现对象标识不一致时按 [Helper](../../helpers.md)重新绑定。
3. Linux 按需查询 [LINUX/kernel-setting](../../commands/configuration/linux.md)、[LINUX/service-enabled](../../commands/configuration/linux.md) 与 [LINUX/service-status](../../commands/fault/linux.md)。启用状态不等于运行状态；读取内核参数不等于检查持久化配置。
4. 防火墙场景区分 Linux [运行时区域规则](../../commands/security/linux.md)和 Windows [有效策略](../../commands/security/windows.md)。Kubernetes 场景核对[目标对象](../../commands/configuration/kubernetes.md)身份与实际状态。未覆盖的配置文件或应用加载机制按[文档入口](../../documents/index.md)补充依据和查询方式，不猜路径或默认值。
5. 将差异定位到目标选择、变更提交、运行时加载或持久化阶段。报告未核验的阶段；重新下发、重载或重启须有相应授权，处理后同时核对配置值与预期业务行为。

## Cause

尚未确定。观测到配置差异不代表已确认其成因；需结合对象身份、变更结果及产品加载机制判断。
