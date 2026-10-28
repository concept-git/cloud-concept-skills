---
status: draft
---

# 无法通过 SSH 或远程桌面登录云服务器，如何定位？

## Issue

“我无法登录云服务器，客户端提示连接超时、连接被拒绝或认证失败。”需要判断失败发生在网络、服务还是认证阶段。

## Environment

- 华为云 ECS；Linux SSH 或 Windows 远程桌面，使用实际配置的目标地址和服务端口。
- 连接来源可能为公网、私网或跳板机；查询使用已有 hcloud 配置及可用的主机通道。

## Resolution

1. 保留客户端原始错误和发生时间，确认源、目的、端口及使用的登录身份；不将密码、私钥或登录地址写入文章或报告。
2. 用 [ECS/ShowServer/v2](../../commands/configuration/hcloud.md#ecs) 确认目标实例。实例未完成启动时转到[启动诊断](boot.md)；连接超时或拒绝时按[网络诊断](network.md)核对路径。
3. 已有其他主机通道时，先用 [H-unit](../../helpers.md#h-unit) 或 [H-win-service](../../helpers.md#h-win-service) 确定服务，再读 [LINUX/service-status](../../commands/fault/linux.md) 或 [WINDOWS/service-status](../../commands/fault/windows.md)，结合目标[连接信息](../../commands/configuration/linux.md)或 [WINDOWS/connections](../../commands/configuration/windows.md)检查服务状态。
4. 认证失败时读取同时间窗的 [LINUX/unit-journal](../../commands/fault/linux.md) 或 [WINDOWS/events](../../commands/fault/windows.md)；Linux 可用 [LINUX/failed-logins](../../commands/security/linux.md)补充。区分日志未采集、无权限与无匹配记录。
5. 输出已确认的失败阶段及一个下一步检查。端口探测须符合已有授权；端口连通不算登录成功。修复后需由授权用户验证实际登录，涉及密码重置或规则修改时另核对执行范围。

## Cause

尚未确定。客户端错误用于选择查询路径；只有目标网络、服务或认证证据与本次失败对应后，才能确认具体原因。
