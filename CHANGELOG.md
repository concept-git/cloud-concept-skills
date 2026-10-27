# Changelog

## 1.4.0 - 2026-10-27

### Fixes
- Align English and Chinese skill versions with the next ClawHub patch releases: cost estimation 3.2.7, billing scout 2.3.11, and account onboarding 1.0.3.
- Complete the cost-estimation English runtime translation and shorten its workflow. Keep pricing inputs in shared RFQ fields plus billing-mode models, with reference and locale checks.
- Separate CLI readiness checks from billing, identity and pricing queries; preserve dotted pricing arguments and region/billing-mode specification matching.
- Document the verified OBS unit mapping, account-type meanings and missing-account handling. Limit real-name results to verification status and type.
- Require evidence for quote units, subtotals and commercial terms; retain the existing provisioning confirmation gates.

### Validation and known limitations
- Public package, locale and RFQ checks pass. Private Piagent evaluation covered one eight-turn workflow and seven targeted follow-up turns using read-only cloud calls; it is not an exhaustive behavioral guarantee.
- ELB capacity/unit applicability remains unresolved: Piagent still inferred values and included the returned amount in a subtotal. Quotes containing that line require review before formal delivery.
- Cost-estimation runtime prose is fully English; billing reference files retain legacy Chinese prose. This release aligns the changed bilingual rules, not a complete translation of every skill reference.

## 1.3.0 - 2026-10-24

- Retain three bilingual Huawei Cloud capabilities and the active FCAPS diagnostics draft with its validation contracts.
- Clarify marketplace descriptions, categories and topics.
- Standardize repository ownership and directory rules; remove source-study archives, logs and temporary workspaces.
- Keep reproducible command evidence and required runtime references; block local-only files in commits, pushes and CI.
