---
status: draft
---

# 出现安全告警、异常访问或权限拒绝，如何核实？

## Issue

“收到安全告警，发现异常登录或连接，或者原本可执行的查询被拒绝。”需要核实告警对象、实际权限及是否存在相互支持的安全证据。

## Environment

- 华为云 IAM、CTS 及实际启用的 HSS、CFW 等安全服务；目标主机为 Linux 或 Windows。
- Kubernetes 权限或网络策略仅在对应集群场景使用；身份与作用域以实际执行会话为准。

## Resolution

1. 记录告警时间、类型和受影响对象；先区分访问被拒绝与疑似异常访问。保留事件证据，不将账号凭据、令牌或原始敏感日志写入文章。
2. 权限拒绝时通过 [IAM 发现查询](../../commands/common/hcloud.md#iam)及[权限排查指引](../../documents/huaweicloud.md#s-安全)核对身份和授权范围；Kubernetes 使用 [KUBERNETES/permission](../../commands/security/kubernetes.md)。参数或权限问题未解决前不原样重试。
3. 安全告警按[安全分册](../../commands/index.md)选择已有结果查询，结合 [CTS/ListTraces/v3](../../commands/common/hcloud.md#cts)；[HSS/ListHostStatus/v5](../../commands/security/hcloud-host.md#hss) 只读已有状态时使用契约要求的 `refresh=false`，不自动启动扫描。
4. Linux 结合[登录记录](../../commands/security/linux.md)与 [LINUX/connections](../../commands/configuration/linux.md)，Windows 结合 [WINDOWS/events](../../commands/fault/windows.md)、[本地用户与组](../../commands/security/windows.md)及连接信息，按同一主机和时间窗关联。文件校验扫描须另核对影响与授权。
5. 报告已确认事实、支持的风险判断和证据缺口。需要隔离、阻断、查杀或重置凭据时交由具有相应授权的响应人员执行，并明确业务影响和复核条件；告警消失不能单独证明风险已消除。

## Cause

尚未确定。单条告警、登录失败、文件差异或权限拒绝不足以确认入侵；原因判断必须与实际身份、配置和事件证据一致。
