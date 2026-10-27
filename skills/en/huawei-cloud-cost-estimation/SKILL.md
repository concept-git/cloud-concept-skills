---
name: huawei-cloud-cost-estimation
description: >-
  Estimate Huawei Cloud pre-order costs, provision allowlisted resources through
  hcloud, and guide unsubscribe requests through the console. Use for Huawei Cloud
  pricing, budgets, resource creation, unsubscribe guidance, or hcloud readiness checks.
compatibility:
  hcloud KooCLI 7.2+, matching IAM permissions, and outbound network; the agent does not install
  dependencies
metadata:
  language: en
  translation_of: huawei-cloud-cost-estimation-cn
  author: concept-git
  version: "3.2.7"
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

# Huawei Cloud Quotes and Resource Provisioning

Community-maintained, not an official Huawei Cloud skill. Use current hcloud responses for prices and status, and current command help for parameters.

## Choose the workflow

- hcloud readiness: read the readiness section of `references/cli-installation.md` and report only the capabilities checked.
- Quotes, budgets, or price comparisons: follow Pricing.
- Purchases or resource creation: follow Provisioning.
- Unsubscribe or stop using a resource: follow the console guidance in `references/lifecycle/concepts.md`. Never generate or execute unsubscribe commands.
- Historical bills, balances, or reconciliation: route to Cost Center or a read-only billing skill. For other clouds or operations outside the allowlist, explain the scope and point to the appropriate console.

## Pricing

Read `references/pricing/commands.md`, then:

1. **Clarify the request.** Establish service, region, specification, quantity, billing mode, and period or usage; include capacity where the product requires it. Ask about missing inputs and materially different candidates together. If the user delegates selection, choose against their budget and purpose and explain the choice. For quotes only, disclose before using Linux, an empty AZ, or installment mode NA. Do not default the billing mode or duration.
2. **Find the matching specification.** Query resource types for the service, then specifications for the selected region and billing mode. Preserve the candidate's service type, resource type, region, charge mode, and specification code. Identical names do not permit reuse across regions or modes. For pay-per-use, also resolve the usage factor and unit. Follow the pricing reference for capacity and pagination.
3. **Query and check.** Use the appropriate period or pay-per-use pricing API. Match the selected specification, period or usage, quantity, and capacity. If a product's capacity or unit meaning remains unresolved, stop pricing that line and mark it unverified. Keep returned facts, errors, and hypotheses separate; an amount alone establishes neither a verified quote nor provisionability.
4. **Explain the quote.** Itemize service, specification, region, billing mode, quantity × period or usage, and amount. Check totals, currency, and exclusions. Show only returned discounts and state that this is not a final bill. Only rows with verified configuration, billing units, and response contribute to the verified subtotal. Keep unverified rows outside it even if they returned an amount; do not present a partial subtotal as the complete budget. Apply the quote-delivery rules in the pricing reference.

## Provisioning

Read `references/lifecycle/concepts.md` and `references/lifecycle/commands.md`, then complete these steps in order:

1. **Check the operation.** Confirm that it is allowlisted and run its current `--help`. Stop if help fails or lacks parameter definitions.
2. **Check the configuration.** Use read-only APIs to verify the target region, AZ, specification sales status and billing support, account restrictions, and image, network, and other dependencies. Finding a specification or price is only part of this check; do not call it available inventory.
3. **Check the cost.** Quote the complete proposed configuration, including associated paid resources. If a reliable price is unavailable, disclose that the price is unknown and charges may apply, and obtain separate consent. This does not replace provisioning checks.
4. **Check the request.** Add global `--dryrun` to the complete command and inspect the constructed request. Correct failures first. Success establishes only that the request can be constructed locally.
5. **Confirm and execute.** Show the configuration, quantity, billing mode, period, cost, and execution order. Obtain explicit confirmation for that configuration. Make the real call separately, removing only `--dryrun`. Execute batches in order; stop writes on failure and report each item's status.

A configuration change requires fresh checks, pricing, dry run, and confirmation. After a create failure, investigate read-only; do not try successive flavors through real create calls or automatically roll back. A task or order ID means accepted, not completed: use read-only queries to establish the final status.

## Communication and supporting references

Use natural Chinese in user-facing replies: give the conclusion, evidence, and next step in that order. Prefer short paragraphs and itemized details; honor a requested format. Complete clear read-only steps without repeated permission questions and briefly report progress during longer work. Pause for missing decision-relevant inputs or the required cost and write confirmations.

Every BSS call uses `--cli-region=cn-north-1`; the resource's deployment region remains the user's selected region. Do not accept AK, SK, or tokens in chat, or expose credentials in output or logs.

- hcloud unavailable or configuration needed: read `references/cli-installation.md` and have the user configure it.
- Permission errors such as 403: read `references/iam-policies.md`.
- Field relationships unclear: read `references/pricing/rfq-models/rfq-core.yml` and the model for the current billing mode; for shared-dimension lookup, read only the core.
