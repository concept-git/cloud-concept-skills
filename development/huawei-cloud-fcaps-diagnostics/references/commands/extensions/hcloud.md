# 扩展与边界

HCS 操作只适用于对应环境。敏感读取和订购命令仅用于识别边界。

表格约定见[索引](../index.md)。按完整命令 ID 搜索，只读取命中行和必要 Helper。

目录：[AOM](hcloud.md#aom) · [APM](hcloud.md#apm) · [ECS](hcloud.md#ecs) · [HCSCLOUDNETDEBUG](hcloud.md#hcscloudnetdebug) · [HSS](hcloud.md#hss) · [SecMaster](hcloud.md#secmaster)

## AOM

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `AOM/ListAccessCode/v2` | 敏感读取：获取Prometheus实例调用凭证 | — | — |

## APM

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `APM/ListAkSk/v1` | 敏感读取：获取ak/sk | — | — |
| `APM/ShowAkSks/v1` | 敏感读取：查询租户的aksk | — | — |
| `APM/ShowToken/v1` | 敏感读取：获取链路追踪应用的token | `x-business-id`、`business_id` | — |

## ECS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `ECS/ShowServerPassword/v2` | 敏感读取：云服务器获取密码(企业项目) | `server_id: ECS.ServerId`；缺 `server_id` → [ECS/ListServersDetails/v2](../configuration/hcloud.md#ecs) | — |

## HCSCLOUDNETDEBUG

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `HCSCLOUDNETDEBUG/CreateCurSessionElbQuery/v1` | 创建ELB当前连接查询任务 | — | — |
| `HCSCLOUDNETDEBUG/CreateHistSessionElbQuery/v1` | 创建ELB历史连接查询任务 | `elb_id` | — |
| `HCSCLOUDNETDEBUG/ListCurSessionElbTask/v1` | 读取ELB当前连接查询任务列表 | — | — |
| `HCSCLOUDNETDEBUG/ListFlowMonitors/v1` | 读取网络流监控列表 | — | — |
| `HCSCLOUDNETDEBUG/ListFlowPaths/v1` | 读取获取业务流监控数据 | `id` | — |
| `HCSCLOUDNETDEBUG/ListHistSessionElbTask/v1` | 读取ELB历史连接查询任务列表 | — | — |
| `HCSCLOUDNETDEBUG/ListVmInfo/v1` | 读取id信息 | — | — |
| `HCSCLOUDNETDEBUG/Listinstances/v1` | 读取实例或注入点信息 | — | — |
| `HCSCLOUDNETDEBUG/ShowElbCurSessionElbTaskDetail/v1` | 读取ELB当前连接查询任务结果查询 | `task_id` | 复用已有任务标识 |
| `HCSCLOUDNETDEBUG/ShowElbHistSessionElbTaskDetail/v1` | 读取ELB历史连接查询任务结果查询 | `task_id` | 复用已有任务标识 |
| `HCSCLOUDNETDEBUG/ShowFullLinkPaths/v1` | 读取全链路虚拟路径查询 | `dst_id`、`src_id` | — |
| `HCSCLOUDNETDEBUG/StartElbCurSessionElbTask/v1` | 执行ELB当前连接查询任务 | `task_id` | 复用已有任务标识 |
| `HCSCLOUDNETDEBUG/StartElbHistSessionElbTask/v1` | 执行ELB历史连接查询任务 | `task_id` | 复用已有任务标识 |

## HSS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `HSS/CreateQuotasOrder/v5` | 订购或配置：HSS服务创建订单订购配额 | — | — |

## SecMaster

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `SecMaster/CreateSubscriptionOrder/v1` | 订购或配置：开通或配置安全云脑订阅 | — | — |
