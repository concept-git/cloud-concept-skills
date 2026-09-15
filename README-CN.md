# 华为云 Agent Skills

[![skills.sh](https://skills.sh/b/concept-git/cloud-concept-skills)](https://skills.sh/concept-git/cloud-concept-skills)

社区维护的华为云技能仓库，覆盖账务分析、购买前成本估算与受控开通，以及账号实名认证引导。3 项能力提供 6 个中英文技能：英文使用基础名，简体中文增加
`-cn`。本项目不是华为云官方产品。

运行载荷位于 `skills/<name>/`；QA 与评估位于 `qa/<name>/`，安装技能时不会复制。

English: [README.md](README.md).

## 技能

| 技能                                                                                         | 版本  | 用途                                 |
| -------------------------------------------------------------------------------------------- | ----- | ------------------------------------ |
| [`huawei-cloud-billing-scout-cn`](docs/skills/cn/huawei-cloud-billing-scout-cn.md)           | 2.3.9 | 只读查询余额、消费、扣费归因和对账。 |
| [`huawei-cloud-cost-estimation-cn`](docs/skills/cn/huawei-cloud-cost-estimation-cn.md)       | 3.2.4 | 当次响应询价与受控资源开通。         |
| [`huawei-cloud-account-onboarding-cn`](docs/skills/cn/huawei-cloud-account-onboarding-cn.md) | 1.0.0 | 只读查询实名状态并引导人脸扫码。     |

## 安装

需要 Node.js（用于 `npx`）与 [KooCLI](https://support.huaweicloud.com/productdesc-hcli/hcli_01.html)
7.2+；技能不会自动安装 KooCLI。

基础名安装英文版；简体中文版统一使用 `-cn`。

```bash
npx skills add concept-git/cloud-concept-skills \
  --skill <skill-name> \
  --agent cursor \
  --copy -y
```

`--agent` 可填 `cursor`、`claude-code` 或 `codex`。查看技能列表：

```bash
npx skills add concept-git/cloud-concept-skills --list
```

各 Agent 说明：[Cursor](docs/agents/cursor.md) · [Claude Code](docs/agents/claude-code.md) ·
[Codex](docs/agents/codex.md) · [Hermes](docs/agents/hermes.md)。

使用前请阅读技能内容。账务与实名认证技能只读；资源开通只允许文档白名单内操作，并强制费用复核与显式确认；退订仅提供控制台指引。

## 贡献

[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) · [docs/authoring.md](docs/authoring.md)

```bash
./tools/validate-all.sh
```

## 许可

[Apache-2.0](LICENSE) © cloud-concept-skills
contributors。发布到 ClawHub 的技能包在该平台为 MIT-0；仓库源码仍为 Apache-2.0。
