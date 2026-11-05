# 共享查询 · hcloud

跨 FCAPS 的身份、作用域、审计与日志查询。按命令 ID 读取；CLI 规则见 [hcloud](../../tools/hcloud.md)。

目录：[CTS](hcloud.md#cts) · [EPS](hcloud.md#eps) · [IAM](hcloud.md#iam) · [LTS](hcloud.md#lts)

## CTS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `CTS/ListTraces/v3` | 读取事件列表 | — | 管理事件用 `trace_type=system`；在线窗口为近 7 天 |

## EPS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `EPS/ListEnterpriseProject/v1` | 读取企业项目列表 | — | — |
| `EPS/ListProviders/v1` | 读取企业项目支持的服务 | — | — |
| `EPS/ListResourceMapping/v1` | 读取资源类型映射 | — | — |
| `EPS/ShowAssociatedResources/v1` | 读取关联资源 | `resource_id`、`region_id` | — |
| `EPS/ShowEnterpriseProject/v1` | 读取企业项目详情 | `enterprise_project_id` | — |
| `EPS/ShowResourceBindEnterpriseProject/v1` | 读取企业项目绑定的资源列表 | `enterprise_project_id` | — |

## IAM

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `IAM/KeystoneListAuthDomains/v3` | 读取IAM用户可以访问的账号详情 | — | — |
| `IAM/KeystoneListAuthProjects/v3` | 读取IAM用户可以访问的项目列表 | — | — |
| `IAM/KeystoneListEndpoints/v3` | 读取终端节点列表 | — | — |
| `IAM/KeystoneListProjects/v3` | 读取指定条件下的项目列表 | — | — |
| `IAM/KeystoneListProjectsForUser/v3` | 读取指定IAM用户的项目列表 | `user_id` | — |
| `IAM/KeystoneListRegions/v3` | 读取区域列表 | — | — |
| `IAM/KeystoneListServices/v3` | 读取服务列表 | — | — |
| `IAM/KeystoneShowCatalog/v3` | 读取服务目录 | — | — |
| `IAM/KeystoneShowProject/v3` | 读取项目详情 | — | — |
| `IAM/ShowProjectDetailsAndStatus/v3` | 读取项目详情与状态 | — | — |

## LTS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `LTS/ListBreifStructTemplate/v2` | 读取结构化模板简略列表 | — | — |
| `LTS/ListCriterias/v2` | 读取快速查询 | `group_id`、`topic_id` | — |
| `LTS/ListHistorySql/v2` | 读取用户历史sql | `log_group_id`、`log_stream_id`；缺 `log_group_id` → [LTS/ListLogGroups/v2](hcloud.md#lts) | — |
| `LTS/ListLogContext/v2` | 读取上下文日志 | `line_num` ← [LTS/ListLogs/v2](hcloud.md#lts) | 自定义时间另需 `__time__` |
| `LTS/ListLogGroups/v2` | 读取账号下所有日志组 | — | — |
| `LTS/ListLogHistogram/v2` | 读取日志直方图 | `group_id`、`stream_id` | — |
| `LTS/ListLogStream/v2` | 读取指定日志组下的所有日志流 | `log_group_id`；缺 `log_group_id` → [LTS/ListLogGroups/v2](hcloud.md#lts) | — |
| `LTS/ListLogStreamIndex/v2` | 读取日志流索引 | `group_id`、`stream_id` | — |
| `LTS/ListLogStreams/v2` | 读取日志流信息 | — | — |
| `LTS/ListLogs/v2` | 读取日志 | 日志组、日志流及时间窗 | 仅查询已接入日志 |
| `LTS/ListQueryAllSearchCriterias/v2` | 读取日志组下所有快速查询 | `group_id` | — |
| `LTS/ListQueryStructuredLogs/v2` | 读取结构化日志 | `log_group_id`、`log_stream_id`；缺 `log_group_id` → [LTS/ListLogGroups/v2](hcloud.md#lts) | — |
| `LTS/ListStructTemplate/v2` | 读取结构化模板 | — | — |
| `LTS/ListStructuredLogsWithTimeRange/v2` | 读取结构化日志(新版) | `log_stream_id`；缺 `log_stream_id` → [LTS/ListLogStreams/v2](hcloud.md#lts) | — |
| `LTS/ShowStructTemplate/v2` | 读取结构化配置 | — | — |
