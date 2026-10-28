---
status: draft
---

# 云硬盘、挂载点或文件系统容量异常，如何定位？

## Issue

“云盘显示有容量，但系统提示空间不足；或者挂载点不见了，无法确认数据在哪块盘上。”需要确认目标存储对象及异常所在层。

## Environment

- 华为云 ECS 与 EVS；Linux 块设备、分区、文件系统或 Windows 磁盘、分区、卷。
- Kubernetes 存储仅在工作负载实际使用 PVC/PV 时纳入。

## Resolution

1. 确认受影响路径、读写错误及时间窗。用 [H-volume](../../helpers.md#h-volume) 找到目标云盘，再读 [EVS/ShowVolume/v2](../../commands/configuration/hcloud.md#evs)；不以容量相同认定是同一块盘。
2. Linux 读取 [LINUX/block-devices](../../commands/configuration/linux.md) 和 [LINUX/mounts](../../commands/configuration/linux.md)，按 [H-device](../../helpers.md#h-device) 绑定云盘与整盘，再确定分区。Windows 结合 [WINDOWS/disks](../../commands/configuration/windows.md)、分区、卷及磁盘身份查询；无法唯一映射时保留缺口。
3. Linux 对目标路径读取 [LINUX/filesystem-space](../../commands/performance/linux.md) 和 [LINUX/filesystem-inodes](../../commands/performance/linux.md)。需要比较目录占用时限定 [LINUX/directory-usage](../../commands/performance/linux.md) 范围；df/du 差异按 [LINUX/deleted-open-files](../../commands/fault/linux.md)及[文档指引](../../documents/huaweicloud.md#f-故障)补证据。
4. PVC 场景按 [KUBERNETES/storage](../../commands/configuration/kubernetes.md) 返回的 volumeName 继续查 PV；未绑定时结合 [Pod 事件](../../commands/fault/kubernetes.md)定位。I/O 慢则转到[性能诊断](performance.md)。
5. 报告云盘、设备、分区、文件系统各层已确认的关系和状态。扩容、格式化、卸载或文件系统修复不在本查询流程内；处理后验证同一对象的挂载、容量及业务读写。

## Cause

尚未确定。云盘容量、文件系统容量和目录占用口径不同；空间告警或映射缺失不能直接归因于云盘故障。
