# Command Contract

This file contains operation purpose, templates, response fields, value mappings, and limits. Read
`concepts.md` for entity/state semantics and `SKILL.md` for behavior and guardrails.

## Standard Form

The service is always `BSS` and the CLI region is always `cn-north-1`; BSS is global and does not
use the profile's deployment region.

```bash
hcloud BSS <Operation> --cli-region=cn-north-1 --cli-output=json
```

Both operations have no business parameters and identify the account through the current profile. Do
not pass `customer_id`, `domain_id`, or pagination fields.

KooCLI requires a configured profile. Exporting only `HUAWEICLOUD_SDK_AK` and `HUAWEICLOUD_SDK_SK`
does not satisfy this flow and returns `[USE_ERROR]配置文件中不存在配置项`. Stop and ask the user to
configure a profile themselves; never write credentials.

## Global Constraints

- Allow only `ShowRealNameAuthStatus` and `ShowRealNameAuthQrCode`. The refused operations are
  `CreatePersonalRealnameAuth`, `CreateEnterpriseRealnameAuthentication`,
  `ChangeEnterpriseRealnameAuthentication`, and `ShowRealnameAuthenticationReviewResult`;
  create/change operations are writes and review-result inspection requires partner credentials.
- Main account only. If an IAM user fails, explain the requirement without replacing credentials.
- Each operation is limited to five calls per second by source IP, API, and ParentUid. Poll no
  faster than every two seconds; back off on `429` or `APIGW.0308`.
- Check status before every QR request because the QR operation does not enforce verification state.
- Never persist `qr_code_url`; it contains a one-time `ticket`.

## Operations

| Operation                | Purpose                              | Required | Rule                                              |
| ------------------------ | ------------------------------------ | -------- | ------------------------------------------------- |
| `ShowRealNameAuthStatus` | Account verification status and type | none     | Always first; also used for polling               |
| `ShowRealNameAuthQrCode` | Face-authentication URL              | none     | Only when unverified and the user has their phone |

### Status Response

| Field             | Type    | Value  | Meaning                                     |
| ----------------- | ------- | ------ | ------------------------------------------- |
| `verified_status` | Integer | `-1`   | unverified; offer QR flow                   |
|                   |         | `0`    | pending; wait without fetching another code |
|                   |         | `1`    | rejected; route to console review comments  |
|                   |         | `2`    | verified; short-circuit                     |
| `verified_type`   | Integer | `0`    | personal verification                       |
|                   |         | `1`    | enterprise verification                     |
|                   |         | `null` | omitted when status is `-1`                 |

`ShowRealNameAuthQrCode` returns `qr_code_url`, a String on the `auth.huaweicloud.com` domain
containing a one-time `ticket`. It expires after scanning or ten minutes.

## Templates

```bash
hcloud BSS ShowRealNameAuthStatus --cli-region=cn-north-1 --cli-output=json
```

```bash
hcloud BSS ShowRealNameAuthStatus --cli-region=cn-north-1 \
  --cli-output=json --cli-query=verified_status
```

```bash
hcloud BSS ShowRealNameAuthQrCode --cli-region=cn-north-1 \
  --cli-output=json --cli-query=qr_code_url
```

Render the unquoted result:

```bash
npx tsx scripts/render-qr.ts "$(hcloud BSS ShowRealNameAuthQrCode \
  --cli-region=cn-north-1 --cli-output=json --cli-query=qr_code_url | tr -d '"')"
```

Use the KooCLI waiter rather than a custom sleep loop:

```bash
hcloud BSS ShowRealNameAuthStatus --cli-region=cn-north-1 --cli-output=json \
  --cli-waiter="{\"expr\":\"verified_status\",\"to\":\"2\",\"timeout\":600,\"interval\":5}"
```

`timeout` is at most 600 seconds and `interval` is 2–10 seconds. After timeout, query status once
more because timeout does not distinguish unverified from pending, then ask before fetching another
QR code.

## Failure Routing

| Signal                                       | Response                                                             |
| -------------------------------------------- | -------------------------------------------------------------------- |
| `[USE_ERROR]配置文件中不存在配置项`          | Ask the user to configure an hcloud profile; never write credentials |
| `429` or `APIGW.0308`                        | Back off and retry no faster than every two seconds                  |
| IAM-user failure                             | Explain that a main account is required                              |
| `verified_status=1`                          | Route to console review comments; do not inspect or edit documents   |
| enterprise/document/bank-card/change request | Route to Account Center → Real-Name Authentication                   |
| non-Huawei-Cloud identity or general KYC     | State that it is out of scope without collecting evidence            |
