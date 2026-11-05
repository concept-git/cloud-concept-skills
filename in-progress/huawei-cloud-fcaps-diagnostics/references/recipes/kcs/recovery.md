---
status: draft
---

# 故障后需要恢复服务或数据，如何确定恢复方案和验收条件？

## Issue

“服务或数据不可用，需要尽快恢复，但不确定该回退配置、恢复备份还是采取其他操作。”需要形成可执行、可验证且已明确授权范围的恢复方案。

## Environment

- 华为云 ECS、EVS，以及实际使用的 CBR 备份或业务恢复机制。
- 恢复对象、业务依赖、备份机制和可接受的数据损失及中断范围由业务方确认。
- 尚未完成恢复演练；查询记录不代表备份可恢复。

## Resolution

1. 确认恢复目标、优先级、可接受中断及数据回退范围，保留当前故障证据。先明确需要恢复的是实例、数据、配置还是业务服务。
2. 通过 [ECS/ShowServer/v2](../../commands/configuration/hcloud.md#ecs)、[H-volume](../../helpers.md#h-volume)及 [EVS/ShowVolume/v2](../../commands/configuration/hcloud.md#evs)核对目标和关联资源；不把其他实例或同容量磁盘当作恢复目标。
3. 使用备份时，读取 [CBR/ListBackups/v1](../../commands/configuration/hcloud.md#cbr) 与 [CBR/ShowBackup/v1](../../commands/configuration/hcloud.md#cbr)，核对备份对象、时间和状态，并按[云硬盘恢复边界](../../documents/huaweicloud.md#f-故障)核对停机、挂载及数据覆盖条件。无适用恢复点时明确缺口。
4. 写出待执行步骤、影响对象、数据保护措施、授权范围、停止条件及失败后的处理方案。若操作不可逆或无法回退，明确说明；不把本指引视为执行恢复、重装或重启的授权。执行前按所选产品的当前文档与帮助核验参数。
5. 获得相应授权并执行后，查询已有任务的最终状态；CBR 任务使用 [CBR/ListOpLogs/v1](../../commands/fault/hcloud.md#cbr) 和 [CBR/ShowOpLog/v1](../../commands/fault/hcloud.md#cbr)。再核对数据、挂载、依赖及业务功能，将实际结果与验收条件逐项对照。

## Cause

不适用：本文回答如何准备和验收恢复方案，不预设故障根因。恢复成功也不代表根因已消除；未完成的根因调查应继续保留。
