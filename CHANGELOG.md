# Changelog

## 1.8.0 - 2026-11-04

### Fixes
- Answer simple FCAPS knowledge questions directly when reliable information is already available. Query tools or the knowledge base only when needed, and stop once the evidence is sufficient. (by @AgenticWeb4)

### Documentation
- Use plain Chinese for diagnostic instructions, investigation reports and evidence checks. Add patient listening and considerate, understandable replies to the Huawei Cloud SRE role. (by @AgenticWeb4)

## 1.7.0 - 2026-11-03

### Fixes
- Clarify investigation in the FCAPS diagnostics draft: handle simple questions directly, delegate independent investigations in parallel, sequence dependent checks, and let the main agent continue investigation and explanation when subagents are unavailable. (by @AgenticWeb4)
- Make follow-up steps conditional on remaining work across diagnostic completion, explanation, and output requirements; allow completed tasks to conclude without unnecessary extra steps. (by @AgenticWeb4)

### Documentation
- Clarify the draft's Huawei Cloud SRE role and remove automatic KCS revision or article drafting from diagnostic completion. (by @AgenticWeb4)

## 1.6.0 - 2026-11-03

### Features
- Expand the FCAPS diagnostics draft with staged investigation, scoped parallel exploration, hypothesis checks, mitigation and recovery verification, evidence-backed handoffs, and action logs. Require approval of a concrete plan before on-site changes. The draft remains under `development/`, outside the installable catalog. (by @AgenticWeb4)

### Fixes
- Synchronize both billing scout editions at 2.3.12 for the existing account-selection clarification: establish Huawei Cloud/BSS billing context and the intended account from the request or conversation, reuse an unambiguous account choice, and ask only while the target remains ambiguous. Billing remains read-only. (by @AgenticWeb4)

### Documentation
- Align the English and Chinese README version tables with billing scout 2.3.12 and cost estimation 3.3.0. (by @AgenticWeb4)

## 1.5.0 - 2026-10-28

### Features
- Improve bilingual cost-estimation guidance for pricing evidence, provisioning checks, order outcomes and credential handling.
- Add KCS Foundry with the OpenKB upstream source snapshot and provenance.

### Improvements
- Reorganize the FCAPS diagnostics draft and its KCS recipes.
- Add validation for estimation gotchas and context budgets.

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
