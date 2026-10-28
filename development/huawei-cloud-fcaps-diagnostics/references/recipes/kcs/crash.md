---
status: draft
---

# 云服务器或工作负载意外重启、崩溃，如何定位？

## Issue

“服务突然中断，云服务器重启了，或者 Pod 不断重启。”需要区分人为操作、平台事件、系统异常和容器退出。

## Environment

- 华为云 ECS 上的 Linux 或 Windows；容器场景为已确认的 Kubernetes 集群和工作负载。
- 依据已有 CTS、系统事件、监控和容器日志；实际保留范围取决于采集配置。

## Resolution

1. 确认中断时间与时区，区分整机重启、单个服务退出和容器重建；记录当前实例或 Pod UID，避免把同名对象当作同一实例。
2. ECS 场景读取 [CTS/ListTraces/v3](../../commands/common/hcloud.md#cts) 及 [ECS/ListScheduledEvents/v2](../../commands/fault/hcloud.md#ecs)，与已有操作和平台事件对齐；注意 CTS 查询的保留窗口。
3. Linux 按时间窗读取 [LINUX/unit-journal](../../commands/fault/linux.md) 和 [LINUX/kernel-journal](../../commands/fault/linux.md)。后者仅覆盖当前启动；故障在上次启动时需另核验历史 boot 的帮助与日志可用性。Windows 使用 [WINDOWS/events](../../commands/fault/windows.md)。无历史日志时明确证据缺口。
4. 容器场景读取 [KUBERNETES/pods](../../commands/configuration/kubernetes.md)、[KUBERNETES/pod-events](../../commands/fault/kubernetes.md) 和 [KUBERNETES/previous-logs](../../commands/fault/kubernetes.md)；前一实例不存在与无读取权限分别记录。按需结合故障前的[性能证据](performance.md)。
5. 将事件按时间排序，区分操作记录、系统异常与推测；不为补证据主动触发转储或再次重启。后续处置按[恢复指引](recovery.md)明确验证条件，并观察原业务是否恢复及异常是否再现。

## Cause

尚未确定。重启次数和启动时间说明发生过状态变化；需要对应的操作、事件或日志才能确认具体触发原因。
