# 询价命令与字段说明

按当前需求读对应小节。查询使用 `--cli-output=json`；BSS 固定 `--cli-region=cn-north-1`，请求中的资源区域按用户选择填写。具体参数以当前操作的 `--help` 为准。

## 先保留完整证据

先读完整 JSON、判断业务错误，再筛选字段；错误可能与成功响应一样返回到标准输出。保留请求条件、错误信息和分页标记，不能用 `head` 截断结果或把解析失败当作空列表。展示给用户时可以精简。

规格候选以 `(cloud_service_type, resource_type, region_code, charge_mode, resource_spec)` 共同标识，名称只用于说明。筛选后也要保留这五项和 `page_info.next_marker`。返回行与请求条件不一致时，不用于询价。

每次询价保留候选身份、项目范围、周期／用量、数量、容量和单位，用请求行 `id` 对应响应金额。使用同一账号及目标区域对应的项目。切换区域、计费方式或规格时重新查询；变更周期、用量、数量或容量时重新询价。

## 查找资源类型与规格

1. 用 `ListServiceResources(--service_type_code)` 找资源类型；服务编码不清楚时先查 `ListServiceTypes`。编码使用查询原文，不拼接、不改大小写。
2. 用 `ListResourceSpecs` 查目标区域和计费方式下的规格；价格目录只证明目录匹配，不证明有库存或有开通权限。
3. 按需产品用 `ListUsageTypes(--resource_type_code)` 查计费因子，再结合 `ListMeasureUnits` 确认单位；不能默认 `Duration`。按资源类型过滤是本技能规则，API 将该筛选参数列为可选。

### BSS/ListResourceSpecs

