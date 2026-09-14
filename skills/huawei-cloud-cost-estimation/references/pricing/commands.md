# 命令合同（RFQ 询价）

每个 op：**contract** + **CLI 模板**。事实/维度看 `semantic/*.yml`。数组用 dot notation（`--product_infos.1.*`）；输出 `--cli-output=json`；字典分页默认 `--limit=10 --offset=0`，每命令 ≤3 页。

## Universal Traps（每次询价必看）

1. **数组仅 dot notation** — JSON 串 / `[...]` KooCLI 不识别。
2. **询价 API 无分页** — 多项一次放进 `product_infos.N.*`。
3. **code 大小写敏感** — type / region / spec 用维度查询原文，不小写化、不拼接。
4. **解析链** — `ListServiceResources` → `ListResourceSpecs` → 按需 `ListUsageTypes(--resource_type_code)` → `ListMeasureUnits` + Measure Resolve → 询价。多候选则问；Specs 有行 ≠ 可询价；禁止默认 Duration/小时。
5. **Measure Resolve** — UsageTypes 无 measure（对齐 `ListMeasureUnits`）。用量槽≠容量槽
   （容量槽仅线性表）。同名 GB：用量 `type=3→10`，容量槽 `17`/`15`。factor 定族：
   `Duration`→`4`/小时；`size*|容量|存量`→`10`/**GB×小时**（勿 `resource_size`，禁 type7/72/87）；
   `*flow|retrieval*`→`10`/GB；`get|put|request*`→`14`/次。
   `CBC.6006`/`CBC.6050`：改 type/factor 或同 abbreviation sibling **一次**；禁穷举。
6. **参数类错误** — `CBC.0100` 核对运行时 help 与参数组合；`CBC.99006006` 回到规格、
   region、计费模式确认；`CBC.99006055` 缩小询价批次或周期。权限类（403/`CBC.0151`/429）
   见 `../iam-policies.md`。

---

## rfq_quote_execution

### `BSS/ListRateOnPeriodDetail` —— 包年/包月询价

> **method**: POST · **safety**: readonly · **entities**: `RFQ_Header`, `RFQ_Line` · **pagination**: n/a · **doc**: [bcloud_01002](https://support.huaweicloud.com/api-bpconsole/bcloud_01002.html)
> **required**: `project_id` + 每行 `id` / `cloud_service_type` / `resource_type` / `resource_spec` / `region` / `period_type` / `period_num` / `subscription_num`
> **conditional**: `linear_product` → `resource_size` + `size_measure_id`

```bash
hcloud BSS ListRateOnPeriodDetail \
  --project_id=<project_id> \
  --product_infos.1.id=1 \
  --product_infos.1.cloud_service_type=hws.service.type.ec2 \
  --product_infos.1.resource_type=hws.resource.type.vm \
  --product_infos.1.resource_spec=c6.2xlarge.2.linux \
  --product_infos.1.region=cn-north-1 \
  --product_infos.1.period_type=2 --product_infos.1.period_num=1 --product_infos.1.subscription_num=1 \
  --product_infos.2.id=2 \
  --product_infos.2.cloud_service_type=hws.service.type.ebs \
  --product_infos.2.resource_type=hws.resource.type.volume \
  --product_infos.2.resource_spec=GPSSD \
  --product_infos.2.region=cn-north-1 \
  --product_infos.2.resource_size=40 --product_infos.2.size_measure_id=17 \
  --product_infos.2.period_type=2 --product_infos.2.period_num=1 --product_infos.2.subscription_num=1 \
  --cli-region=cn-north-1 --cli-output=json
```

| 字段 | 类型 | 取值 | 备注 |
| --- | --- | --- | --- |
| `period_type` / `period_num` | int | 0 天 / 2 月 / 3 年 / 4 小时 | 包年包月通常 2 或 3 |
| `subscription_num` | int | 1..10000 | 询价数量 |
| `size_measure_id` | int | 仅线性三类 | 见容量槽表 |
| `fee_installment_mode` | string | HALF_PAY / ZERO_PAY / NA | 暂仅 CloudPond |

### `BSS/ListOnDemandResourceRatings` —— 按需询价

> **method**: POST · **safety**: readonly · **entities**: `RFQ_OnDemand_Header`, `RFQ_OnDemand_Line` · **pagination**: n/a · **doc**: [bcloud_01001](https://support.huaweicloud.com/api-bpconsole/bcloud_01001.html)
> **required**: `project_id` + 每行 `id` / `cloud_service_type` / `resource_type` / `resource_spec` / `region` / `usage_factor` / `usage_value` / `usage_measure_id` / `subscription_num`
> **conditional**: `linear_product` → `resource_size` + `size_measure_id`
> **optional**: `inquiry_precision`（0 默认 6 位 / 1 全 10 位）

混合按需（ECS + EVS + 按流量带宽）：

```bash
hcloud BSS ListOnDemandResourceRatings \
  --project_id=<project_id> \
  --product_infos.1.id=1 \
  --product_infos.1.cloud_service_type=hws.service.type.ec2 \
  --product_infos.1.resource_type=hws.resource.type.vm \
  --product_infos.1.resource_spec=c3.3xlarge.2.linux \
  --product_infos.1.region=cn-north-1 \
  --product_infos.1.usage_factor=Duration --product_infos.1.usage_value=2 --product_infos.1.usage_measure_id=4 \
  --product_infos.1.subscription_num=1 \
  --product_infos.2.id=2 \
  --product_infos.2.cloud_service_type=hws.service.type.ebs \
  --product_infos.2.resource_type=hws.resource.type.volume \
  --product_infos.2.resource_spec=SSD \
  --product_infos.2.region=cn-north-1 \
  --product_infos.2.resource_size=10 --product_infos.2.size_measure_id=17 \
  --product_infos.2.usage_factor=Duration --product_infos.2.usage_value=2 --product_infos.2.usage_measure_id=4 \
  --product_infos.2.subscription_num=1 \
  --product_infos.3.id=3 \
  --product_infos.3.cloud_service_type=hws.service.type.vpc \
  --product_infos.3.resource_type=hws.resource.type.bandwidth \
  --product_infos.3.resource_spec=12_sbgp \
  --product_infos.3.region=cn-north-1 \
  --product_infos.3.resource_size=1 --product_infos.3.size_measure_id=15 \
  --product_infos.3.usage_factor=upflow --product_infos.3.usage_value=4 --product_infos.3.usage_measure_id=10 \
  --product_infos.3.subscription_num=1 \
  --cli-region=cn-north-1 --cli-output=json
```

| 字段 | 类型 | 取值 | 备注 |
| --- | --- | --- | --- |
| `usage_factor` | string | 当次 `ListUsageTypes.code` | 禁止默认 Duration |
| `usage_value` | number | 按 Trap #5 编码 | 容量族=GB×小时；时长=小时；流量=GB |
| `usage_measure_id` | int | Trap #5 + `ListMeasureUnits` | 用量槽；≠ `size_measure_id` |
| `inquiry_precision` | int | 0 / 1 | 默认 6 位 / 全 10 位 |

---

## response_contract（报价怎么读）

只读当次响应，**不臆造折扣**。`measure_id=1`=元；`currency=CNY`（空=人民币）；`id` 回映射请求行。默认官网价；有折扣才附折后。分项之和=总额；on-demand 已含 `usage_value`，不再二次乘。

| API | 官网价 | 折后（有则报） |
| --- | --- | --- |
| `ListRateOnPeriodDetail` | `official_website_rating_result.official_website_amount`（分项同对象） | `optional_discount_rating_results[]` 取 `best_offer==1` |
| `ListOnDemandResourceRatings` | 根级 / `product_rating_results[]` 的 `official_website_amount` | `discount_amount>0` 时读 `amount` |

---

## dimension_lookup

| 操作 | 用途 | 必填 | 分页 |
| --- | --- | --- | --- |
| `BSS/ListServiceTypes` | `cloud_service_type` | - | limit/offset |
| `BSS/ListServiceResources` | →`resource_type` | `service_type_code` | limit/offset |
| `BSS/ListUsageTypes` | →`usage_factor` | **`resource_type_code`** | limit/offset |
| `BSS/ListMeasureUnits` | Measure Resolve（会话一次） | - | none |
| `BSS/ListResourceTypes` | 翻译 resource_type | - | limit/offset |
| `BSS/ListConversions` | 度量进制 | - | none |

```bash
hcloud BSS ListServiceResources --service_type_code=hws.service.type.ec2 \
  --cli-region=cn-north-1 --cli-output=json --limit=10 --offset=0
hcloud BSS ListUsageTypes --resource_type_code=hws.resource.type.vm \
  --cli-region=cn-north-1 --cli-output=json --limit=100 --offset=0
hcloud BSS ListMeasureUnits --cli-region=cn-north-1 --cli-output=json
```

---

## resource_spec_lookup

### `BSS/ListResourceSpecs` —— 规格解析唯一路径

> **method**: POST · **safety**: readonly · **entities**: `Dim_ResourceSpec` · **pagination**: marker/limit · **doc**: [qct_00008](https://support.huaweicloud.com/api-oce/qct_00008.html)
> **required**: `cloud_service_type` / `resource_type` / `region_code` / `charge_mode`（1 包年包月 / 3 按需）
> **optional**: `filters.[N].key=RESOURCE_SPEC` + `filters.[N].value`、`marker` + `limit`

- `marker`+`limit` 同用；首页无 `marker`；翻页用 `page_info.next_marker`。
- `charge_mode`/`region_code` 与询价 line 一致；返回值禁再拼 OS 后缀。
- 有规格线索必须带 `filters`；`limit=100`；3 页未收敛则停并让用户选；429 等 2s 重试一次。
- 候选取 `cloud_service_basics[].resource_spec`，复述用 `resource_spec_name`。

```bash
hcloud BSS ListResourceSpecs --charge_mode=1 \
  --cloud_service_type=hws.service.type.ec2 --resource_type=hws.resource.type.vm \
  --region_code=cn-north-4 \
  --filters.1.key=RESOURCE_SPEC --filters.1.value=c6.2xlarge \
  --limit=100 --cli-region=cn-north-1 --cli-output=json
```

### 线性产品容量槽（仅此三类可填 `resource_size`+`size_measure_id`）

| `resource_type` | `size_measure_id` | 单位 |
| --- | --- | --- |
| `hws.resource.type.volume` | 17 | GB |
| `hws.resource.type.bandwidth` | 15 | Mbps |
| `hws.resource.type.share_bandwidth` | 15 | Mbps |

## scope_resolve

```bash
hcloud IAM KeystoneListAuthProjects --cli-region=cn-north-1 --cli-output=json
hcloud IAM KeystoneListProjects --domain_id=<domain_id> --cli-region=cn-north-1 --cli-output=json
```

伙伴代客：置换客户 Token 后取 region 对应 `project_id`；见 `../iam-policies.md`。
