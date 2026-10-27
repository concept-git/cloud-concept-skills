# Pricing commands and fields

Read the sections needed for the current request. Use `--cli-output=json`. All BSS calls use `--cli-region=cn-north-1`; the resource region is the user's selected deployment region. Consult the current operation's `--help` for parameters.

## Preserve the evidence

Parse the complete JSON and check business errors before filtering fields. Errors may appear on stdout just like successful responses. Preserve request conditions, errors, and pagination markers. Do not truncate evidence with `head` or treat a parsing failure as an empty result. User-facing presentation may be shorter.

Identify a candidate by `(cloud_service_type, resource_type, region_code, charge_mode, resource_spec)` together; names are display labels. Retain all five fields and `page_info.next_marker` after filtering. Do not quote a returned row whose fields conflict with the request.

For each quote, preserve candidate identity, project scope, period or usage, quantity, capacity, and units. Match response amounts to request-line `id`. Use the same account and the project for the target region. Query specifications again when region, billing mode, or specification changes; reprice when period, usage, quantity, or capacity changes.

## Resolve resource types and specifications

1. Use `ListServiceResources(--service_type_code)` to find resource types. If the service code is unknown, query `ListServiceTypes` first. Preserve returned codes without concatenation or case changes.
2. Use `ListResourceSpecs` for the target region and billing mode. A pricing-directory match does not establish inventory or provisioning permission.
3. For pay-per-use, query `ListUsageTypes(--resource_type_code)` and resolve units with `ListMeasureUnits`. Do not default to `Duration`. Filtering by resource type is a skill rule; the API declares that filter optional.

### BSS/ListResourceSpecs

