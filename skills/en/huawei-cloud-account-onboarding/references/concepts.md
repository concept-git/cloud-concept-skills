# Real-Name Verification Concepts

This file defines entities, state semantics, and guidance boundaries. Copyable commands and value
mappings live in `commands.md`.

## Entities

**RealNameAuthStatus** is an account-level fact from `ShowRealNameAuthStatus`, at the grain of one
account at one point in time. It determines whether the account can purchase resources on the China
site and whether a QR code is needed. It answers only whether the current profile is verified and
its verification type; subject details, document numbers, submission time, review comments, and
failure detail remain in the console.

**FaceAuthQrCode** is a one-time credential from `ShowRealNameAuthQrCode`, at one URL per call. The
account holder scans it on their phone for a liveness check. It expires after scanning or after ten
unscanned minutes. Render it only for the current user; never persist, forward, reuse, or parse its
`ticket`.

## State Machine

| State      | Meaning                       | Route                                         |
| ---------- | ----------------------------- | --------------------------------------------- |
| unverified | never submitted or expired    | fetch → render → user scans → poll            |
| pending    | submitted and awaiting review | wait; never fetch another code                |
| rejected   | review failed                 | console review comments; never edit documents |
| verified   | terminal state                | report status/type and do not fetch a code    |

Pending and rejected usually come from non-face channels such as document review. Face verification
is immediate and normally moves from unverified directly to verified.

## The Skill Owns the QR Gate

`ShowRealNameAuthQrCode` does not check verification status and returns a usable URL even for an
already verified account. Always check status first and short-circuit verified accounts. The
operation does not protect the user; the skill must.

## Face-Scan Only

This is the only immediate channel that requires the skill to handle no identity material. Route
personal-document review, bank-card review, enterprise review, and subject changes to Huawei Cloud
Console → Account Center → Real-Name Authentication. Corresponding BSS write operations require
partner credentials and identity images in OBS, which conflict with this read-only skill.

## User Presence and Sensitive Data

Before fetching a code, confirm the user has their phone now. A code expires in ten minutes and rate
limits are five calls per second. After expiry or timeout, ask before fetching another code; never
regenerate silently.

Refuse identity numbers, document images, bank-card details, and SMS codes and ask the user to
delete them. The complete flow is status → QR delivery → status monitoring and requires none of
those values. Scanning, liveness, and confirmation happen only on the user's phone.