[官方说明](https://support.huaweicloud.com/api-oce/qct_00008.html)。只读，必填 `cloud_service_type`、`resource_type`、`region_code`、`charge_mode`。

- `charge_mode=1`：包年／包月；`3`：按需。包月和包年在询价时通过周期字段区分。
- 有规格线索时带 `filters.1.key=RESOURCE_SPEC` 和 `filters.1.value`。该过滤支持模糊匹配，须核对完整编码、配置和规格族，不能默认取第一条。
- `limit=100`；首页不传 `marker`，后续使用响应的 `next_marker`，同时保留 `limit`，翻页时不改查询条件。
- 最多查三页；仍有下一页或多个实质不同候选时，说明已查范围并缩小条件或请用户选择。局部结果不能证明规格不存在。
- 使用返回的 `resource_spec`；OS 若已包含在编码中，不再加后缀。创建接口的规格 ID 另从服务侧查询并建立映射。

```bash
hcloud BSS ListResourceSpecs --charge_mode=<1或3> \
  --cloud_service_type=<服务编码> --resource_type=<资源类型编码> \
  --region_code=<部署区域> \
  --filters.1.key=RESOURCE_SPEC --filters.1.value=<规格线索> \
  --limit=100 --cli-region=cn-north-1 --cli-output=json
```

字典接口 `ListServiceTypes`、`ListServiceResources`、`ListResourceTypes`、`ListUsageTypes` 使用 `limit/offset`；默认每页 10 条，可按需求扩大，每次最多三页。`ListMeasureUnits` 和 `ListConversions` 不分页。度量单位可在当前会话内复用。

## 包年／包月询价

### BSS/ListRateOnPeriodDetail

[官方说明](https://support.huaweicloud.com/api-bpconsole/bcloud_01002.html)。只读，询价接口不分页。

- 请求必填 `project_id`。
- 每行必填 `id`、`cloud_service_type`、`resource_type`、`resource_spec`、`region`、`period_type`、`period_num`、`subscription_num`；同一请求的 `id` 不重复。
- 月：`period_type=2`；年：`3`。`period_num` 是周期数量；其他周期 `0=天、4=小时` 仅在产品支持时使用。
- “包年一次购买”和“按月购买十二次”不擅自视为同一价格；按用户选定的周期直接询价。按月乘十二只能作为明确标注的外推估算。
- `subscription_num` 为 1–10000。线性产品需要的容量和单位见下一节。
- `available_zone` 有明确选择时填写；空值表示不按 AZ 筛选，不代表全部 AZ 可用。
- `fee_installment_mode` 默认 `NA`，其他取值 `HALF_PAY/ZERO_PAY` 暂仅 CloudPond；以当前 help 为准。

```bash
hcloud BSS ListRateOnPeriodDetail --project_id=<项目ID> \
  --product_infos.1.id=1 \
  --product_infos.1.cloud_service_type=<服务编码> \
  --product_infos.1.resource_type=<资源类型编码> \
  --product_infos.1.resource_spec=<已核验的规格编码> \
  --product_infos.1.region=<部署区域> \
  --product_infos.1.period_type=<2或3> --product_infos.1.period_num=<周期数量> \
  --product_infos.1.subscription_num=<购买数量> \
  --cli-region=cn-north-1 --cli-output=json
```

## 按需询价

### BSS/ListOnDemandResourceRatings

[官方说明](https://support.huaweicloud.com/api-bpconsole/bcloud_01001.html)。只读，询价接口不分页。

- 请求必填 `project_id`。
- 每行必填 `id`、`cloud_service_type`、`resource_type`、`resource_spec`、`region`、`usage_factor`、`usage_value`、`usage_measure_id`、`subscription_num`。
- `usage_factor` 来自对应资源类型的 `ListUsageTypes.code`；`usage_value` 是该计费因子的使用量。`inquiry_precision=0` 默认保留 6 位，`1` 为 10 位。
- 已确认的常见映射：`Duration` 按小时使用单位 `4`；流量 GB 常用 `10`，请求次数常用 `14`。容量按时累计的用量可能为 GB×小时；只有当前产品契约已确认时才按容量×小时计算。
- `ListUsageTypes` 不提供完整单位映射。通过 `ListMeasureUnits` 和产品定义确认，不能仅凭因子名含 `size`、`flow` 或单位缩写猜测。
- 已验证场景（KooCLI 7.2.12，2026-10-27）：北京四 `hws.service.type.obs` / `hws.resource.type.obs` 的 `obs.size.ltcp.clr.standard.1az`，按需因子 `size` 使用 `usage_value=GB×小时`、`usage_measure_id=10`；单位 `72` 返回 `CBC.6050`，不能仅因字典名称是 GB·小时就选它。其他产品或规格重新核实适用性。
- 用量单位 `usage_measure_id` 与订购容量单位 `size_measure_id` 各有用途，同名“GB”不能直接互换。

数组参数统一使用 `--product_infos.1.*`、`--product_infos.2.*`，不传 JSON 字符串或方括号数组。报错中的 `productInfos` 不代表 CLI 字段改名：先对照当前 help 和实际请求；不要用 `body.demand` 包装产品行，也不要向按需接口传包周期字段。按需命令沿用上述包周期模板的公共字段，将周期参数替换为当前查得的计费因子、使用量和用量单位。

## 询价参数约束

以下约束适用于上述两种询价 API；按操作区分的字段仅用于对应模式。依据各操作官方请求定义，并与 KooCLI 7.2.12 帮助核对（2026-10-27）；help 未列出的长度和范围来自官方文档。接口升级时重新核对。

| 字段 | 类型与限制 |
| --- | --- |
| `product_infos` | 产品行数组，最多 100 项；同次请求的行 `id` 唯一 |
| `project_id`、行 `id`、`region`、`available_zone` | string，最长 64 |
| `cloud_service_type`、`resource_type`、`resource_spec` | string，最长 400；此处为询价输入限制，规格目录接口有自己的限制 |
| `subscription_num` | integer，1–10000 |
| `resource_size` | integer，1–214783647；线性产品与 `size_measure_id` 成对必填，非线性产品省略／null 不作为筛选 |
| `size_measure_id` | integer；单位按当前产品合同确认 |
| 包周期 `period_type`、`period_num` | integer；周期枚举见对应操作，周期数量为 1–214783647 |
| 包周期 `fee_installment_mode` | string，最长 64；默认值与适用产品见对应操作 |
| 按需 `usage_factor` | string，最长 64，大小写不敏感；保留来源编码 |
| 按需 `usage_value` | number（API 为 BigDecimal），按因子和单位解释，不强制转为整数 |
| 按需 `usage_measure_id`、`inquiry_precision` | integer；前者为用量单位，后者为可选精度模式 |

两种模式的 `available_zone` 均大小写不敏感；未传、空串或 null 表示不筛选。费用分期仅适用于 CloudPond，`fee_installment_mode` 未传、空串或 null 时为 `NA`。按需的容量与用量单位 ID 在官方文档中均标为“最大长度 4”，不把整数长度自行改写为取值范围。

## 容量和单位

按当前产品的请求定义判断是否需要 `resource_size` 和 `size_measure_id`。`resource_size` 表示订购容量或规模，不能用它替代按需的使用量。

下面是已知示例，不是产品白名单：

- 云硬盘 `hws.resource.type.volume`：容量 GB，`size_measure_id=17`。
- 带宽 `hws.resource.type.bandwidth`、`hws.resource.type.share_bandwidth`：带宽 Mbps，`size_measure_id=15`。

RDS 存储、DCS、ELB 等须另外核对该产品的容量含义及单位。通用 help 列出 `14=个`、`17=GB` 等，只证明这些单位存在，不证明某个产品应使用哪个。

出现“缺少 resourceSpecSize”时，先确认该产品需要的容量维度和单位。购买数量 `subscription_num=1` 不能证明 `resource_size=1`，单位为“个”或 GB 都一样。缺少对应依据时，将此项列为待核实并移出已核实小计，继续查询其他已明确项目；返回金额本身不能证明参数含义正确。

## 报价交付

写明查询日期。价格快照不能证明有效期、保价、税费口径或 SLA；这些条款须有明确来源，或标为用户指定的假设。必需项目未定价时，标题用“已核实部分小计”，旁边列出缺项。架构图和费用明细沿用已确认配置，变化单独说明。按未舍入金额汇总，展示时再取小数位。

## 读取报价与处理异常

- 包周期官网价：`official_website_rating_result.official_website_amount`；分项在其 `product_rating_results[]`。有折扣时读取 `optional_discount_rating_results[]`，按 `best_offer==1` 识别最优结果。
- 按需官网价：根级及分项 `official_website_amount`；`discount_amount>0` 时可展示对应 `amount`。
- `measure_id=1` 表示元，`currency=CNY` 或接口约定的空值表示人民币。按请求行 `id` 对应分项，核对金额合计；按需返回金额已包含 `usage_value`，不重复相乘。
- 零金额：如实保留 `0`、产品 ID、分项和请求条件。未核实适用范围或条件前，不据此承诺免费；也不直接推断“无报价”或“站点配置错误”。
- 空列表：说明本次条件和已查页数未找到结果，不推断全站无此产品。
- 业务错误：保留错误码和原文，把已知事实与原因假设分开。`CBC.0100` 查参数组合；`CBC.99006006` 查服务、类型、规格、区域和计费方式；`CBC.99006055` 查批次与周期，不擅自改用户需求。
- `CBC.6006/CBC.6050` 仅在取得明确字段或单位依据后修正重试一次，不穷举。429 等待 2 秒重试一次；权限错误读 `../iam-policies.md`。

字段关系或跨产品配对不清楚时，再读 `rfq-models/rfq-core.yml` 及当前计费方式的模型；仅核对公共维度时只读核心文件。项目 ID 用当前 IAM 的 `KeystoneListAuthProjects` 或 `KeystoneListProjects` 查询；伙伴代客的身份范围见 `../iam-policies.md`，不在聊天中传递 Token。