[API reference](https://support.huaweicloud.com/api-oce/qct_00008.html). Read-only. Required: `cloud_service_type`, `resource_type`, `region_code`, and `charge_mode`.

- `charge_mode=1`: yearly/monthly; `3`: pay-per-use. Distinguish yearly from monthly through the pricing request's period fields.
- When a specification hint exists, set `filters.1.key=RESOURCE_SPEC` and `filters.1.value`. Matching is fuzzy: check the full code, configuration, and family instead of choosing the first row.
- Use `limit=100`. Omit `marker` on the first page; subsequent pages use the returned `next_marker` together with `limit`. Keep query conditions unchanged while paging.
- Read at most three pages. If more pages or materially different candidates remain, state the inspected scope and narrow the query or ask the user to choose. Partial results do not prove absence.
- Use the returned `resource_spec`. Do not add an OS suffix already present in it. Obtain creation flavor IDs from the service API and retain their mapping to the quoted specification.

```bash
hcloud BSS ListResourceSpecs --charge_mode=<1-or-3> \
  --cloud_service_type=<service-code> --resource_type=<resource-type-code> \
  --region_code=<deployment-region> \
  --filters.1.key=RESOURCE_SPEC --filters.1.value=<specification-hint> \
  --limit=100 --cli-region=cn-north-1 --cli-output=json
```

Dictionary operations `ListServiceTypes`, `ListServiceResources`, `ListResourceTypes`, and `ListUsageTypes` use `limit/offset`. Start with 10 rows per page, increasing it as needed; inspect at most three pages per query. `ListMeasureUnits` and `ListConversions` have no pagination. Reuse measure-unit results within the current session.

## Yearly/monthly pricing

### BSS/ListRateOnPeriodDetail

[API reference](https://support.huaweicloud.com/api-bpconsole/bcloud_01002.html). Read-only. Pricing requests do not paginate.

- Request: `project_id` is required.
- Each line requires `id`, `cloud_service_type`, `resource_type`, `resource_spec`, `region`, `period_type`, `period_num`, and `subscription_num`. IDs must be unique within a request.
- Month: `period_type=2`; year: `3`. `period_num` is the number of periods. Other values, `0=day` and `4=hour`, apply only when the product supports them.
- Do not equate an annual purchase with twelve monthly purchases. Query the user's selected period directly. Monthly price multiplied by twelve is only an explicitly labeled extrapolation.
- `subscription_num` ranges from 1 to 10000. See the capacity section for linear-product capacity and units.
- Supply `available_zone` when selected. An empty value means no AZ filter; it does not mean availability in every AZ.
- `fee_installment_mode` defaults to `NA`; `HALF_PAY/ZERO_PAY` currently apply only to CloudPond. Follow current help.

```bash
hcloud BSS ListRateOnPeriodDetail --project_id=<project-id> \
  --product_infos.1.id=1 \
  --product_infos.1.cloud_service_type=<service-code> \
  --product_infos.1.resource_type=<resource-type-code> \
  --product_infos.1.resource_spec=<verified-specification-code> \
  --product_infos.1.region=<deployment-region> \
  --product_infos.1.period_type=<2-or-3> --product_infos.1.period_num=<period-count> \
  --product_infos.1.subscription_num=<quantity> \
  --cli-region=cn-north-1 --cli-output=json
```

## Pay-per-use pricing

### BSS/ListOnDemandResourceRatings

[API reference](https://support.huaweicloud.com/api-bpconsole/bcloud_01001.html). Read-only. Pricing requests do not paginate.

- Request: `project_id` is required.
- Each line requires `id`, `cloud_service_type`, `resource_type`, `resource_spec`, `region`, `usage_factor`, `usage_value`, `usage_measure_id`, and `subscription_num`.
- Obtain `usage_factor` from `ListUsageTypes.code` for the corresponding resource type. `usage_value` is that factor's usage. `inquiry_precision=0` defaults to six decimal places; `1` gives ten.
- Established examples: `Duration` in hours uses unit `4`; traffic in GB commonly uses `10`, and request counts commonly use `14`. Time-integrated capacity may be GB-hours. Multiply capacity by hours only when the current product contract establishes that meaning.
- `ListUsageTypes` does not provide a complete unit mapping. Confirm with `ListMeasureUnits` and the product definition; do not infer from `size`, `flow`, or a unit abbreviation alone.
- Verified case (KooCLI 7.2.12, 2026-10-27): for `hws.service.type.obs` / `hws.resource.type.obs`, `obs.size.ltcp.clr.standard.1az` in `cn-north-4`, pay-per-use factor `size` uses `usage_value=GB × hours` and `usage_measure_id=10`. Unit `72` is rejected with `CBC.6050`; do not select it merely because its dictionary label is GB-hours. Recheck applicability for other products or specifications.
- Usage units (`usage_measure_id`) and purchased-capacity units (`size_measure_id`) serve different purposes. Identically named GB units are not interchangeable.

Use dotted array arguments such as `--product_infos.1.*` and `--product_infos.2.*`, not JSON strings or bracket arrays. A server error mentioning `productInfos` does not rename the CLI field: check current help and the actual request shape. Do not wrap pricing lines in `body.demand` or send period fields to the pay-per-use API. Reuse the period template's common fields and replace its period parameters with the resolved usage factor, usage value, and usage unit.

## Pricing parameter constraints

These constraints apply to the two pricing APIs above; mode-specific fields belong only to that mode. Checked against their official request definitions and KooCLI 7.2.12 help on 2026-10-27. Lengths and ranges absent from help come from the API documentation; recheck them when the interface changes.

| Field | Type and constraint |
| --- | --- |
| `product_infos` | Product-line array, at most 100 items; line `id` is unique within the request |
| `project_id`, line `id`, `region`, `available_zone` | string, maximum length 64 |
| `cloud_service_type`, `resource_type`, `resource_spec` | string, maximum length 400 for pricing input; the specification-directory API has its own limits |
| `subscription_num` | integer, 1–10000 |
| `resource_size` | integer, 1–214783647; linear products require it together with `size_measure_id`; omitted/null values do not filter nonlinear products |
| `size_measure_id` | integer; resolve the unit from the current product contract |
| Period `period_type`, `period_num` | integer; period values are in the operation section, and the count is 1–214783647 |
| Period `fee_installment_mode` | string, maximum length 64; defaults and applicability are in the operation section |
| Pay-per-use `usage_factor` | string, maximum length 64, case-insensitive; retain the source code |
| Pay-per-use `usage_value` | number (API BigDecimal), interpreted with factor and unit; do not force an integer |
| Pay-per-use `usage_measure_id`, `inquiry_precision` | integer; usage unit and optional precision mode respectively |

For both modes, `available_zone` is case-insensitive; omitted, empty or null means no filter. Installments apply only to CloudPond; omitted, empty or null `fee_installment_mode` defaults to `NA`. The pay-per-use API documents both capacity and usage unit IDs with a maximum length of 4; do not invent a numeric range from that integer-length notation.

## Capacity and units

Use the current product's request definition to decide whether `resource_size` and `size_measure_id` are needed. `resource_size` describes purchased capacity or scale; it does not replace pay-per-use usage.

These are established examples, not an exhaustive product allowlist:

- Cloud disks, `hws.resource.type.volume`: capacity in GB, `size_measure_id=17`.
- Bandwidth, `hws.resource.type.bandwidth` and `hws.resource.type.share_bandwidth`: Mbps, `size_measure_id=15`.

For RDS storage, DCS, ELB, and other products, establish the product-specific capacity meaning and unit separately. Generic help listing `14=count` or `17=GB` establishes available unit codes, not which one a particular product requires.

On a missing `resourceSpecSize` error, identify the product-specific capacity dimension and unit before filling it. `subscription_num=1` does not justify `resource_size=1`, whether the unit is count or GB. Without that mapping, mark this line unverified, exclude it from the verified subtotal, and continue other resolved lines. A returned amount alone does not validate the mapping.

## Quote delivery

State the query date. A price snapshot does not establish a validity period, price guarantee, tax treatment, or SLA; include such terms only with an identified source or as explicitly user-supplied assumptions. When required items remain unpriced, headline the verified-items subtotal and list missing charges beside it. Reuse the confirmed configuration for diagrams and line items; label any changes. Keep full-precision amounts for totals and round for display.

## Read prices and handle exceptions

- Period list price: `official_website_rating_result.official_website_amount`; line items are its `product_rating_results[]`. When discounts are returned, inspect `optional_discount_rating_results[]` and identify the best result with `best_offer==1`.
- Pay-per-use list price: root-level and line-item `official_website_amount`. If `discount_amount>0`, the corresponding `amount` may be shown.
- `measure_id=1` means yuan. `currency=CNY`, or an empty value under the API's documented convention, means CNY. Match lines by request `id` and reconcile their sum. Pay-per-use amounts already include `usage_value`; do not multiply again.
- Zero amount: retain the actual zero, product ID, line items, and request conditions. Until coverage and conditions are verified, do not promise free service or infer that no price exists or the site configuration is wrong.
- Empty list: state that the inspected pages found no match under the current conditions, not that the product is absent everywhere.
- Business error: preserve its code and message, separating facts from causal hypotheses. For `CBC.0100`, check parameters; for `CBC.99006006`, check service, type, specification, region, and mode; for `CBC.99006055`, check batch and period without silently changing the user's request.
- For `CBC.6006/CBC.6050`, correct and retry once only after obtaining specific field or unit evidence; never enumerate guesses. On 429, wait two seconds and retry once. Read `../iam-policies.md` for permission errors.

If field relationships or cross-product mappings are unclear, read `rfq-models/rfq-core.yml` and the current billing-mode model; shared-dimension lookup needs only the core. Resolve the project with current IAM `KeystoneListAuthProjects` or `KeystoneListProjects`. Partner-on-behalf-of-customer scope is covered in `../iam-policies.md`; never transmit tokens through chat.
