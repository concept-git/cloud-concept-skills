# Huawei Cloud Agent Skills

[![skills.sh](https://skills.sh/b/concept-git/cloud-concept-skills)](https://skills.sh/concept-git/cloud-concept-skills)

Community-maintained Huawei Cloud skills for billing analysis, pre-order cost estimation and controlled provisioning, and account real-name onboarding. This project is not an official Huawei Cloud product.

Every skill keeps its runtime payload under `skills/<name>/`; QA and evaluations live under `qa/<name>/` and are not installed with the skill.

中文说明见 [README-CN.md](README-CN.md).

## Skills

| Skill | Version | Purpose |
| --- | --- | --- |
| [`huawei-cloud-billing-scout`](docs/skills/huawei-cloud-billing-scout.md) | 2.3.9 | Read-only balance, spend, charge attribution, reconciliation, coupons, stored-value cards, and partner billing. |
| [`huawei-cloud-cost-estimation`](docs/skills/huawei-cloud-cost-estimation.md) | 3.2.4 | Period and on-demand quotes; allowlisted creates behind dry-run, fee review, and explicit confirmation. |
| [`huawei-cloud-account-onboarding`](docs/skills/huawei-cloud-account-onboarding.md) | 1.0.0 | Read-only real-name status, terminal face-scan QR rendering, and waiter polling. |

## Install

Requires Node.js for `npx`. The skills additionally require [KooCLI](https://support.huaweicloud.com/intl/en-us/productdesc-hcli/hcli_01.html) 7.2+; they do not install it automatically.

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

Agent-specific notes: [Cursor](docs/agents/cursor.md) · [Claude Code](docs/agents/claude-code.md) · [Codex](docs/agents/codex.md) · [Hermes](docs/agents/hermes.md).

Read each skill before use: skills run with the agent's permissions. Billing and onboarding are read-only. Provisioning is limited to the documented allowlist and confirmation gates; unsubscribe is console-guided only.

## Contributing

[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) · [docs/authoring.md](docs/authoring.md)

```bash
./tools/validate-all.sh
```

## License

[Apache-2.0](LICENSE) © cloud-concept-skills contributors. Bundles published to ClawHub are MIT-0 there; repository source remains Apache-2.0.
