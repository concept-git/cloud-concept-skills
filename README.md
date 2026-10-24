# Cloud Agent Skills

[![skills.sh](https://skills.sh/b/concept-git/cloud-concept-skills)](https://skills.sh/concept-git/cloud-concept-skills)

Community-maintained Cloud skills for billing analysis, pre-order cost estimation and
controlled provisioning, and account real-name onboarding. Three capabilities ship as six localized
skills: English uses the base name and Simplified Chinese adds `-cn`. This project is not an
official Cloud product.

Every skill keeps its runtime payload under `skills/<locale>/<name>/`; QA and evaluations live under
`qa/<locale>/<name>/` and are not installed with the skill.

中文说明见 [README-CN.md](README-CN.md).

## Skills

| English | 中文 | Version | Purpose |
| --- | --- | --- | --- |
| [`huawei-cloud-billing-scout`](skills/en/huawei-cloud-billing-scout/SKILL.md) | [`huawei-cloud-billing-scout-cn`](skills/cn/huawei-cloud-billing-scout-cn/SKILL.md) | 2.3.9 | Read-only billing analysis and reconciliation. |
| [`huawei-cloud-cost-estimation`](skills/en/huawei-cloud-cost-estimation/SKILL.md) | [`huawei-cloud-cost-estimation-cn`](skills/cn/huawei-cloud-cost-estimation-cn/SKILL.md) | 3.2.4 | Current-response quotes and guarded provisioning. |
| [`huawei-cloud-account-onboarding`](skills/en/huawei-cloud-account-onboarding/SKILL.md) | [`huawei-cloud-account-onboarding-cn`](skills/cn/huawei-cloud-account-onboarding-cn/SKILL.md) | 1.0.0 | Read-only real-name status and face-scan guidance. |

Discovery metadata: [catalog.yml](catalog.yml).

## In development

[`huawei-cloud-fcaps-diagnostics`](development/huawei-cloud-fcaps-diagnostics/README.md)
contains verified diagnostic command contracts and resource helpers for Huawei Cloud
ECS and related services. Recipes remain planned. It stays under `development/`
and is not published as an installable skill.

## Install

Requires Node.js for `npx`. The skills additionally require
[KooCLI](https://support.huaweicloud.com/intl/en-us/productdesc-hcli/hcli_01.html) 7.2+; they do not
install it automatically.

Base names install English. Append `-cn` for Simplified Chinese.

ClawHub publishes only the English `skills/en` editions; Chinese editions remain on GitHub.

```bash
npx skills add concept-git/cloud-concept-skills \
  --skill <skill-name> \
  --agent cursor \
  --copy -y
```

`--agent` accepts `cursor`, `claude-code`, or `codex`. List available skills with:

```bash
npx skills add concept-git/cloud-concept-skills --list
```

Read each skill before use: skills run with the agent's permissions. Billing and onboarding are
read-only. Provisioning is limited to the documented allowlist and confirmation gates; unsubscribe
is console-guided only.

## Contributing

Project rules and repository ownership: [CLAUDE.md](CLAUDE.md).

```bash
./tools/validate-all.sh
```

## License

[Apache-2.0](LICENSE) © cloud-concept-skills contributors. Bundles published to ClawHub are MIT-0
there; repository source remains Apache-2.0.
