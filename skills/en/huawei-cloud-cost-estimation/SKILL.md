---
name: huawei-cloud-cost-estimation
description:
  Generates Huawei Cloud pre-order estimates, provisions allowlisted resources through hcloud, and
  routes unsubscribe requests to console guidance. Use for Huawei Cloud pricing, budgets, creation,
  provisioning, or unsubscribe. Creates require runtime help, --dryrun, fee review, and
  confirmation. Never emits or runs unsubscribe operations, accepts credentials, or performs
  non-allowlisted writes.
compatibility:
  hcloud KooCLI 7.2+, matching IAM permissions, and outbound network; the agent does not install
  dependencies
metadata:
  language: en
  translation_of: huawei-cloud-cost-estimation-cn
  author: concept-git
  version: "3.2.4"
  openclaw:
    requires:
      bins: [hcloud]
    primaryEnv: HUAWEICLOUD_SDK_AK
    homepage: https://github.com/concept-git/cloud-concept-skills/tree/main/skills/en/huawei-cloud-cost-estimation
    envVars:
      - { name: HUAWEICLOUD_SDK_AK, required: false }
      - { name: HUAWEICLOUD_SDK_SK, required: false }
      - { name: HUAWEICLOUD_SDK_REGION, required: false }
---

# Huawei Cloud Cost Estimation and Provisioning

> Community edition, not an official Huawei Cloud skill. Treat the current hcloud response as
> authoritative.

Prices come only from the current response: never guess, analogize, or recall them. Provisioning is
the only permitted write path; unsubscribe is console guidance only.

## Route

- Quote, budget, or comparison → Pricing.
- Provision, purchase, or create → Lifecycle Create, limited to `references/lifecycle/commands.md`.
- Unsubscribe or stop using → console-only Unsubscribe Guidance.
- Historical bills, balance, or reconciliation → Cost Center or read-only BSS billing; other clouds
  → refuse; non-allowlisted writes → console guidance.

## Execution Pace

Complete chains of at most three hcloud commands directly to the next safety gate. For longer
chains, run only two or three commands per round, report progress and the next step, then ask
whether to continue. A user may request uninterrupted execution, but clarification, unknown-cost
approval, `--dryrun`, and write confirmation remain mandatory.

## Pricing

1. **Parse** `cloud_service_type / resource_type / region / resource_spec` plus period or usage;
   route through `references/pricing/semantic/catalog.yml`.
2. **Clarify** missing region, quantity, duration/usage, linear size, ambiguous categories, or
   unresolved variants in one question with two to four candidates. Disclose and apply only safe
   defaults: OS=linux, empty AZ, and `fee_installment_mode=NA`.
3. **Query** using `references/pricing/commands.md`: `ListServiceResources` → `ListResourceSpecs` →
   on-demand `ListUsageTypes(--resource_type_code)` → measure resolution → quotation. Ask on
   multiple matches; a spec match may still fail. Never invent duration or mix capacity and usage
   slots.
4. **Verify and present** that line items sum to the total and currency, period, and quantity align.
   Present `[service] [spec] [region] [quantity × period] = amount`, total, and “not a final bill.”
   Show discounts only when returned.

## Lifecycle Create

Read `references/lifecycle/concepts.md`, then perform every gate in order:

1. **Allowlist** — Map intent to an operation in `references/lifecycle/commands.md`; refuse misses.
2. **Help** — Run `hcloud <Service> <Operation> --help` for required and conditional fields. Stop on
   `[APIE_ERROR]` or missing schema; never guess.
3. **Resolve** — Run required read-only dependencies such as VPC, subnet, AZ, image, and flavor. Let
   the user choose among multiple matches.
4. **Cost** — Use Pricing when possible. Otherwise disclose “price unknown and may incur charges”
   and obtain separate approval.
5. **Dry** — Add global `--dryrun` to the complete command. Fix and rerun failures; never promote a
   failed dry run.
6. **Confirm** — Show resource, region, spec, quantity, billing, known or unknown price, and batch
   order; wait for explicit confirmation.
7. **Execute** — Remove only `--dryrun`. Run multiple commands in order, stop on failure, never
   auto-rollback, and report succeeded, failed, and unexecuted items.

Any parameter, region, quantity, or operation change invalidates the dry run and confirmation and
returns to Help.

## Unsubscribe Guidance

Never run or generate unsubscribe CLI/API operations, and never use `--dryrun` as a substitute for
console preview.

- **Subscription resources:** direct the user to Huawei Cloud Console → Cost Center → Orders →
  Unsubscriptions. Ask them to back up or migrate data and verify the account, resource, related
  resources, refund, fees, and refund destination before submission.
- **Pay-per-use resources:** unsubscribe does not apply. Direct the user to the service console to
  delete the resource after backup; do not delete it for them.

If automation is requested, preserve this boundary and provide the
[official unsubscribe rules](https://support.huaweicloud.com/usermanual-billing/unsubscription_topic_2000010.html).

## Critical Rules

1. Prices come from the current response; parameters come from current help.
2. No real create call without a successful `--dryrun` and explicit confirmation.
3. Never automate or emit unsubscribe operations.
4. Refuse AK, SK, and tokens in chat; point to `references/cli-installation.md` for
   self-configuration.
5. Every BSS call uses `--cli-region=cn-north-1`; `product_infos.N.region` remains the deployment
   region.
6. Route out-of-scope work to Cost Center, the appropriate console, or read-only billing.

Use bullets or numbered items, not GFM tables, in user-facing responses. For command-level traps,
read `references/pricing/commands.md`.

## Reference Index

| Domain    | Concepts                                                  | Commands                           |
| --------- | --------------------------------------------------------- | ---------------------------------- |
| Pricing   | `references/pricing/semantic/catalog.yml` and `rfq-*.yml` | `references/pricing/commands.md`   |
| Lifecycle | `references/lifecycle/concepts.md`                        | `references/lifecycle/commands.md` |

For 403 or permission failures, read `references/iam-policies.md`. If hcloud is unavailable, relay
`references/cli-installation.md`; never install it for the user.
