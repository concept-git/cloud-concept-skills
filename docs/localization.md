# Skill Localization Contract

English is the default install name; Simplified Chinese adds `-cn`:

```text
skills/en/<name>/       # English
skills/cn/<name>-cn/    # 简体中文
```

## Invariants

1. Each skill has exactly one pair. The folder and `SKILL.md.name` match.
2. English metadata uses `language: en` and `translation_of: <name>-cn`; Chinese uses
   `language: zh-CN` and `translation_of: <name>`.
3. Locale directories organize source discovery only. Each install payload is self-contained and
   never reads its sibling locale at runtime.
4. Commands, code, URLs, schemas, operation names, safety gates, and completion criteria have the
   same meaning in both locales. Translate prose, not behavior.
5. Executable assets are byte-identical unless a locale-specific implementation is explicitly
   documented and tested.
6. English `SKILL.md`, UI metadata, and skill page use English; Chinese equivalents use Chinese.
   Preserve vendor-native labels only when users must match them exactly.
7. Update both locales, QA, catalog, README, and marketplaces in one change. CI must pass
   `tools/validate-localization.py` and `tools/validate-all.sh` before publish.

## Change Rule

Change the behavioral source first, apply the same behavior to both locales, then translate. A
language-only edit may change wording but not commands, ordering, refusal rules, or observable
outputs.
