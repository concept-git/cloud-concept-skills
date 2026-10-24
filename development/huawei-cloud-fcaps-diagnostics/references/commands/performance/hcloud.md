# 性能 P

按同一资源和时间窗查询指标。OS 指标依赖实际采集能力。

表格约定见[索引](../index.md)。按完整命令 ID 搜索，只读取命中行和必要 Helper。

目录：[AOM](hcloud.md#aom) · [APM](hcloud.md#apm) · [CES](hcloud.md#ces) · [COC](hcloud.md#coc) · [ECS](hcloud.md#ecs) · [EVS](hcloud.md#evs)

## AOM

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `AOM/ListAllVersionByVersionId/v1` | 读取脚本版本查询 | `script_id` | — |
| `AOM/ListDashBoards/v2` | 读取仪表盘列表 | — | — |
| `AOM/ListDashboardsFolder/v2` | 读取仪表盘分组列表 | — | — |
| `AOM/ListInstantQueryAomPromGet/v2` | 读取GET方法查询瞬时数据 | — | — |
| `AOM/ListInstantQueryAomPromPost/v2` | 读取(推荐)POST方法查询瞬时数据 | — | — |
| `AOM/ListLabelValuesAomPromGet/v2` | 读取标签值 | `label_name` | — |
| `AOM/ListLabelsAomPromGet/v2` | 读取GET方法获取标签名列表 | — | — |
| `AOM/ListLabelsAomPromPost/v2` | 读取(推荐)POST方法获取标签名列表 | — | — |
| `AOM/ListLogItems/v2` | 读取日志 | — | — |
| `AOM/ListMetadataAomPromGet/v2` | 读取元数据查询 | — | — |
| `AOM/ListMetricItems/v2` | 读取指标 | — | — |
| `AOM/ListPromInstance/v2` | 读取Prometheus实例 | — | — |
| `AOM/ListRangeQueryAomPromGet/v2` | 读取GET方法查询区间数据 | — | — |
| `AOM/ListRangeQueryAomPromPost/v2` | 读取(推荐)POST方法查询区间数据 | — | — |
| `AOM/ListSample/v2` | 读取时序数据 | — | — |
| `AOM/ListSeries/v2` | 读取时间序列 | — | — |
| `AOM/ShowDashBoard/v2` | 读取仪表盘详情 | `dashboard_id` | — |
| `AOM/ShowMetricsData/v2` | 读取监控数据 | — | — |

## APM

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `APM/ChangeAgentStatus/v1` | 更改实例的采集状态 | `x-business-id` | — |
| `APM/ListAppEnvs/v1` | 读取组件下的环境列表 | `x-business-id`、`app_id` | — |
| `APM/ListApps/v1` | 读取组件列表 | `x-business-id`、`business_id` | — |
| `APM/ListBusiness/v1` | 读取应用列表 | — | — |
| `APM/ListBusinessEnv/v1` | 读取URL跟踪Region环境列表 | `x-business-id`、`business_id` | — |
| `APM/ListEnvInstances/v1` | 读取实例信息列表 | `x-business-id`、`env_id` | — |
| `APM/ListEnvMonitorItem/v1` | 读取监控项列表 | `x-business-id`、`env_id` | — |
| `APM/ListEnvTags/v1` | 读取环境标签 | `x-business-id`、`business_id` | — |
| `APM/ListOpenRegion/v1` | 读取开通的region | — | — |
| `APM/ListSupportedRegion/v1` | 读取所有的支持的region | — | — |
| `APM/SaveMonitorItemConfig/v1` | 修改采集配置：保存监控项 | `x-business-id`、`env_id`、`monitor_item_id` | — |
| `APM/SearchAgent/v1` | 读取应用下所有探针 | `x-business-id`、`business_id` | — |
| `APM/SearchApplication/v1` | 读取对指定区域下的组件和环境及其探针情况进行搜索 | `x-business-id`、`business_id` | — |
| `APM/SearchBusinessTopology/v1` | 读取应用全局拓扑图 | `x-business-id`、`target_business_id` | — |
| `APM/SearchEnvTopology/v1` | 读取组件环境拓扑图 | `x-business-id`、`target_env_id` | — |
| `APM/SearchTransaction/v1` | 读取URL跟踪视图列表 | `x-business-id`、`business_id` | — |
| `APM/SearchTransactionConfig/v1` | 读取URL跟踪配置列表 | `x-business-id`、`business_id` | — |
| `APM/ShowBusinessDetail/v1` | 读取单个应用的详情 | `x-business-id`、`business_id` | — |
| `APM/ShowClobDetail/v1` | 读取原始数据详情 | `x-business-id`、`clob_id`、`env_id` | — |
| `APM/ShowEnvMonitorItems/v1` | 读取监控项信息 | `x-business-id`、`env_id` | — |
| `APM/ShowEventDetail/v1` | 读取event的详情 | `env_id`、`event_id`、`span_id`、`trace_id` | — |
| `APM/ShowFlameLineTree/v1` | 读取ShowFlameLineTree | `x-business-id`、`instance_id` | — |
| `APM/ShowMonitorItemDetail/v1` | 读取一个监控项的详情 | `x-business-id`、`env_id`、`monitor_item_id` | — |
| `APM/ShowMonitorItemViewConfig/v1` | 读取监控项配置信息 | `x-business-id`、`collector_id`、`env_id` | — |
| `APM/ShowRawTable/v1` | 读取原始数据表格 | `x-business-id`、`env_id` | — |
| `APM/ShowSpanSearch/v1` | 读取span数据 | 应用 `x-business-id`、`biz_id` 和 `region` | 查询接口；IAM 访问级别标为 Write |
| `APM/ShowSubBusinessDetail/v1` | 读取子应用详情 | `x-business-id`、`sub_business_id` | — |
| `APM/ShowSumTable/v1` | 读取汇总表格数据 | `x-business-id`、`env_id` | — |
| `APM/ShowTopology/v1` | 读取调用链拓扑图 | `trace_id` | — |
| `APM/ShowTopologyTree/v1` | 读取应用树 | `x-business-id`、`business_id` | — |
| `APM/ShowTraceEvents/v1` | 读取一个trace的所有调用链数据 | `trace_id` | — |
| `APM/ShowTransactionDetail/v1` | 读取URL跟踪视图详情 | `x-business-id` | — |
| `APM/ShowTrend/v1` | 读取趋势图 | `x-business-id`、`env_id` | — |

## CES

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `CES/BatchCreateAgentInvocations/v3` | 安装或维护 Agent：批量创建Agent任务 | — | — |
| `CES/BatchListMetricData/v1` | 读取批量查询监控数据 | — | — |
| `CES/BatchListSpecifiedMetricData/v2` | 读取批量查询指标数据 | — | — |
| `CES/ListAgentDimensionInfo/v2` | 读取主机监控原始维度值 | `instance_id` | — |
| `CES/ListAgentInvocations/v3` | 读取Agent任务列表 | — | — |
| `CES/ListAgentStatus/v3` | 读取插件状态查询 | — | — |
| `CES/ListDashboardInfos/v2` | 读取监控看板列表 | — | — |
| `CES/ListDashboardWidgets/v2` | 读取指定监控看板下的监控视图列表 | `dashboard_id` | — |
| `CES/ListMetrics/v1` | 读取指标列表 | 目标实例的指标维度 | ECS 基础指标用 `SYS.ECS` |
| `CES/ListResourceGroup/v1` | 读取所有资源分组 | — | — |
| `CES/ListResourceGroups/v2` | 读取资源分组列表 | — | — |
| `CES/ListResourceGroupsServicesResources/v2` | 读取资源分组下指定服务类别特定维度的资源列表 | `group_id`、`service` | — |
| `CES/ShowMetricData/v1` | 读取监控数据 | 指标及维度；缺失 → [CES/ListMetrics/v1](hcloud.md#ces) | `from/to` 为毫秒时间戳 |
| `CES/ShowQuotas/v1` | 读取配额 | — | — |
| `CES/ShowResourceGroup/v1` | 读取资源分组下的资源 | `group_id` | — |
| `CES/ShowResourceGroup/v2` | 读取指定资源分组详情 | `group_id` | — |
| `CES/ShowWidget/v2` | 读取指定监控视图信息 | `widget_id` | — |

## COC

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `COC/ListAssessTask/v1` | 读取分页查询评估任务列表 | — | — |
| `COC/ListCapacityOrder/v1` | 读取应用、组件、分组容量数据的排名 | — | — |
| `COC/ListCapacityView/v1` | 读取应用的容量数据 | — | — |

## ECS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `ECS/BatchResizeServers/v2` | 批量变更云服务器规格 | `resize.servers.[N].id` | — |
| `ECS/ListResizeFlavors/v2` | 读取云服务器规格变更支持列表 | — | — |
| `ECS/RegisterServerMonitor/v2` | 注册监控：注册云服务器监控 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/ResizePostPaidServer/v2` | 变更云服务器规格(按需) | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/ResizeServer/v2` | 变更云服务器规格 | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |
| `ECS/ShowFlavorCapacity/v2` | 读取规格的容量 | `flavor_id` | — |

## EVS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `EVS/BatchResizeVolumes/v2` | 批量扩容云硬盘 | `volumes.[N].id` | — |
| `EVS/ModifyVolumeQoS/v2` | 修改云硬盘QoS | `volume_id: EVS.VolumeId`；缺 `volume_id` → [EVS/ListVolumes/v2](../configuration/hcloud.md#evs) | — |
| `EVS/ResizeVolume/v2` | 扩容云硬盘 | `volume_id: EVS.VolumeId`；缺 `volume_id` → [EVS/ListVolumes/v2](../configuration/hcloud.md#evs) | — |
