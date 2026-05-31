#!/usr/bin/env python3
"""
CCFTS demo contract test.

Checks that each demo has the required structure and that the published
expected CSV files pass a few basic business sanity checks. This is not a full
accounting engine; it catches obvious public-demo regressions.
"""

import csv
import sys
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"

REQUIRED_DEMO_STRUCTURE = {
    "README.md": "file",
    "input": "dir",
    "expected": "dir",
    "output": "dir",
}

REQUIRED_DEMO_FILES = {
    "demo-spv-flash-report": [
        "input/trial-balance.csv",
        "expected/quick-report-pnl.csv",
        "expected/quick-report-bs.csv",
    ],
    "demo-project-unit-flash-report": [
        "input/trial-balance.csv",
        "expected/quick-report-pnl.csv",
        "expected/quick-report-bs.csv",
    ],
    "demo-vat-prepayment": [
        "input/project-info.csv",
        "expected/prepayment-calculation.csv",
    ],
}


def _load_amounts(csv_path):
    with csv_path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    amounts = {}
    for row in rows:
        name = row.get("项目名称")
        amount = row.get("金额(万元)")
        if not name or amount in (None, ""):
            continue
        try:
            amounts[name] = float(amount)
        except ValueError:
            continue
    return amounts


def _check_balance_sheet(demo_dir, errors):
    bs_path = demo_dir / "expected" / "quick-report-bs.csv"
    if not bs_path.exists():
        return
    amounts = _load_amounts(bs_path)
    assets = amounts.get("资产总计")
    liabilities = amounts.get("负债合计")
    equity = amounts.get("权益合计", 0.0)
    liabilities_plus_equity = amounts.get("负债+权益合计")
    if liabilities_plus_equity is None and liabilities is not None:
        liabilities_plus_equity = liabilities + equity
    if assets is None or liabilities_plus_equity is None:
        errors.append(f"{demo_dir.name}: balance sheet missing assets or liabilities+equity total")
        return
    if round(assets - liabilities_plus_equity, 6) != 0:
        errors.append(
            f"{demo_dir.name}: balance sheet not balanced "
            f"(assets={assets}, liabilities+equity={liabilities_plus_equity})"
        )


def _check_vat_expected(demo_dir, errors):
    vat_path = demo_dir / "expected" / "prepayment-calculation.csv"
    if not vat_path.exists():
        return
    with vat_path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    total_row = next((r for r in rows if r.get("项目") == "合计"), None)
    detail_rows = [r for r in rows if r.get("项目") and r.get("项目") != "合计"]
    if not total_row or not detail_rows:
        errors.append(f"{demo_dir.name}: VAT expected missing detail rows or total row")
        return
    vat_sum = sum(float(r["预缴VAT(万元)"]) for r in detail_rows)
    total_sum = sum(float(r["预缴合计(万元)"]) for r in detail_rows)
    if round(float(total_row["预缴VAT(万元)"]) - vat_sum, 6) != 0:
        errors.append(f"{demo_dir.name}: VAT total does not match detail VAT sum")
    if round(float(total_row["预缴合计(万元)"]) - total_sum, 6) != 0:
        errors.append(f"{demo_dir.name}: VAT grand total does not match detail sum")

def run():
    if not EXAMPLES_DIR.exists():
        print("SKIP: examples/ directory does not exist")
        sys.exit(0)

    demos = [d for d in sorted(EXAMPLES_DIR.iterdir()) if d.is_dir()]
    if not demos:
        print("SKIP: no demo directories found under examples/")
        sys.exit(0)

    errors = []
    for demo in demos:
        demo_name = demo.name
        for path, ptype in REQUIRED_DEMO_STRUCTURE.items():
            full_path = demo / path
            if ptype == "file" and not full_path.is_file():
                errors.append(f"{demo_name}: missing {path}")
            elif ptype == "dir" and not full_path.is_dir():
                errors.append(f"{demo_name}: missing {path}/ directory")

        for relative_file in REQUIRED_DEMO_FILES.get(demo_name, []):
            full_path = demo / relative_file
            if not full_path.is_file():
                errors.append(f"{demo_name}: missing {relative_file}")
            elif full_path.stat().st_size == 0:
                errors.append(f"{demo_name}: empty {relative_file}")

        _check_balance_sheet(demo, errors)
        _check_vat_expected(demo, errors)

        if not any(e.startswith(demo_name) for e in errors):
            print(f"  OK  {demo_name}")

    print(f"\nDemos checked: {len(demos)}")
    print(f"Errors:        {len(errors)}")

    if errors:
        print("\nFAILED:")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("\nPASSED: all demo contracts passed")
        sys.exit(0)

if __name__ == "__main__":
    run()
