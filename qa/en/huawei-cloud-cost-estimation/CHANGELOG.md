# huawei-cloud-cost-estimation Changelog

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../../CHANGELOG.md).

## 3.2.4 - 2026-08-24

### Changed

- Promote `pricing/iam-policies.md` → `references/iam-policies.md` (cross-cutting, serves both domains): add create-side write-permission principle (write Action follows the allowlisted op's service; no per-service enumeration; report 403 instead of self-escalating); keep RFQ read-only layers
- Move parameter errors (`CBC.0100`/`CBC.99006006`/`CBC.99006055`) from iam-policies to `pricing/commands.md` traps; iam-policies now covers permission/throttle only (403/`CBC.0151`/429)
- SKILL.md Reference Index restructured as concept-layer/command-layer symmetry per domain (Pricing `semantic/*.yml` + `commands.md`; Lifecycle `concepts.md` + `commands.md`); cross-cutting docs listed separately
