# cloud-concept-skills

Community-maintained Huawei Cloud skills; this is not an official Huawei Cloud project.

## Repository ownership

| Repository | Owns |
| --- | --- |
| `concept-skills` | Software concepts, semantic modeling, knowledge organization, and visual learning. |
| `cloud-concept-skills` | Huawei Cloud operations, billing, controlled provisioning, and account onboarding. |
| `myoffice-skills` | Office workflows, presentations, source notes, repository guidance, and Agent DX tooling. |

## Directory contract

| Directory | Contract |
| --- | --- |
| `skills/en/<name>/`, `skills/zh-CN/<name>-cn/` | Self-contained install payloads, including required `references/`, assets and runtime scripts. |
| `qa/` | Private local validation, fixtures and reports; ignored by Git and absent from public checkouts. |
| `catalog.yml` | Tracked discovery metadata used by QA and publishing tools. |
| `docs/` | Concise local notes and examples; ignored by Git and never required by QA or distribution. |
| `tools/`, `.githooks/`, `.github/` | Repository tooling, local commit/push gates and CI. |

Learning copies, downloaded repositories, process notes, raw outputs and generated eval workspaces
belong outside the checkout, normally in a task-specific temporary directory. Delete them when no
longer needed. Preserve runtime `skills/**/references/` and maintained fixtures/examples.

## Change and release rules

- Update the owning repository; keep sibling projects independent and link rather than copy their skills.
- Keep localized pairs, declared source versions and `catalog.yml` consistent; the catalog is the public version record. English uses the base
  name and `language: en`; Chinese adds `-cn` and `language: zh-CN`. Paired `translation_of` values
  name each other. Translate prose while preserving commands, safety gates and observable behavior.
  The repository `VERSION` and per-skill catalog versions have separate scopes.
- Run `./tools/validate-all.sh` for public package checks; it must work without `qa/`.
  Run `./tools/validate-all.sh --local-qa` only for available local QA; no behavioral or live-service result is implied by public checks.
- Set `git config core.hooksPath .githooks` once per checkout. Ignore rules and commit/push/CI hygiene checks
  keep local-only files out of Git, including files added with force.
- Commit and publish only within user authorization. ClawHub receives English payloads only;
  GitHub retains both languages. Verify remote contents before announcing a release.
- Treat credentials, local installs and caches as local-only. Keep only the current release notes;
  rewriting Git history or deleting remote releases requires explicit user authorization.
- Keep `qa/`, `docs/`, analysis material and generated reports local; exclude them even when force-added.

## Cloud-specific rules

- Keep active drafts under `development/` with optional private `qa/development/`; they are outside the
  installable catalog until explicitly promoted. Source-document routing is runtime data, not a study archive.
- Do not auto-install `hcloud` or collect credentials. Real BSS tests require the skill-specific
  opt-in variable; defaults stay offline. Billing and onboarding remain read-only. Provisioning
  stays within the allowlist and confirmation gates; unsubscribe stays console-only.
- Verify current CLI help before changing contracts. Classify effects from operation behavior,
  not the HTTP verb or operation name. Keep help checks, live results, absent data and permission
  failures distinct; one environment's success does not prove another environment works.
- Keep one canonical command contract with command, action, inputs/sources and constraints.
  Define field bindings once, retaining producer, type, selection condition, output and version.
  Service/Helper/Recipe/Persona/Shared are responsibility roles, not mandatory loading stages.
- FCAPS groups tool/target-system contracts. Distinguish agent host, target OS and Kubernetes
  context; preserve observation scope. Keep unfinished recipes brief and non-executable.
- Keep billing facts/dimensions/measures thin in semantic YAML; place CLI enums and examples in
  command references. Use document catalogs only when the command is unknown. Known commands
  route directly to contracts; a cached document or source-repair instruction grants no execution authority.
- Bind document metadata and QA evidence to declared source snapshots/hashes. Prefer the publisher's
  Markdown, then the same article's HTML; verify article identity and body. Store raw downloads,
  screenshots, clones and logs outside the checkout; keep reproducible validation fixtures.
