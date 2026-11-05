---
status: draft
---

# 业务变慢或主机负载升高，如何定位资源瓶颈？

## Issue

“业务响应变慢、吞吐下降，或者 CPU、内存、磁盘、网络指标升高。”需要判断资源异常是否与业务退化发生在同一时间和对象上。

## Environment

- 华为云 ECS、EVS、CES；主机为 Linux 或 Windows，工具和监控能力按目标环境核验。
- Kubernetes 使用率查询依赖实际集群的 metrics API。

## Resolution

1. 确认业务延迟、吞吐或错误的变化时间，选择可比的正常时段，并记录当时负载及近期变更。
2. 按实际指标和维度读取 [CES/ShowMetricData/v1](../../commands/performance/hcloud.md#ces)。比较前对齐对象、时间窗、单位与聚合口径；缺指标先核对采集条件。
3. 在已授权采样范围内，Linux 按问题选择 [LINUX/cpu-sample](../../commands/performance/linux.md)、[LINUX/memory](../../commands/performance/linux.md)、[LINUX/disk-sample](../../commands/performance/linux.md) 或网卡统计；Windows 先[发现计数器路径](../../commands/configuration/windows.md)，再用 [WINDOWS/counter](../../commands/performance/windows.md)有限采样。
4. 磁盘指标按 [H-device](../../helpers.md#h-device)关联 EVS；进程 I/O 可用 [LINUX/process-io](../../commands/performance/linux.md)补充。容器按 [KUBERNETES/pod-usage](../../commands/performance/kubernetes.md)查询；metrics API 缺失不记为使用率为零。
5. 按[性能文档指引](../../documents/huaweicloud.md#p-性能)解释观测，选择一个能区分瓶颈假设的后续检查。抓包、跟踪、压测和扩容须分别核对影响与授权；处理后在可比负载下复查业务指标与对应资源指标。

## Cause

尚未确定。单个高利用率、瞬时快照或与业务变慢同时出现的指标只能支持候选解释，不能单独证明根因。
