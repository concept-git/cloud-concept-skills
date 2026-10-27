# Provisioning checks and failure handling

Allowed writes are listed in `commands.md`. This reference defines checks; obtain parameters from current `hcloud <Service> <Operation> --help`. Stop if help fails, the operation does not exist, or parameter definitions are missing.

## What each kind of evidence establishes

- BSS directory match: a pricing specification exists for the requested service, resource type, region, and billing mode.
- Successful BSS quote: the current inputs produced a price. Capacity, units, and included billing items must still match the intended configuration.
- Service-side checks: inspect sales status, billing support, account restrictions, and dependency compatibility. Passing permits the statement that current availability checks passed, not a guarantee of successful creation.

Retain pricing specification codes and creation flavor IDs separately, checking their mapping. Adding or removing suffixes does not replace a service-side lookup.

## Read-only ECS checks

Read current `ECS/ListFlavors` help, then query the target flavor and AZ. Preserve `id`, CPU, memory, and relevant `os_extra_specs`.

1. **Sales status.** Use the target AZ's entry in `cond:operation:az` when present; otherwise use regional `cond:operation:status`. `normal/promotion` means commercially available, `abandon` means retired, `sellout` means sold out, and `obt/obt_sellout` concerns public beta. Apply documented defaults; regional `abandon` must not override AZ-level `normal`.
2. **Billing support.** Check `cond:operation:charge`: `period` means yearly/monthly and `demand` means pay-per-use. The documented default, when absent, supports both. Where further sales-policy evidence is needed, use `ListFlavorSellPolicies` within the current help and response capabilities. Verify returned flavor, AZ, `sell_mode`, and `sell_status`; a CLI enum does not prove every mode is supported by the service.
3. **Account and dependencies.** Check beta or role restrictions, queryable quotas, image architecture and status, network and subnet constraints, and supported disk types. Preserve fields needed to judge compatibility instead of keeping names alone.

Stop for explicit lack of support, sold-out status, or permission restrictions. Disclose conditions that current read-only APIs cannot establish; do not call them available inventory. Use each other service's own product or flavor APIs, not ECS-specific fields.

Source: [ECS flavor extension fields](https://support.huaweicloud.com/api-ecs/zh-cn_topic_0020212656.html). Interpret fields through the official definitions and take current status from the current response.

## Costs and request checks

Classify cost as reliably quoted for the complete current configuration, unverified, or evidenced as not independently billable. Include associated resource costs. For unverified cost, disclose that the price is unknown and charges may apply, and obtain separate consent. This cannot bypass a known incompatibility or permission restriction.

Global `--dryrun` constructs the request locally without calling the business API. It does not validate inventory, permissions, or order acceptance. Some services also have request-level `dry_run/dryRun` parameters that call the service; these differ from the global option.

Run the complete command with `--dryrun` and inspect the constructed request and output. Correct failures and repeat the check. Run the real call separately: do not unconditionally chain it after a dry run or let a successful pipeline tail mask an earlier failure.

The user confirms the displayed configuration, costs, and batch order. Remove only `--dryrun` for the real call. Changing flavor, region, AZ, image, network, disk, quantity, billing mode, period, or operation requires fresh checks, pricing, dry run, and confirmation.

## After a create failure

Stop subsequent writes immediately. Preserve the error and request association, then investigate read-only. Do not cycle through flavors, images, or AZs using real create calls, or automatically roll back. A new proposal supported by evidence must complete the full workflow.

If a request times out or its outcome is unclear, inspect order, task, or resource state before risking duplicate creation. An order or task ID means accepted, not completed. Query its final state read-only; report successful, failed, unexecuted, and still-unverified batch items separately.

Explain `Ecs.0016` beta-permission errors and `Ecs.0019` retired-flavor errors from their actual messages. An `Ecs.0707` product-not-found error alone does not establish a network or site root cause.

## Unsubscribe and stop using

Do not generate or run unsubscribe CLI/API operations, or substitute a local dry run for the console preview.

- Yearly/monthly: Huawei Cloud Console → Cost Center → Orders → Unsubscriptions. If the UI labels the entry Unsubscriptions and Returns, use that entry.
- Pay-per-use: direct the user to the relevant service console to delete the resource themselves after backup. This skill does not delete it.

Before submission, remind the user to back up or migrate data and check account, resource, related resources, refund amount, fees, and refund destination. Follow the console and [official unsubscription rules](https://support.huaweicloud.com/usermanual-billing/unsubscription_topic_2000010.html).
