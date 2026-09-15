# Huawei Cloud Agent Skills

[![skills.sh](https://skills.sh/b/concept-git/cloud-concept-skills)](https://skills.sh/concept-git/cloud-concept-skills)

Community-maintained Huawei Cloud skills for billing analysis, pre-order cost estimation and
controlled provisioning, and account real-name onboarding. Three capabilities ship as six localized
skills: English uses the base name and Simplified Chinese adds `-cn`. This project is not an
official Huawei Cloud product.

Every skill keeps its runtime payload under `skills/<name>/`; QA and evaluations live under
`qa/<name>/` and are not installed with the skill.

中文说明见 [README-CN.md](README-CN.md).

## Skills

| English                                                                                | 中文                                                                                         | Purpose                                            |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| [`huawei-cloud-billing-scout`](docs/skills/en/huawei-cloud-billing-scout.md)           | [`huawei-cloud-billing-scout-cn`](docs/skills/cn/huawei-cloud-billing-scout-cn.md)           | Read-only billing analysis and reconciliation.     |
| [`huawei-cloud-cost-estimation`](docs/skills/en/huawei-cloud-cost-estimation.md)       | [`huawei-cloud-cost-estimation-cn`](docs/skills/cn/huawei-cloud-cost-estimation-cn.md)       | Current-response quotes and guarded provisioning.  |
| [`huawei-cloud-account-onboarding`](docs/skills/en/huawei-cloud-account-onboarding.md) | [`huawei-cloud-account-onboarding-cn`](docs/skills/cn/huawei-cloud-account-onboarding-cn.md) | Read-only real-name status and face-scan guidance. |

## Install

Requires Node.js for `npx`. The skills additionally require
[KooCLI](https://support.huaweicloud.com/intl/en-us/productdesc-hcli/hcli_01.html) 7.2+; they do not
install it automatically.

Base names install English. Append `-cn` for Simplified Chinese.

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

Agent-specific notes: [Cursor](docs/agents/cursor.md) · [Claude Code](docs/agents/claude-code.md) ·
[Codex](docs/agents/codex.md) · [Hermes](docs/agents/hermes.md).

Read each skill before use: skills run with the agent's permissions. Billing and onboarding are
read-only. Provisioning is limited to the documented allowlist and confirmation gates; unsubscribe
is console-guided only.

## Contributing

[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) · [docs/authoring.md](docs/authoring.md)

```bash
./tools/validate-all.sh
```

## License

[Apache-2.0](LICENSE) © cloud-concept-skills contributors. Bundles published to ClawHub are MIT-0
there; repository source remains Apache-2.0.
