# 华为云账号开通 · 人脸扫码实名认证

`huawei-cloud-account-onboarding-cn` · **Huawei Cloud Account Onboarding — Real-Name Verification via Face-Scan QR**

Answers and resolves one question: **can this Huawei Cloud account buy anything yet?** The skill checks `verified_status` over read-only BSS, and when the account is unverified it fetches the face-auth QR address, renders it in the terminal for the user to scan on their phone, then polls until verification lands. Read-only throughout: it never submits, changes or reviews an authentication, and never touches identity materials.

> **华为社区版** · 社区维护，非华为云官方；结论以当次 hcloud/BSS 响应为准。

**Version:** 1.0.0 · Changelog: [qa/huawei-cloud-account-onboarding-cn/CHANGELOG.md](../../../qa/cn/huawei-cloud-account-onboarding-cn/CHANGELOG.md)

## What it does

| Capability | Behavior |
| --- | --- |
| Status check | `hcloud BSS ShowRealNameAuthStatus` → `verified_status` (`-1` 未实名 / `0` 审核中 / `1` 不通过 / `2` 已实名) and `verified_type` (`0` 个人 / `1` 企业) |
| QR fetch | `hcloud BSS ShowRealNameAuthQrCode` → `qr_code_url`, single-use, void after 10 minutes; fetched only when unverified **and** the user has their phone at hand |
| Terminal render | `scripts/render-qr.ts` draws a scannable half-block QR with the single-use warning and a fallback URL |
| Polling | `--cli-waiter` on `verified_status` to `2` (interval 5s, timeout 600s), then one confirming re-read |
| Gate ownership | The QR command does **not** validate verification state — it returns a usable code even for verified accounts — so the skill checks status first |
| Surface | The payload speaks `hcloud` commands only; no raw OpenAPI paths, HTTP verbs or auth headers appear in the skill |
| Out of scope | Enterprise / certificate / bank-card / change channels (console-only), review comments, ID or credential intake, any write operation, non-Huawei-Cloud KYC |

## Runtime bundle (install payload)

```text
skills/huawei-cloud-account-onboarding-cn/
├── SKILL.md
├── references/
│   ├── concepts.md          # entities, state machine, channel boundary
│   └── commands.md          # operation contracts, fields, enums, templates
└── scripts/
    ├── render-qr.ts         # the only script: pure terminal QR renderer
    └── package.json         # qrcode + tsx (npm install at first use)
```

No `evals/`, `qa/`, or `*-workspace/` under `skills/`; `node_modules/` is installed locally and never committed.

## SKILL.md structure

SKILL.md is kept as a compact entry point (~15 lines of body); the detail lives in `references/`.

| Section | Role |
| --- | --- |
| 三步 | 查状态 → 递二维码 → 盯落地, with the gate that the QR command does not self-validate |
| 红线 | Read-only · no material intake · no proxy verification · face-scan channel only |
| References | Where to read entities, commands and the renderer |

## In-skill flow

```text
用户提到华为云实名认证
     │
     ▼
门禁 · 是当前 hcloud profile 的华为云账号？profile 已配置？
     │
     ▼
ShowRealNameAuthStatus
     ├─ 2  已实名 ──> 报状态与认证类型，结束（不取码）
     ├─ 0  审核中 ──> 告知等待，不重复取码
     ├─ 1  不通过 ──> 控制台「账号中心 → 实名认证」看审核意见
     └─ -1 未实名
            │ 确认用户此刻能拿手机
            ▼
     ShowRealNameAuthQrCode ──> render-qr.ts ──> 用户手机扫码 + 活体
            │
            ▼
     --cli-waiter 至 verified_status=2 ──> 落地：恭喜 | 超时：先问再重取
```

## Safety

The QR address carries a one-time `ticket`. It is rendered for the current user only — never written to a file or log, never forwarded to another person or device. Proxy scanning defeats liveness verification and risks Huawei Cloud freezing the account. ID numbers, document photos, bank cards and SMS codes are refused on sight; the three-step flow needs none of them.

## QA layout

```text
qa/huawei-cloud-account-onboarding-cn/
├── validate.sh
├── VERSION · CHANGELOG.md
├── skillcheck.toml · .markdownlint.json
├── evals/evals.json            # 11 cases
├── assertions/README.md
└── fixtures/ops_contracts.yml  # cross-layer operation contract
```

```bash
./qa/huawei-cloud-account-onboarding-cn/validate.sh
```

Gate = layout purity (including stale-mock regression) + version sync across `qa/VERSION`, `SKILL.md`, `docs/catalog.yml` and this page + `ops_contracts.yml` ↔ `commands.md` cross-layer check + script purity/render/exit-code smoke + skills-ref + markdownlint + skillcheck. Real BSS calls run only when `HUAWEICLOUD_ACCOUNT_ONBOARDING_REAL=1`.

## Install

```bash
npx skills add concept-git/cloud-concept-skills/skills/huawei-cloud-account-onboarding-cn
cd skills/huawei-cloud-account-onboarding-cn/scripts && npm install
```

Requires `hcloud` (KooCLI 7.2+) with a profile configured by the user (`hcloud configure set`) on the **main account** — IAM sub-users cannot call these operations. The agent never installs the CLI or writes credentials.

## Marketplaces

- [ClawHub](https://clawhub.ai/) — publish from `skills/huawei-cloud-account-onboarding-cn/` after `./qa/huawei-cloud-account-onboarding-cn/validate.sh`

ClawHub publish (only after explicit release approval):

```bash
# Use absolute path to the skill folder (relative ./skills/... may fail on some CLI versions)
clawhub skill publish "$PWD/skills/huawei-cloud-account-onboarding-cn" \
  --slug huawei-cloud-account-onboarding-cn \
  --name "Huawei Cloud Account Onboarding — Real-Name Verification via Face-Scan QR" \
  --version <semver> \
  --changelog "<semver>: rewrite onto the real BSS face-scan commands; terminal QR renderer; waiter polling; mock server removed" \
  --clawscan-note "Huawei Cloud BSS read-only, two Show operations only (ShowRealNameAuthStatus, ShowRealNameAuthQrCode). Face-scan channel only; refuses ID/document/bank-card/SMS intake, refuses all real-name write operations, routes enterprise and certificate channels to the console; agent must not install hcloud or write credentials; the single script renders a QR string and performs no I/O" \
  --tags latest
```

ClawHub skill bundle is **MIT-0**; repository source remains **Apache-2.0**. Installable `SKILL.md` must not declare a conflicting `license` in frontmatter.
