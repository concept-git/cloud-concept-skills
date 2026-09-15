# huawei-cloud-account-onboarding Changelog

Skill-only history. Repository tooling changes: [../../CHANGELOG.md](../../CHANGELOG.md).

## 1.0.0 - 2026-08-24

Rewrite onto the real Huawei Cloud BSS API. **Breaking**: the local mock server and
its HTTP contract are gone; the skill now calls `hcloud` and needs a configured profile.

### Features

- Real BSS read-only face-scan channel via KooCLI 7.2.12: `ShowRealNameAuthStatus`
  and `ShowRealNameAuthQrCode`, both parameterless and fixed to `--cli-region=cn-north-1`
- The payload speaks `hcloud` commands only — no OpenAPI paths, HTTP verbs or auth
  headers surface anywhere in the skill
- SKILL.md kept as a compact entry point (~15 lines of body): three steps, four red
  lines, and pointers into `references/`
- `references/concepts.md` — entities, the four `verified_status` states and their
  routes, why the QR gate lives in the skill, face-scan-only channel boundary
- `references/commands.md` — command contracts, response fields and enum maps,
  `--cli-query` narrowing, `--cli-waiter` polling to `verified_status=2`,
  throttle (5/s) and failure routing
- `scripts/render-qr.ts` — the only script: pure terminal QR renderer in TypeScript,
  no hcloud call, no env read, no file write; exits 2 on missing or non-https input

### Fixes

- Stop treating the QR operation as self-gating — it returns a usable code even for
  already-verified accounts (verified against a live account), so the skill checks
  status first
- Drop `license` from frontmatter and declare `metadata.openclaw.requires.bins: [hcloud]`,
  matching the other Huawei Cloud skills

### Removals

- `scripts/mock-server.js`, `scripts/create-verification.js`,
  `scripts/poll-verification.js`, `references/api-contract.md`

### QA

- `fixtures/ops_contracts.yml` cross-layer contract (operation, response fields,
  enum values, refused write operations) verified against `references/commands.md`
- Guards that no OpenAPI path leaks into the payload and that SKILL.md stays an
  entry point (<=25 non-empty body lines)
- Script purity check, render smoke and exit-code assertions
- Optional real BSS smoke behind `HUAWEICLOUD_ACCOUNT_ONBOARDING_REAL=1`
- Evals expanded to 11 cases covering all four states, credential hygiene and
  channel refusals

## 0.1.0 - 2026-07-04

First release (**Huawei Community Edition**, local mock).

### Features

- Real-name verification (实名认证) QR flow modeled on industry three-part shape
  (create session → poll status → terminal state; Feishu QR login / Alipay certify / Stripe Identity)
- `scripts/mock-server.js` — zero-dep mock: `POST /v1/verifications`,
  `GET /v1/verifications/{id}`, `GET /v1/customers/me/verification-status`,
  H5 approve/reject page on LAN IP; TTL 180s (env-overridable), scanned sessions never expire
- `scripts/create-verification.js` — terminal QR (colored frame, black/white modules via `qrcode`),
  machine-readable `VERIFICATION_ID=` output, idempotent on already-verified accounts
- `scripts/poll-verification.js` — 3s polling with status transitions
  (pending → scanned → approved/rejected/expired), exit codes 0/2/3/4
- SKILL.md workflow: check account status → generate QR → poll → converge;
  expired QR prompts user before regenerating; refuses real ID/credential intake
- QA gate: layout + version sync + script syntax/e2e smoke + skills-ref + markdownlint + skillcheck
