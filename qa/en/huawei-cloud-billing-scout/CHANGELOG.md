# huawei-cloud-billing-scout Changelog

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../../CHANGELOG.md).

## 2.3.9 - 2026-06-02

### Added

- **SKILL.md**: BSS 端点规则 — 所有 `hcloud BSS` 固定 `--cli-region=cn-north-1`；勿用 profile 默认区
- **eval #25** `bss-cli-region-not-profile-default` + `protocol_grading.py` cli-region 断言；真实 hcloud A/B 验证
- **qa**: A/B harness — `bin/run_ab_eval.py`, `grade_response.py`, `aggregate_ab.py`; `assertions/README.md` documents Skill Creator workflow

### Changed

- **semantic**: thin `billing-ontology.yml` / `catalog.yml` (facts, grain, `source_operations` only; investigation flow in SKILL.md)
- **gate**: `gate.py full` runs `smoke_real_bss.py` when `HUAWEICLOUD_BILLING_SCOUT_REAL=1`
