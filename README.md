# Huawei Cloud Agent Skills

[![skills.sh](https://skills.sh/b/concept-git/cloud-concept-skills)](https://skills.sh/concept-git/cloud-concept-skills)

Community-maintained Huawei Cloud skills for billing analysis, pre-order cost estimation and
controlled provisioning, and account real-name onboarding. Three capabilities ship as six localized
skills: English uses the base name and Simplified Chinese adds `-cn`. This project is not an
official Huawei Cloud product.

Published skills keep their runtime payload under `skills/productivity/<locale>/<name>/`; QA and evaluations remain private on the maintainer's machine and are not committed or installed.

中文说明见 [README-CN.md](README-CN.md).

## Directory layout

All four categories live under `skills/`.

| Directory | Purpose |
| --- | --- |
| `skills/engineering/` | Engineering skills. Reserved for future additions. |
| `skills/drafts/` | Draft skills and projects, including FCAPS diagnostics and KCS Foundry. |
| `skills/productivity/` | Published billing, cost-estimation, and account-onboarding skills in English and Simplified Chinese. |
| `skills/misc/` | Other skills. Reserved for future additions. |

`skills.sh.json` lists the published skill containers for installer discovery. Drafts remain outside the public catalog and default installation list.

## Skills

| English | 中文 | Version | Purpose |
| --- | --- | --- | --- |
| [`huawei-cloud-billing-scout`](skills/productivity/en/huawei-cloud-billing-scout/SKILL.md) | [`huawei-cloud-billing-scout-cn`](skills/productivity/zh-CN/huawei-cloud-billing-scout-cn/SKILL.md) | 2.3.12 | Read-only billing analysis and reconciliation. |
| [`huawei-cloud-cost-estimation`](skills/productivity/en/huawei-cloud-cost-estimation/SKILL.md) | [`huawei-cloud-cost-estimation-cn`](skills/productivity/zh-CN/huawei-cloud-cost-estimation-cn/SKILL.md) | 3.3.0 | Current-response quotes and guarded provisioning. |
| [`huawei-cloud-account-onboarding`](skills/productivity/en/huawei-cloud-account-onboarding/SKILL.md) | [`huawei-cloud-account-onboarding-cn`](skills/productivity/zh-CN/huawei-cloud-account-onboarding-cn/SKILL.md) | 1.0.3 | Read-only real-name status and face-scan guidance. |

Discovery metadata: [catalog.yml](catalog.yml).

## In development

[`huawei-cloud-fcaps-diagnostics`](skills/drafts/huawei-cloud-fcaps-diagnostics/README.md)
contains verified diagnostic command contracts and resource helpers for Huawei Cloud
ECS and related services. Recipes remain planned. It stays under `skills/drafts/`
and is not published as an installable skill.

[`kcs-foundry`](skills/drafts/kcs-foundry/README.md) contains the KCS knowledge-extraction project and its OpenKB upstream source snapshot.

## Install

Requires Node.js 22.20+ and Git. Copy a command below and run it from your project directory. These commands install to Codex in the current project.

Running the cloud skills also requires [KooCLI](https://support.huaweicloud.com/intl/en-us/productdesc-hcli/hcli_01.html) 7.2+; the skills do not install it automatically.

Use `--agent claude-code` or `--agent cursor` for another agent; add `--global` to install across projects. See the [installer options](https://github.com/vercel-labs/skills/blob/main/docs/commands.md).

### English editions

```bash
npx --yes skills add concept-git/cloud-concept-skills --skill huawei-cloud-billing-scout huawei-cloud-cost-estimation huawei-cloud-account-onboarding --agent codex --copy --yes
```

### Simplified Chinese editions

```bash
npx --yes skills add concept-git/cloud-concept-skills --skill huawei-cloud-billing-scout-cn huawei-cloud-cost-estimation-cn huawei-cloud-account-onboarding-cn --agent codex --copy --yes
```

### Install one skill

**`huawei-cloud-billing-scout`**

```bash
npx --yes skills add concept-git/cloud-concept-skills --skill huawei-cloud-billing-scout --agent codex --copy --yes
```

**`huawei-cloud-cost-estimation`**

```bash
npx --yes skills add concept-git/cloud-concept-skills --skill huawei-cloud-cost-estimation --agent codex --copy --yes
```

**`huawei-cloud-account-onboarding`**

```bash
npx --yes skills add concept-git/cloud-concept-skills --skill huawei-cloud-account-onboarding --agent codex --copy --yes
```

### List available skills

```bash
npx --yes skills add concept-git/cloud-concept-skills --list
```

English payloads live in `skills/productivity/en/`; Simplified Chinese payloads live in `skills/productivity/zh-CN/` and keep the `-cn` skill names. ClawHub publishes English editions only.

Billing and onboarding remain read-only. Provisioning follows the skill allowlist, cost review, and confirmation gates; unsubscribe is console-guided only.

## Contributing

`qa/` is private and untracked; public checks do not depend on it. Run `./tools/validate-all.sh --local-qa` only when local QA is available.

Project rules and repository ownership: [CLAUDE.md](CLAUDE.md).

```bash
./tools/validate-all.sh
```

## License

[Apache-2.0](LICENSE) © cloud-concept-skills contributors. Bundles published to ClawHub are MIT-0
there; repository source remains Apache-2.0.
