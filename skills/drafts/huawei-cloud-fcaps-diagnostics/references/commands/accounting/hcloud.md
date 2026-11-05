# 计量计费 A

核对用量、费用和订购状态。BSS 查询按账号站点和 help 选择区域。

表格约定见[索引](../index.md)。按完整命令 ID 搜索，只读取命中行和必要 Helper。

目录：[BSS](hcloud.md#bss) · [LTS](hcloud.md#lts) · [WAF](hcloud.md#waf)

## BSS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `BSS/ListCosts/v2` | 读取成本数据 | — | `time_condition.time_measure_id` 为时间单位：1 天、2 月 |
| `BSS/ListCustomerBillsFeeRecords/v2` | 读取流水账单 | — | — |
| `BSS/ListCustomerBillsMonthlyBreakDown/v2` | 读取月度成本 | — | — |
| `BSS/ListCustomerOnDemandResources/v2` | 读取客户按需资源列表 | `customer_id` | — |
| `BSS/ListCustomerOrders/v2` | 读取订单列表 | — | — |
| `BSS/ListCustomerselfResourceRecordDetails/v2` | 读取资源详单 | — | — |
| `BSS/ListCustomerselfResourceRecords/v2` | 读取资源消费记录 | — | — |
| `BSS/ListFreeResourceInfos/v2` | 读取资源包列表 | — | — |
| `BSS/ListFreeResourceUsages/v2` | 读取资源包使用量 | — | — |
| `BSS/ListFreeResourcesUsageRecords/v2` | 读取资源包使用明细 | — | — |
| `BSS/ListPayPerUseCustomerResources/v2` | 读取客户包年/包月资源列表 | — | 查询包年/包月资源；KooCLI 7.2.12 使用 `cn-north-1` |
| `BSS/ShowCustomerAccountBalances/v2` | 读取账户余额 | — | KooCLI 7.2.12 使用 `cn-north-1` |
| `BSS/ShowCustomerMonthlySum/v2` | 读取汇总账单 | — | — |
| `BSS/ShowCustomerOrderDetails/v2` | 读取订单详情 | `order_id` | — |

## LTS

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `LTS/EnableLogCollection/v2` | 开启超额采集：打开超额采集开关 | — | — |
| `LTS/ListTimeLineTrafficStatistics/v2` | 读取按时间段统计查询资源 | — | — |
| `LTS/ListTopnTrafficStatistics/v2` | 读取日志组或日志流流量的 Top N 统计 | — | — |

## WAF

| 命令 | 作用 | 输入与来源 | 约束 |
| --- | --- | --- | --- |
| `WAF/ConfirmUserBundle/v1` | 读取用户套餐信息 | — | — |
| `WAF/ShowSubscriptionInfo/v1` | 读取租户订购信息 | — | — |
