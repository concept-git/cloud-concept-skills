---
name: huawei-cloud-cost-estimation-cn
description: Generate Huawei Cloud pre-order price estimates, safely provision allowlisted resources via hcloud, and guide unsubscribe requests to the console only. Use this skill whenever the user mentions 华为云/Huawei Cloud/hcloud with 报价/询价/价格/quote/pricing/budget, 开通/购买/创建/provision/create, or 退订/unsubscribe. Create requires runtime help, --dryrun, fee review, and confirmation. Never run or emit unsubscribe CLI/API. Refuse other clouds, credentials, payment/renewal/delete, and non-allowlisted writes.
compatibility: hcloud KooCLI 7.2+, IAM permissions matching requested read/write operations, outbound network; no agent auto-install
metadata:
  language: zh-CN
  translation_of: huawei-cloud-cost-estimation
  author: concept-git
  version: "3.2.4"
  openclaw:
    requires:
      bins: [hcloud]
    primaryEnv: HUAWEICLOUD_SDK_AK
    homepage: https://github.com/concept-git/cloud-concept-skills/tree/main/skills/cn/huawei-cloud-cost-estimation-cn
    envVars:
      - {name: HUAWEICLOUD_SDK_AK, required: false}
      - {name: HUAWEICLOUD_SDK_SK, required: false}
      - {name: HUAWEICLOUD_SDK_REGION, required: false}
---

# 华为云成本估算与资源开通

> **华为社区版** · 社区维护，非华为云官方；结论以当次 hcloud 响应为准。

价格只认当次响应，**不臆造、不类比、不记忆**；仅开通可写，退订只指引官网控制台。

## Route

- **询价 / 预算 / 比价** → Pricing。
- **开通 / 购买 / 创建资源** → Lifecycle Create（仅 `references/lifecycle/commands.md` 白名单内）。
- **退订 / 停止使用资源** → Unsubscribe Guidance（仅控制台指引，不调用 CLI/API）。
- 历史账单/余额/对账 → 费用中心或 BSS 账单只读 API；非华为云 → 拒绝；白名单外写操作 → 给控制台指引。

## Execution Pace

预计不超过 3 条 `hcloud` 时直达下一安全门禁；超过 3 条时每轮只执行 2–3 条（复用/并行只读/合并询价），说明已完成与下一步并友好询问是否继续。用户要求一次完成可连续执行；澄清、未知费用、`--dryrun`、写入确认不跳过。

## Pricing

1. **Parse** — 抽取四元组 `cloud_service_type / resource_type / region / resource_spec` + 周期或使用量；读 `references/pricing/semantic/catalog.yml` 路由 period / on-demand。
2. **Clarify** — 缺 region/数量/周期或用量/线性 size，或类目模糊、多变种未定 → 停下一轮问完（2–4 候选）。仅 safe-default 缺失（OS=linux、AZ=空、`fee_installment_mode=NA`）→ 披露后继续。口语四元组确认，不暴露内部名。
3. **Query** — 按 Execution Pace 与 `references/pricing/commands.md`：
   `ListServiceResources` → `ListResourceSpecs` → 按需 `ListUsageTypes(--resource_type_code)` → Measure Resolve → 询价。
   多候选则问；Specs 命中仍可能失败；禁默认 Duration、禁容量槽/用量槽混用。
4. **Verify & Present** — 分项加和=总价；币种/周期/数量对齐。分项 `[服务] [规格] [region] [数量×周期] = ¥<金额>` + 加总 + 「非最终账单」；默认官网价，有折扣才附折后。

## Lifecycle Create

读 `references/lifecycle/concepts.md` 后按序执行，跳步即违规：

1. **Allowlist** — 意图映射到 `references/lifecycle/commands.md` 命令主体；未命中即拒绝。
2. **Help** — `hcloud <Service> <Operation> --help` 取必填/条件必填；`[APIE_ERROR]` 或无 schema 即停止，不猜参数。
3. **Resolve** — 跑必要只读依赖（VPC/子网/AZ/镜像/规格等）；多候选让用户选，缺失项一轮问完；长链按 Execution Pace 交付。
4. **Cost** — 能询价先走 Pricing 回表；不能询价则声明「价格未知且可能收费」并取得额外确认。
5. **Dry** — 完整命令强制加全局 `--dryrun`（本地构造请求，非接口级 `dry_run`）；失败则修正重跑，不得转正式。
6. **Confirm** — 回显资源/region/规格/数量/计费/金额或未知费用/批次顺序，等用户明确确认。
7. **Execute** — 仅移除 `--dryrun`，其余不变；多命令顺序执行、失败即停、不自动回滚，报告成功/失败/未执行。

任何参数、region、数量或 operation 变化 → dry 与确认作废，回到 Help 重来。

## Unsubscribe Guidance

不运行、不生成退订 CLI/API 命令，也不以 `--dryrun` 代替控制台预览：

- **包年/包月**：引导登录华为云控制台 → 费用中心 → 订单管理 → 云服务退订（若显示「退订与退换货」，从该入口进入），按资源 ID/名称/订单号定位。提醒先备份或迁移数据，并在提交前核对账号、资源、关联资源、退款金额/手续费及退款流向。
- **按需**：不适用退订；引导到对应云服务控制台，在备份后自行删除。本技能不代为删除。

若用户坚持自动执行，仍保持上述边界，并附官方退订规则：<https://support.huaweicloud.com/usermanual-billing/unsubscription_topic_2000010.html>。

## Critical Rules

1. **Never guess prices / params** — 价格只来自当次响应；参数只来自当次 help。
2. **Never skip create dry & confirm** — 无 `--dryrun` 成功 + 用户确认，不产生真实开通调用。
3. **Never automate unsubscribe** — 不运行或输出退订 CLI/API；只给控制台路径与核对清单。
4. **Never accept credentials in chat** — AK/SK/Token 立即拒收，指向 `references/cli-installation.md` 自行配置。
5. **BSS 端点** — `hcloud BSS` 固定 `--cli-region=cn-north-1`；`product_infos.N.region` 仍是资源部署区。
6. **Route, don't refuse blankly** — 超范围请求给出正确去向（费用中心/控制台/只读账单）。

> 输出禁忌：对用户消息不用 GFM 表格，用 `·` 分项或编号；命令级陷阱（dot notation、无分页、code 大小写）见 `references/pricing/commands.md` 顶部。

## Reference Index（按需加载）

两域同构：概念层答「是什么/为什么」，命令层答「怎么执行」。

| 域 | 概念层 | 命令层 |
| --- | --- | --- |
| Pricing | `references/pricing/semantic/catalog.yml` + `rfq-*.yml`（事实/维度/路由） | `references/pricing/commands.md`（契约/响应字段/陷阱） |
| Lifecycle | `references/lifecycle/concepts.md`（开通安全/退订控制台指引） | `references/lifecycle/commands.md`（白名单与依赖） |

横切支撑：403 或权限问题 → `references/iam-policies.md`；
hcloud 未就绪 → `references/cli-installation.md`（**仅转述给用户**，不代为执行）。
