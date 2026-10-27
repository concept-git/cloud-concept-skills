# IAM least privilege

IAM actions vary with account type, site, and service version. Verify them through API Explorer and current `hcloud <Service> <Operation> --help`. If permissions are insufficient, ask the user to have an administrator grant them. Do not add write permissions to repair a failed query or elevate privileges yourself.

## Pricing: read-only

| Layer | Operations | Purpose |
| --- | --- | --- |
| BSS pricing | `ListRateOnPeriodDetail`, `ListOnDemandResourceRatings` | Yearly/monthly or pay-per-use quotes |
| BSS dictionaries | `ListServiceTypes`, `ListResourceTypes`, `ListServiceResources`, `ListResourceSpecs`, `ListMeasureUnits`, `ListConversions` | Resolve services, resources, specifications, and measures |
| Product support | `ECS/NovaListAvailabilityZones` | When the user specifies an AZ |
| Identity scope | `IAM/KeystoneListAuthProjects`, `IAM/KeystoneListProjects` | Resolve accessible projects |

A common pricing policy is `bss:order:view` plus the corresponding read-only BSS/IAM actions.

## Provisioning: writes

Write permissions follow the service that owns the allowlisted operation; for example, `ECS/CreateServers` requires the corresponding ECS write actions. Dependency queries need only their read actions. This reference does not enumerate every service's write actions: use the action in the current 403 message and API Explorer, and ask the user's administrator to grant it.

## Partner quotes on behalf of a customer

Use the customer-authorized token with `KeystoneListAuthProjects` to resolve the customer's project for the target region, then request pricing. Stop on authorization failure; do not broaden the scope.

## Permission and rate-limit failures

| Symptom | Action |
| --- | --- |
| `403 Forbidden` / `CBC.0151` | Record operation and account scope; recommend the relevant action, read-only for pricing |
| `429` | Wait two seconds and retry once; stop if it still fails |

For parameter errors such as `CBC.0100`, `CBC.99006006`, and `CBC.99006055`, see `pricing/commands.md`. Historical bills, balances, and reconciliation are outside this skill; use Cost Center or the separate read-only billing skill.
