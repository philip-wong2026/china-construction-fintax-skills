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
    "demo-collection-clear-arrears": [
        "input/collection-ledger.csv",
        "expected/collection-priority.csv",
    ],
}

COLLECTION_RISK_LEVELS = {"黑色", "红色", "橙色", "黄色", "绿色"}


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
    vat_sum = sum(float(r["预缴增值税(万元)"]) for r in detail_rows)
    total_sum = sum(float(r["预缴合计(万元)"]) for r in detail_rows)
    if round(float(total_row["预缴增值税(万元)"]) - vat_sum, 6) != 0:
        errors.append(f"{demo_dir.name}: VAT total does not match detail VAT sum")
    if round(float(total_row["预缴合计(万元)"]) - total_sum, 6) != 0:
        errors.append(f"{demo_dir.name}: VAT grand total does not match detail sum")


def _parse_float(row, column, demo_name, errors):
    value = row.get(column)
    try:
        return float(value)
    except (TypeError, ValueError):
        project_id = row.get("项目编号", "unknown")
        errors.append(f"{demo_name}: invalid number in {project_id} column {column}: {value!r}")
        return None


def _check_collection_expected(demo_dir, errors):
    ledger_path = demo_dir / "input" / "collection-ledger.csv"
    priority_path = demo_dir / "expected" / "collection-priority.csv"
    if not ledger_path.exists() or not priority_path.exists():
        return

    with ledger_path.open(encoding="utf-8-sig", newline="") as f:
        ledger_rows = list(csv.DictReader(f))
    with priority_path.open(encoding="utf-8-sig", newline="") as f:
        priority_rows = list(csv.DictReader(f))

    if not ledger_rows or not priority_rows:
        errors.append(f"{demo_dir.name}: collection ledger or priority output is empty")
        return

    ledger_ids = {r.get("项目编号") for r in ledger_rows if r.get("项目编号")}
    priority_ids = {r.get("项目编号") for r in priority_rows if r.get("项目编号")}
    if ledger_ids != priority_ids:
        errors.append(
            f"{demo_dir.name}: collection priority project IDs do not match ledger "
            f"(missing={sorted(ledger_ids - priority_ids)}, extra={sorted(priority_ids - ledger_ids)})"
        )

    try:
        priorities = [int(r["优先序"]) for r in priority_rows]
    except (KeyError, ValueError) as exc:
        errors.append(f"{demo_dir.name}: invalid collection priority sequence ({exc})")
        priorities = []
    if priorities and priorities != list(range(1, len(priority_rows) + 1)):
        errors.append(f"{demo_dir.name}: collection priority sequence is not 1..N")

    for row in ledger_rows:
        balance = _parse_float(row, "应收账款余额(万元)", demo_dir.name, errors)
        not_due = _parse_float(row, "未到期(万元)", demo_dir.name, errors)
        overdue = _parse_float(row, "已到期未付(万元)", demo_dir.name, errors)
        retention = _parse_float(row, "质保金(万元)", demo_dir.name, errors)
        if None in (balance, not_due, overdue, retention):
            continue
        if round(balance - not_due - overdue - retention, 6) != 0:
            errors.append(
                f"{demo_dir.name}: collection balance mismatch for {row.get('项目编号')} "
                f"(balance={balance}, not_due+overdue+retention={not_due + overdue + retention})"
            )

    for row in priority_rows:
        risk = row.get("风险分层")
        if risk not in COLLECTION_RISK_LEVELS:
            errors.append(f"{demo_dir.name}: invalid risk level for {row.get('项目编号')}: {risk!r}")
        for column in ("建议动作", "升级路径", "人工复核事项"):
            if not row.get(column):
                errors.append(f"{demo_dir.name}: missing {column} for {row.get('项目编号')}")


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
        _check_collection_expected(demo, errors)

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
