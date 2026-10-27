#!/usr/bin/env python3
"""Check RFQ references, API field coverage and locale structure without cloud calls."""
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
COMMON_LINE = {
    "id", "cloud_service_type", "resource_type", "resource_spec", "region",
    "subscription_num", "available_zone", "resource_size", "size_measure_id",
}
MODES = {
    "period": ("ListRateOnPeriodDetail", "RFQ_Header", "RFQ_Line",
               set(), {"period_type", "period_num", "fee_installment_mode"}),
    "on_demand": ("ListOnDemandResourceRatings", "RFQ_OnDemand_Header", "RFQ_OnDemand_Line",
                  {"inquiry_precision"}, {"usage_factor", "usage_value", "usage_measure_id"}),
}


class UniqueKeys(yaml.SafeLoader):
    pass


def mapping(loader, node, deep=False):
    pairs = loader.construct_pairs(node, deep=deep)
    result = dict(pairs)
    assert len(result) == len(pairs), "Duplicate YAML key"
    return result


UniqueKeys.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def read(path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeys)


def topology(value):
    """Compare language-independent structure; prose is reviewed separately."""
    prose = {"description", "meaning", "grain", "source_rule", "relations",
             "evidence_boundary", "invariants", "contract_sections"}
    if isinstance(value, dict):
        return {k: topology(v) for k, v in value.items() if k not in prose}
    if isinstance(value, list):
        return [topology(v) for v in value]
    return value


structures = []
for locale, name in [("en", "huawei-cloud-cost-estimation"),
                     ("zh-CN", "huawei-cloud-cost-estimation-cn")]:
    base = ROOT / "skills" / locale / name
    models_dir = base / "references/pricing/rfq-models"
    core = read(models_dir / "rfq-core.yml")
    assert set(core["models"]) == set(MODES), "Unexpected pricing-mode coverage"
    expected_files = {"rfq-core.yml", *core["models"].values()}
    assert {p.name for p in models_dir.glob("*.yml")} == expected_files
    command = models_dir / core["command_contracts_file"]
    headings = set(re.findall(r"^#{1,6} (.+)$", command.read_text(), re.M))
    dimensions = core["dimensions"]
    assert dimensions["Dim_ResourceSpec"]["business_key"] == [
        "cloud_service_type", "resource_type", "region_code", "charge_mode", "resource_spec"]
    for dimension in dimensions.values():
        if "parent_dimension" in dimension:
            assert dimension["parent_dimension"] in dimensions
    models = []
    for mode, (operation, header, line, header_extra, line_extra) in MODES.items():
        model = read(models_dir / core["models"][mode])
        assert model["pricing_mode"] == mode
        assert model["source_operation"] == "BSS/" + operation
        assert model["shared_file"] == "rfq-core.yml"
        assert set(model["contract_sections"]) <= headings
        facts = {fact["name"]: fact for fact in model["facts"]}
        assert set(facts) == {header, line}
        assert facts[header]["child_facts"] == [line]
        assert facts[line]["parent_fact"] == header
        available_dimensions = {**dimensions, **model.get("dimensions", {})}
        for fact_name, expected in [(header, {"project_id"} | header_extra),
                                    (line, COMMON_LINE | line_extra)]:
            fact = facts[fact_name]
            shared = core[fact["fields_from"]]
            extra = fact.get("attributes", {})
            assert not shared.keys() & extra.keys(), "A mode shadows a shared field"
            fields = {**shared, **extra}
            assert set(fields) == expected, (mode, fact_name, set(fields) ^ expected)
            for definition in fields.values():
                if "dimension" in definition:
                    assert definition["dimension"] in available_dimensions
        models.append(model)
    for path in [base / "SKILL.md", command, *models_dir.glob("*.yml")]:
        assert not re.search(r"semantic/catalog\.yml|rfq-shared-dimensions\.yml", path.read_text())
    structures.append(topology([core, *models]))
assert structures[0] == structures[1], "RFQ structure differs between locales"
print("OK: RFQ field coverage, references and locale structure validated")
