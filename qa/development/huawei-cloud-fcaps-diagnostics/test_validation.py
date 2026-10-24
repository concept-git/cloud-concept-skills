#!/usr/bin/env python3
"""Inject realistic contract errors into disposable copies; never call cloud APIs."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

QA = Path(__file__).resolve().parent
SOURCE = QA.parents[2] / "development/huawei-cloud-fcaps-diagnostics"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--recheck", type=Path, required=True)
    args = parser.parse_args()
    cases = [
        ("missing_command", "references/commands/configuration/hcloud.md", r"^\| `ECS/ShowServer/v2`[^\n]*\n", "", "Coverage mismatch"),
        ("wrong_version", "references/commands/configuration/hcloud.md", r"ECS/ShowServer/v2", "ECS/ShowServer/v99", "Coverage mismatch"),
        ("scan_labeled_read", "references/commands/security/hcloud-host.md", "发起基线及弱口令检测", "读取基线结果", "Known effect/method distinction lost"),
        ("wrong_subnet_binding", "references/helpers.md", re.escape("同项 `subnets[].id` → `VPC.SubnetId`"), "同项 `subnets[].neutron_subnet_id` → `VPC.SubnetId`", "Missing selection or field binding"),
        ("false_live_success", "references/verification/cloud.md", re.escape("`HSS/RunBaselineDetect/v5` | 通过 | 未执行"), "`HSS/RunBaselineDetect/v5` | 通过 | 成功", "Verification evidence mismatch"),
        ("false_cli_execution", "references/verification/cloud.md", re.escape("`configure set` | 通过 | 未执行"), "`configure set` | 通过 | 成功", "CLI verification evidence mismatch"),
        ("wrong_dependency_location", "references/commands/configuration/hcloud.md", re.escape("[ECS/ListServersDetails/v2](hcloud.md#ecs)"), "[ECS/ListServersDetails/v2](../fault/hcloud.md#ecs)", "Dependency points outside its canonical contract"),
        ("wrong_enum_case", "references/commands/configuration/hcloud.md", "usage=True", "usage=true", "Execution constraint lost"),
        ("stale_execution_proof", "references/tools/hcloud.md", "已确认的 profile、region、IAM project", "默认 profile、region、IAM project", "Live dependency checks do not match this contract revision"),
    ]
    with tempfile.TemporaryDirectory(prefix="hcloud-contract-tests-") as tmp:
        root = Path(tmp)

        def run(skill, name):
            report = root / (name + "-report")
            result = subprocess.run([
                "rtk", "proxy", sys.executable, str(QA / "validate.py"),
                "--skill", str(skill), "--evidence", str(args.evidence.resolve()),
                "--recheck", str(args.recheck.resolve()), "--report-dir", str(report),
            ], capture_output=True, text=True)
            path = report / "acceptance.json"
            if not path.exists():
                raise AssertionError(f"Validator failed without a report: {result.stderr}")
            return result.returncode, json.loads(path.read_text())

        code, report = run(SOURCE, "baseline")
        assert code == 0, report["errors"]
        print("PASS baseline")
        for name, rel, pattern, replacement, expected in cases:
            copy = root / name
            shutil.copytree(SOURCE, copy)
            path = copy / rel
            changed, count = re.subn(pattern, lambda _: replacement, path.read_text(), count=1, flags=re.M)
            assert count == 1, f"Mutation no longer applies: {name}"
            path.write_text(changed)
            code, report = run(copy, name)
            assert code != 0 and any(expected in e for e in report["errors"]), (name, report["errors"])
            print("PASS rejected " + name)
    print(f"PASS {len(cases)} injected errors rejected")


if __name__ == "__main__":
    main()
