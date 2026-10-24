# huawei-cloud-account-onboarding QA

Per-skill quality gate. Run `validate.sh` locally and in CI via
`tools/validate-all.sh`.

## Layout

```text
qa/huawei-cloud-account-onboarding/
├── validate.sh                 # entry point (required)
├── VERSION · CHANGELOG.md
├── skillcheck.toml · .markdownlint.json
├── README.md
├── evals/evals.json            # Skill Creator eval cases
├── assertions/README.md        # assertion rubric for eval authors
└── fixtures/ops_contracts.yml  # cross-layer operation contract
```

`fixtures/ops_contracts.yml` is the source of truth for the two BSS operations
(URI, response fields, enum values, refused write operations). `validate.sh`
fails when `skills/.../references/commands.md` drifts from it.

## Commands

```bash
./qa/huawei-cloud-account-onboarding/validate.sh
```

Real BSS calls are gated. They run only with a configured `hcloud` profile and:

```bash
HUAWEICLOUD_ACCOUNT_ONBOARDING_REAL=1 ./qa/huawei-cloud-account-onboarding/validate.sh
```

The real smoke is read-only: it reads `verified_status` and asserts the value is
within the documented enum. It never fetches a QR code, since every fetch burns a
single-use credential.
