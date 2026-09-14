# 华为云成本估算与资源开通

`huawei-cloud-cost-estimation` · **Huawei Cloud Cost Estimation & Controlled Provisioning — Quote, Create, Console-Guided Unsubscribe**

Deterministic pre-order quotes via hcloud BSS (`ListServiceResources` → `ListResourceSpecs` → on-demand `ListUsageTypes` → `ListMeasureUnits`+Measure Resolve → period/on-demand RFQ) plus 74 controlled create operations. Small chains complete directly; larger chains stage 2–3 commands unless the user asks end-to-end. Creates require runtime `--help`, fee review, local `--dryrun`, and confirmation. Unsubscribe is console-guidance-only.

> **华为社区版** · 社区维护，非华为云官方；结论以当次 hcloud 响应为准。

**Version:** 3.2.4 · Changelog: [qa/huawei-cloud-cost-estimation/CHANGELOG.md](../../qa/huawei-cloud-cost-estimation/CHANGELOG.md) · 中文仓库说明：[README-CN.md](../../README-CN.md)

## What it does

| Capability | Typical requests |
| --- | --- |
| Period / on-demand RFQ | 包年包月、按小时/按量多少钱；多产品分项加总 |
| Spec & dimension lookup | `ListServiceResources` / `ListResourceSpecs` / 按需 `ListUsageTypes` / Measure Resolve |
| Controlled create | 开通/购买白名单内资源（ECS/RDS/CCE/CloudIDE/WAF 等 74 个命令主体） |
| Console-guided unsubscribe | 包年/包月前往费用中心核对退款与关联资源；按需前往云服务控制台自行删除 |
| Out of scope | 历史账单/余额/对账 → 费用中心或只读账单 API；跨云；支付/续费/删除；对话中 AK/SK |

Independent from [huawei-cloud-billing-scout](huawei-cloud-billing-scout.md) (past spend)—install either or both; skills do not cross-route.

## Runtime bundle (install payload)

```text
skills/huawei-cloud-cost-estimation/
├── SKILL.md                     # route + pricing flow + lifecycle gates
└── references/
    ├── cli-installation.md      # cross-cutting: CLI readiness (user-run only)
    ├── iam-policies.md          # cross-cutting: read layers + create write principle + 403
    ├── pricing/
    │   ├── semantic/            # concept layer: catalog + rfq-{period,ondemand,shared}
    │   └── commands.md          # command layer: RFQ contracts, response paths, traps
    └── lifecycle/
        ├── concepts.md          # concept layer: create gates + unsubscribe guidance
        └── commands.md          # command layer: 74 create ops, bodies only
```

No `evals/`, `qa/`, or `*-workspace/` under `skills/`.

## In-skill flow

```text
User request
     │
     ├─ Execution Pace ─► ≤3 direct · >3 staged with a continue prompt
     │
     ├─ Quote ──► catalog → resource_type → specs → (on-demand usage_factor) → RFQ → present
     │
     ├─ Create ─► allowlist → runtime --help → resolve deps (read-only)
     │            → cost echo (quote or unknown-fee extra confirm)
     │            → mandatory --dryrun → batch echo + explicit confirm
     │            → execute (remove --dryrun only) · fail-fast · no auto-rollback
     │
     └─ Unsubscribe ─► no CLI/API → official console path
                       → backup + resource/association/refund review
```

Parameters are never stored in the skill: each write op is explored with `hcloud <Service> <Operation> --help` at run time; if help fails (`[APIE_ERROR]`), the flow stops. Local `--dryrun` (prints the request, skips the call) is distinct from the server-side `dry_run` parameter a few APIs offer.

## Safety boundary

```text
Allowed: BSS RFQ/dictionary reads; read-only dependency lookups;
         74 allowlisted create ops behind --dryrun + fee echo + confirmation
Refused: chat AK/SK intake, payment, renewal, refund, delete,
         unsubscribe CLI/API, non-allowlisted writes, cross-cloud
Guided:  package unsubscribe → Billing Center; on-demand cleanup → service console
```

Create evals stop at `--dryrun`; unsubscribe evals enforce console-only guidance. Real provisioning tests are manual. Evidence snapshot: [docs/hcloud/evidence/normative-allowlist.md](../hcloud/evidence/normative-allowlist.md).

## QA (not installed with skill)

```text
qa/huawei-cloud-cost-estimation/
├── validate.sh                  # layout, version sync, create allowlist + unsubscribe boundary
├── fixtures/ops_contracts.yml   # 74 create ops + forbidden destructive op
├── evals/evals.json             # 19 offline cases (19 covers progressive execution)
├── assertions/README.md
└── bin/                         # grade_response.py, run_ab_eval.py, aggregate_ab.py
```

```bash
./qa/huawei-cloud-cost-estimation/validate.sh
```

## Marketplaces

- ClawHub: `huawei-cloud-cost-estimation` 3.2.4; bundle license MIT-0

## Install

[![skills.sh](https://skills.sh/b/concept-git/cloud-concept-skills)](https://skills.sh/concept-git/cloud-concept-skills)

```bash
npx skills add concept-git/cloud-concept-skills \
  --skill huawei-cloud-cost-estimation \
  --agent cursor \
  --copy -y
```

**Hermes:** [hermes.md](../agents/hermes.md) · local sync:

```bash
rsync -a --delete ./skills/huawei-cloud-cost-estimation/ ~/.hermes/skills/huawei-cloud-cost-estimation/
```

Requires hcloud ≥7.2 and IAM permissions matching the requested read/write operations. Agent does not auto-install `hcloud`.
