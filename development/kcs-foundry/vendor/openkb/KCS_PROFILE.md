# Local KCS profile

This vendor directory is a modified fork of the upstream snapshot recorded in `../openkb.source.json`. Original licensing and upstream attribution remain in place. `knowledge_profile` defaults to `generic`; existing generic compilation and its schema remain unchanged.

## Native compilation

Initialize a new KB with `openkb init --knowledge-profile kcs`. KCS concepts stay in `wiki/concepts/`, with `knowledge_kind: case` for bounded historical events and `pattern` for reusable methods with explicit conditions. Both retain the OpenKB source, summary, entity, index, wikilink and backlink model. Compile related material into existing concepts where justified; preserve differences, uncertain causes and conflicting evidence.

`openkb/kcs.py` owns the shared KCS rules, schema, payload checks, source/content fingerprints and offline audit. Concept bodies require one H1 and exactly four H2 sections, in order: Issue, Environment, Resolution, Cause. Resolution includes numbered steps. Each field has source-located evidence; a supported Cause requires evidence marked `confirmed_in_source`. Structural checks cannot establish that the source actually supports the claim.

The compiler supplies full prior pages and evidence when updating a concept. Program-owned metadata records the profile, schema version, kind, cause status, description, evidence, sources, fingerprints and content hash. New or changed knowledge becomes `draft`. Existing `reviewed`/`validated` state survives only when content and source fingerprints still match its `validation_hash`; no generator grants that state. Removing a source invalidates prior validation and requires reconciliation/recompilation.

KCS generation fails on malformed payloads or unresolved links instead of silently dropping failed pages. The existing per-document add mutation provides rollback. A Foundry batch may contain earlier successful document commits when a later document fails.

## Configuration and migration

The profile is KB-local, not a global scalar setting. KCS ingestion also requires an explicit nonempty KB-local model, to avoid accidentally inheriting an unrelated default deployment.

For an existing KB, back up its files, set `knowledge_profile: kcs`, then explicitly run `openkb recompile --refresh-schema`. A mismatching schema fails visibly rather than being silently replaced. Schema refresh keeps a backup. Changing a config flag alone does not convert existing concept bodies or evidence.

`openkb kcs-audit` checks native structure, source bindings, index synchronization and compiled graph links without a model. Generic structural lint is unchanged; KCS structural lint includes these errors. Foundry's `validate_kcs.py --kb` additionally checks original material snapshots and provenance across batches. Both are mechanical checks, not semantic review or runtime verification.

## Model protocol

For the Foundry short UTF-8 text ingestion path, the compiler calls LiteLLM chat completions with messages and JSON response format, without tool definitions. The model must produce the requested JSON. `response_format: {type: json_object}` support is independent of function calling; an internal gateway that rejects this parameter needs a separately tested compatibility adapter.

OpenKB query/chat, semantic lint, skill generation and `run_skill()` use Agents SDK function tools and require tool-call support. Setting `parallel_tool_calls: false` makes calls sequential; it does not remove tools. The default native Foundry path bypasses `run_skill()`. Explicit legacy `--mode export` still uses it. Reading the compiled wiki as local files requires neither API.

See `../../USAGE.md` for the actual deployment, provenance layout and internal pilot procedure. No live internal tickets or real model responses were used to validate this change.
