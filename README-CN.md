# Cloud Operations & Automation Skills

[![skills.sh](https://skills.sh/b/concept-git/cloud-concept-skills)](https://skills.sh/concept-git/cloud-concept-skills)

社区维护的华为云运维技能。已发布的是账务、成本估算和账号实名认证。诊断和知识提炼仍是草稿。前端设计和网页检查以 Git 子模块引入。

这些技能不是华为云官方产品。

English: [README.md](README.md)

## 已发布技能

英文用基础名，简体中文加 `-cn`。

| 技能 | 版本 | 用途 |
| --- | --- | --- |
| [`huawei-cloud-billing-scout-cn`](skills/productivity/zh-CN/huawei-cloud-billing-scout-cn/SKILL.md) | 2.3.12 | 只读查询余额、消费、扣费归因和对账。 |
| [`huawei-cloud-cost-estimation-cn`](skills/productivity/zh-CN/huawei-cloud-cost-estimation-cn/SKILL.md) | 3.3.0 | 当次响应询价，并在约束内开通资源。 |
| [`huawei-cloud-account-onboarding-cn`](skills/productivity/zh-CN/huawei-cloud-account-onboarding-cn/SKILL.md) | 1.0.3 | 只读查询实名状态，并引导人脸扫码。 |

目录：[catalog.yml](catalog.yml)。

账务和实名认证只读。开通资源仍受白名单、费用复核和确认约束。退订只给控制台指引。

## 安装

需要 Node.js 22.20+、Git，以及 [KooCLI](https://support.huaweicloud.com/productdesc-hcli/hcli_01.html) 7.2+。技能不安装 KooCLI。

在项目目录运行。默认装到该项目的 Codex。`--agent` 可换成 `claude-code` 或 `cursor`。加 `--global` 则所有项目可用。[安装参数](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)。

中文：

```bash
npx --yes skills add concept-git/cloud-concept-skills --skill huawei-cloud-billing-scout-cn huawei-cloud-cost-estimation-cn huawei-cloud-account-onboarding-cn --agent codex --copy --yes
```

英文：同一命令，技能名换成 `huawei-cloud-billing-scout huawei-cloud-cost-estimation huawei-cloud-account-onboarding`。

只装一个：把列表换成一个名字。查看可装技能：`npx --yes skills add concept-git/cloud-concept-skills --list`。

载荷在 `skills/productivity/en/` 和 `skills/productivity/zh-CN/`。ClawHub 只发布英文版。

## 目录

| 目录 | 用途 |
| --- | --- |
| `skills/productivity/` | 上面 6 个已发布技能。 |
| `skills/drafts/` | 草稿。不进公开目录，也不进默认安装列表。 |
| `skills/misc/` | 其他项目，包括下面两个子模块。 |
| `skills/engineering/` | 预留。 |

`skills.sh.json` 列出安装器要发现的已发布技能。

## 相关项目

[skills-list](https://github.com/daoxianglaonong/skills-list) 在 `skills/misc/frontend-design/skills-list/`：页面主题、响应式设计和设计验收。

[MetaPQP](https://github.com/vi-vi-vi-vi-vivian/MetaPQP) 在 `skills/misc/web-quality/MetaPQP/`：官网体验检查和页面对比。

克隆后运行 `git submodule update --init`。

## 开发中

[`directory-summary`](skills/drafts/directory-summary/SKILL.md) 根据目录里已有的文件生成 `.abstract.md` 和 `.overview.md`。

[`huawei-cloud-fcaps-diagnostics`](skills/drafts/huawei-cloud-fcaps-diagnostics/README.md) 已有华为云 ECS 及相关服务的诊断命令契约和资源衔接 Helper。场景指引仍是草稿，还没有端到端验证。它还不能安装。

[`kcs-foundry`](skills/drafts/kcs-foundry/README.md) 存放 KCS 知识提炼项目和 OpenKB 上游源码快照。

## 贡献

`qa/` 只在本机，不提交、不发布。公开校验不使用它。本机有用例时再运行 `./tools/validate-all.sh --local-qa`。

规则：[CLAUDE.md](CLAUDE.md)。

```bash
./tools/validate-all.sh
```

## 许可

[Apache-2.0](LICENSE) © cloud-concept-skills contributors。ClawHub 上的安装包是 MIT-0。仓库源码仍是 Apache-2.0。
