# Cloud Operations & Automation Skills

[![skills.sh](https://skills.sh/b/concept-git/cloud-concept-skills)](https://skills.sh/concept-git/cloud-concept-skills)

Community-maintained skills for Huawei Cloud operations. Published skills cover billing, cost estimation, and account onboarding. Draft diagnostics and knowledge extraction stay in the repository. Frontend design and website checks come in as Git submodules.

These skills are not an official Huawei Cloud product.

中文：[README-CN.md](README-CN.md)

## Published skills

English uses the base name. Simplified Chinese adds `-cn`.

| English | 中文 | Version | Purpose |
| --- | --- | --- | --- |
| [`huawei-cloud-billing-scout`](skills/productivity/en/huawei-cloud-billing-scout/SKILL.md) | [`huawei-cloud-billing-scout-cn`](skills/productivity/zh-CN/huawei-cloud-billing-scout-cn/SKILL.md) | 2.3.12 | Read-only billing analysis and reconciliation. |
| [`huawei-cloud-cost-estimation`](skills/productivity/en/huawei-cloud-cost-estimation/SKILL.md) | [`huawei-cloud-cost-estimation-cn`](skills/productivity/zh-CN/huawei-cloud-cost-estimation-cn/SKILL.md) | 3.3.0 | Current-response quotes and guarded provisioning. |
| [`huawei-cloud-account-onboarding`](skills/productivity/en/huawei-cloud-account-onboarding/SKILL.md) | [`huawei-cloud-account-onboarding-cn`](skills/productivity/zh-CN/huawei-cloud-account-onboarding-cn/SKILL.md) | 1.0.3 | Read-only real-name status and face-scan guidance. |

Index: [catalog.yml](catalog.yml).

Billing and onboarding are read-only. Provisioning stays inside the skill allowlist, cost review, and confirmation gates. Unsubscribe is console guidance only.

## Install

Node.js 22.20+, Git, and [KooCLI](https://support.huaweicloud.com/intl/en-us/productdesc-hcli/hcli_01.html) 7.2+. The skills do not install KooCLI.

Run from the project directory. This installs into Codex for that project. `--agent claude-code` or `--agent cursor` selects another agent. `--global` installs for every project. [Installer options](https://github.com/vercel-labs/skills/blob/main/docs/commands.md).

English:

```bash
npx --yes skills add concept-git/cloud-concept-skills --skill huawei-cloud-billing-scout huawei-cloud-cost-estimation huawei-cloud-account-onboarding --agent codex --copy --yes
```

Simplified Chinese: the same command with `huawei-cloud-billing-scout-cn huawei-cloud-cost-estimation-cn huawei-cloud-account-onboarding-cn`.

One skill: replace that list with one name. List the skills: `npx --yes skills add concept-git/cloud-concept-skills --list`.

Payloads: `skills/productivity/en/`, `skills/productivity/zh-CN/`. ClawHub publishes English only.

## Layout

| Directory | Purpose |
| --- | --- |
| `skills/productivity/` | The six published skills above. |
| `skills/drafts/` | Drafts. Not in the public catalog or the default install list. |
| `skills/misc/` | Other projects, including the two submodules below. |
| `skills/engineering/` | Reserved. |

`skills.sh.json` lists published skills for the installer.

## Related projects

[skills-list](https://github.com/daoxianglaonong/skills-list) is at `skills/misc/frontend-design/skills-list/`: page themes, responsive design, and design audits.

[MetaPQP](https://github.com/vi-vi-vi-vi-vivian/MetaPQP) is at `skills/misc/web-quality/MetaPQP/`: website experience checks and page comparisons.

After clone: `git submodule update --init`.

## In development

[`directory-summary`](skills/drafts/directory-summary/SKILL.md) writes `.abstract.md` and `.overview.md` for a directory from the files already there.

[`huawei-cloud-fcaps-diagnostics`](skills/drafts/huawei-cloud-fcaps-diagnostics/README.md) has verified diagnostic command contracts and resource helpers for Huawei Cloud ECS and related services. The recipes are drafts and have not passed end-to-end validation. It is not an installable skill.

[`kcs-foundry`](skills/drafts/kcs-foundry/README.md) holds the KCS knowledge-extraction project and an OpenKB source snapshot.

## Contributing

`qa/` is private and untracked. Public checks do not use it. Run `./tools/validate-all.sh --local-qa` only when local QA is present.

Rules: [CLAUDE.md](CLAUDE.md).

```bash
./tools/validate-all.sh
```

## License

[Apache-2.0](LICENSE) © cloud-concept-skills contributors. ClawHub bundles are MIT-0 on ClawHub. Repository source stays Apache-2.0.
