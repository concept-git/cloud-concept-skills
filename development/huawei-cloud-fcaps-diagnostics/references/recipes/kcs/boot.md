---
status: draft
---

# 云服务器启动失败或长时间未就绪，如何定位失败阶段？

## Issue

“云服务器启动后一直不可用，不知道是云平台还没完成启动，还是操作系统没有启动成功。”需要确定失败阶段及下一项检查。

## Environment

- 华为云 ECS；目标操作系统为 Linux 或 Windows，按实际发行版、版本和镜像选择查询。
- 使用已配置的 hcloud；主机查询依赖已可用的执行通道。账号、区域、实例及时间窗保留在事件记录中。

## Resolution

1. 确认最后一次正常启动、首次失败时间和近期镜像或配置变更；区分实例状态异常、系统启动异常和仅远程登录失败。
2. 用 [ECS/ShowServer/v2](../../commands/configuration/hcloud.md#ecs) 查询实例状态；已有异步任务时用 [ECS/ShowJob/v2](../../commands/fault/hcloud.md#ecs) 核对最终结果。请求被接受不表示启动完成。
3. 读取 [ECS/ShowServerConsoleOutput/v2](../../commands/fault/hcloud.md#ecs) 的已有控制台日志，按时间定位最后可见的启动阶段。日志缺失记为缺口，不触发重启或重装来补证据。
4. 目标系统可访问时，经已确认的执行通道读取 Linux 的 [LINUX/kernel-journal](../../commands/fault/linux.md) 或 Windows 的 [WINDOWS/events](../../commands/fault/windows.md)。主机不可访问时保留云侧证据；系统已启动但登录失败则转到[登录诊断](login.md)。
5. 结合[官方文档指引](../../documents/huaweicloud.md#f-故障)核对适用条件，按[输出要求](../../../SKILL.md#输出)记录失败阶段、支持证据及缺口。后续修复应验证实例状态、系统启动完成和目标业务可用性。

## Cause

尚未确定。实例状态、控制台日志和系统事件用于区分失败阶段；单独的启动超时或登录失败不足以确认根因。
