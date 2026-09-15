# cloud-concept-skills

Community-maintained Huawei Cloud skills; not an official Huawei Cloud project.

## Repository contract

- `skills/<name>/` contains the install payload only. Put gates, evals, and `skillcheck.toml` under `qa/<name>/`.
- Run `./qa/<name>/validate.sh` for a changed skill or `./tools/validate-all.sh` for the repository.
- Keep `skills/`, `qa/` (`VERSION`, changelog), `docs/catalog.yml`, and `docs/skills/<name>.md` synchronized.
- English lives at `skills/en/<name>`; Simplified Chinese at `skills/cn/<name>-cn`. Update pairs together under `docs/localization.md`; `tools/validate-localization.py` is the parity gate.
- Never commit credentials, `.env*`, generated workspaces, or gate reports.
- Do not auto-install `hcloud`. Real BSS calls run only when a skill-specific opt-in environment variable enables them.
- Billing and onboarding stay read-only. Cost-estimation creates stay within the allowlist and confirmation gates; unsubscribe stays console-only.

## Billing semantic split

Keep facts, dimensions, measures, and routing thin in `references/semantic/*.yml`. Put CLI contracts, concrete codes, enum values, response paths, and command examples in `references/related-commands.md` and its linked command references.
