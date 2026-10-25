# Huawei Cloud Agent Skills

[![skills.sh](https://skills.sh/b/concept-git/cloud-concept-skills)](https://skills.sh/concept-git/cloud-concept-skills)

社区维护的华为云技能仓库，覆盖账务分析、购买前成本估算与受控开通，以及账号实名认证引导。3 项能力提供 6 个中英文技能：英文使用基础名，简体中文增加
`-cn`。本项目不是华为云官方产品。

运行载荷位于 `skills/<locale>/<name>/`；校验与评估仅保留在本机 `qa/`，不提交、不发布。

English: [README.md](README.md).

## 技能

| 技能 | 版本 | 用途 |
| -------------------------------------------------------------------------------------------- | ----- | ------------------------------------ |
| [`huawei-cloud-billing-scout-cn`](skills/zh-CN/huawei-cloud-billing-scout-cn/SKILL.md) | 2.3.9 | 只读查询余额、消费、扣费归因和对账。 |
| [`huawei-cloud-cost-estimation-cn`](skills/zh-CN/huawei-cloud-cost-estimation-cn/SKILL.md) | 3.2.4 | 当次响应询价与受控资源开通。 |
| [`huawei-cloud-account-onboarding-cn`](skills/zh-CN/huawei-cloud-account-onboarding-cn/SKILL.md) | 1.0.0 | 只读查询实名状态并引导人脸扫码。 |

## 开发中

[`huawei-cloud-fcaps-diagnostics`](development/huawei-cloud-fcaps-diagnostics/README.md)
已完成华为云 ECS 及关联服务的诊断命令契约与资源衔接 Helper，场景 Recipe 仅规划。
当前独立存放在 `development/`，尚未发布为可安装技能。

## 安装

需要 Node.js 22.20+ 与 Git。在目标项目目录运行下列命令，直接复制即可；默认安装到当前项目的 Codex，不修改全局技能。

运行云技能还需要 [KooCLI](https://support.huaweicloud.com/productdesc-hcli/hcli_01.html) 7.2+；技能不会自动安装它。

`--agent codex` 可换为 `--agent claude-code` 或 `--agent cursor`；增加 `--global` 可供所有项目使用。技能安装器的[参数说明](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)。

### 中文版

```bash
npx --yes skills add concept-git/cloud-concept-skills --skill huawei-cloud-billing-scout-cn huawei-cloud-cost-estimation-cn huawei-cloud-account-onboarding-cn --agent codex --copy --yes
```

### 英文版

```bash
npx --yes skills add concept-git/cloud-concept-skills --skill huawei-cloud-billing-scout huawei-cloud-cost-estimation huawei-cloud-account-onboarding --agent codex --copy --yes
```

### 按需安装单个技能

**`huawei-cloud-billing-scout-cn`**

```bash
npx --yes skills add concept-git/cloud-concept-skills --skill huawei-cloud-billing-scout-cn --agent codex --copy --yes
```

**`huawei-cloud-cost-estimation-cn`**

```bash
npx --yes skills add concept-git/cloud-concept-skills --skill huawei-cloud-cost-estimation-cn --agent codex --copy --yes
```

**`huawei-cloud-account-onboarding-cn`**

```bash
npx --yes skills add concept-git/cloud-concept-skills --skill huawei-cloud-account-onboarding-cn --agent codex --copy --yes
```

### 查看可安装技能

```bash
npx --yes skills add concept-git/cloud-concept-skills --list
```

英文载荷位于 `skills/en/`，简体中文载荷位于 `skills/zh-CN/`；中文技能名仍以 `-cn` 结尾。ClawHub 仅发布英文版。

账务和实名认证技能只读；资源开通仍受技能的白名单、费用复核和确认约束；退订仅提供控制台指引。

## 贡献

`qa/` 仅供本机使用，不提交、不发布；公开校验不依赖它。需要运行本机用例时，使用 `./tools/validate-all.sh --local-qa`。

项目职责与目录规范见 [CLAUDE.md](CLAUDE.md)。

```bash
./tools/validate-all.sh
```

## 许可

[Apache-2.0](LICENSE) © cloud-concept-skills
contributors。发布到 ClawHub 的技能包在该平台为 MIT-0；仓库源码仍为 Apache-2.0。
