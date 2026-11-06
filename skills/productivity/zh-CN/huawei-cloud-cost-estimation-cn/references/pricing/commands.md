# 询价命令与字段

调用前读 `../gotchas.md` G01–G06。使用 `--cli-output=json` 和当前操作帮助。本文件定义命令字段，`rfq-models/rfq-core.yml` 定义字段关系。 CLI数组用`product_infos.1.*`；报错中的`productInfos`不改变CLI拼写。

## 查资源类型与规格

1. 服务编码未知时查 `ListServiceTypes`；用 `ListServiceResources(--service_type_code)` 找资源类型。
2. 按目标区域和模式查 `ListResourceSpecs`，保留候选的服务／类型／区域／模式／规格及分页标记。
3. 按需产品查 `ListUsageTypes(--resource_type_code)`、`ListMeasureUnits`，再建立G03–G04 要求的产品映射。

### BSS/ListResourceSpecs

[API](https://support.huaweicloud.com/api-oce/qct_00008.md)。必填：`cloud_service_type`、`resource_type`、`region_code`、`charge_mode`（`1` 包周期，`3` 按需）。

```bash
hcloud BSS ListResourceSpecs --charge_mode=<1-or-3> \
  --cloud_service_type=<service> --resource_type=<type> \
  --region_code=<deployment-region> \
  --filters.1.key=RESOURCE_SPEC --filters.1.value=<hint> \
  --limit=100 --cli-region=cn-north-1 --cli-output=json
```

有规格线索时使用筛选。首页不传 `marker`，后续使用返回的 `page_info.next_marker`，保持查询条件和 `limit` 不变。最多查看三页，再收窄剩余候选或请用户选择。

字典接口 `ListServiceTypes`、`ListServiceResources`、`ListResourceTypes`、`ListUsageTypes` 用 `limit/offset`：每页先取10条，按需增加，每次查询最多三页。`ListMeasureUnits`／`ListConversions` 不分页，结果在会话内复用。

## 包年包月询价

### BSS/ListRateOnPeriodDetail

[API](https://support.huaweicloud.com/api-bpconsole/bcloud_01002.md)。请求需 `project_id`。每项必填唯一 `id`、`cloud_service_type`、`resource_type`、`resource_spec`、`region`、`period_type`、`period_num`、`subscription_num`。

- `period_type`：`2` 月，`3` 年；`0` 天、`4` 小时仅用于支持的产品。`period_num` 为周期数。
- 已选 AZ 时填写 `available_zone`。`fee_installment_mode` 默认 `NA`；`HALF_PAY/ZERO_PAY` 仅适用于 CloudPond。
- 按产品要求补充下述容量字段。询价调用不分页。

```bash
hcloud BSS ListRateOnPeriodDetail --project_id=<project> \
  --product_infos.1.id=1 \
  --product_infos.1.cloud_service_type=<service> \
  --product_infos.1.resource_type=<type> \
  --product_infos.1.resource_spec=<verified-code> \
  --product_infos.1.region=<deployment-region> \
  --product_infos.1.period_type=<2-or-3> --product_infos.1.period_num=<count> \
  --product_infos.1.subscription_num=<quantity> \
  --cli-region=cn-north-1 --cli-output=json
```

## 按需询价

### BSS/ListOnDemandResourceRatings

[API](https://support.huaweicloud.com/api-bpconsole/bcloud_01001.md)。请求需 `project_id`。复用包周期模板的公共字段，将周期／分期字段换成 `usage_factor`、`usage_value`、`usage_measure_id`。询价调用不分页。

- `usage_factor` 取对应资源的 `ListUsageTypes.code`；`usage_value` 按已明确的使用量单位填写。`inquiry_precision=0` 返回六位小数，`1` 返回十位。
- 已知示例：Duration／小时用单位 `4`，流量／GB 通常用 `10`，请求次数通常用 `14`。先核实当前产品映射再采用。

## 询价参数约束

适用于上述两个询价接口。依据为2026-10-27的官方请求定义及KooCLI 7.2.12帮助；接口变化时重查当前帮助／API文档。

| 字段 | 类型／范围 |
| --- | --- |
| `product_infos` | 数组，最多100项；每项 ID 唯一 |
| `project_id`、项 `id`、`region`、`available_zone` | 字符串，最长64 |
| `cloud_service_type`、`resource_type`、`resource_spec` | 询价输入字符串，最长400 |
| `subscription_num` | 整数，1–10000 |
| `resource_size` | 整数，1–214783647；线性产品还需 `size_measure_id`；非线性产品省略／null 不过滤 |
| `size_measure_id` | 整数，产品容量单位 |
| `period_type`、`period_num` | 整数；类型值见上文，数量1–214783647 |
| `fee_installment_mode` | 字符串，最长64 |
| `usage_factor` | 字符串，最长64，不区分大小写 |
| `usage_value` | 十进制数，不要求整数 |
| `usage_measure_id`、`inquiry_precision` | 整数 |

`available_zone` 不区分大小写，省略／空／null 表示不筛选。分期模式省略／空／null 表示 `NA`。按需接口将容量／用量单位 ID 的最大长度记为4，这不是数值范围。

## 容量和单位

`resource_size` 表示每项订购容量／规模，需要时与 `size_measure_id` 配对，用量另行保留。

| 产品／范围 | 已核实映射 |
| --- | --- |
| 云硬盘：`hws.resource.type.volume` | 容量 GB，`size_measure_id=17` |
| 带宽：`hws.resource.type.bandwidth`、`hws.resource.type.share_bandwidth` | Mbps，`size_measure_id=15` |
| OBS：`hws.service.type.obs` / `hws.resource.type.obs`，`obs.size.ltcp.clr.standard.1az`，`cn-north-4`，按需 | 因子 `size`，`usage_value=GB × hours`，`usage_measure_id=10`；2026-10-27 用 KooCLI 7.2.12 验证 |

其他产品／规格查对应映射，映射不完整按 G03 处理。

## 读取报价与处理异常

- 包周期官网金额：`official_website_rating_result.official_website_amount`；分项：`product_rating_results[]`。可选折扣：`optional_discount_rating_results[]`，最优结果：`best_offer==1`。
- 按需：根级／分项 `official_website_amount`；`discount_amount>0` 时可按其含义展示对应 `amount`。
- `measure_id=1` 为元。`currency=CNY` 或 API 约定的空值为人民币。按请求 `id` 匹配分项，用完整精度相加后再舍入展示。
- 错误处理见 G01，报价交付边界见 G06；权限与伙伴代客范围见 `../iam-policies.md`。
