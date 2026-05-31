#!/usr/bin/env python3
"""
CCFTS MCP loading test — verifies that key slugs resolve correctly and their
frontmatter contains expected fields. Does NOT require MCP runtime.
No external dependencies.
"""

import os
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"
LIST_FIELDS = {"depends_on", "entity_types", "entity_levels", "domains",
               "enterprise_scales", "triggers", "references", "slots", "sources"}

def parse_frontmatter(filepath):
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("---", 3)
    if end == -1:
        return None
    fm_text = text[3:end].strip()
    result = {}
    current_list_key = None
    current_list_values = []
    for line in fm_text.splitlines():
        line_stripped = line.strip()
        if current_list_key and line_stripped.startswith("- "):
            val = line_stripped[2:].strip().strip('"').strip("'")
            current_list_values.append(val)
            continue
        if current_list_key and not line_stripped.startswith("- "):
            result[current_list_key] = current_list_values
            current_list_key = None
            current_list_values = []
        if ":" not in line_stripped:
            continue
        key, _, value = line_stripped.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'").strip()
        if not value and key in LIST_FIELDS:
            current_list_key = key
            current_list_values = []
            continue
        if key in LIST_FIELDS:
            val = value.strip("[]")
            result[key] = [v.strip().strip('"').strip("'") for v in val.split(",") if v.strip()] if val else []
        elif key in ("jurisdiction",):
            result[key] = value
        elif key in ("is_base",):
            result[key] = value.lower() == "true"
        else:
            result[key] = value
    if current_list_key and current_list_values:
        result[current_list_key] = current_list_values
    return result

def safe_resolve(slug):
    for root, _, files in os.walk(SKILLS_DIR):
        for f in files:
            if f == f"{slug}.md":
                return Path(root) / f
    raise FileNotFoundError(slug)

# Key slugs to verify
TEST_SLUGS = {
    "ccfts-fr-all-rounding-rules": {
        "entity_levels": ["all"],
        "is_base": True,
        "min_slots": 3,
        "min_depends_on": 1,
        "min_references": 1,
    },
    "ccfts-fr-all-flash-report-workflow": {
        "entity_levels": ["all"],
        "is_base": True,
        "min_slots": 3,
        "min_depends_on": 2,
        "min_references": 3,
    },
    "ccfts-tax-all-vat-general-filing": {
        "entity_levels": ["all"],
        "is_base": True,
        "min_slots": 1,
        "min_depends_on": 1,
        "min_references": 2,
    },
    "ccfts-tax-intl-cross-border-withholding": {
        "entity_levels": ["intl"],
        "is_base": False,
        "min_depends_on": 1,
        "min_references": 1,
        "jurisdiction": "GLOBAL",
    },
    "ccfts-acct-small-enterprise-individual-contractor": {
        "entity_levels": ["small-enterprise"],
        "is_base": False,
        "min_depends_on": 1,
        "min_references": 2,
    },
}

def run():
    errors = []
    passed = 0

    for slug, checks in TEST_SLUGS.items():
        try:
            fp = safe_resolve(slug)
        except FileNotFoundError:
            errors.append(f"{slug}: file not found")
            continue

        fm = parse_frontmatter(fp)
        if not fm:
            errors.append(f"{slug}: frontmatter not parseable")
            continue

        name = fm.get("name", "")
        if name != slug:
            errors.append(f"{slug}: name mismatch '{name}'")

        entity_levels = fm.get("entity_levels", [])
        expected_levels = checks.get("entity_levels", [])
        if expected_levels and entity_levels != expected_levels:
            errors.append(f"{slug}: entity_levels {entity_levels} != expected {expected_levels}")

        if "is_base" in checks and fm.get("is_base") != checks["is_base"]:
            errors.append(f"{slug}: is_base {fm.get('is_base')} != expected {checks['is_base']}")

        slots = fm.get("slots", [])
        if len(slots) < checks.get("min_slots", 0):
            errors.append(f"{slug}: slots count {len(slots)} < expected min {checks['min_slots']}")

        depends_on = fm.get("depends_on", [])
        if len(depends_on) < checks.get("min_depends_on", 0):
            errors.append(f"{slug}: depends_on count {len(depends_on)} < expected min {checks['min_depends_on']}")

        references = fm.get("references", [])
        if len(references) < checks.get("min_references", 0):
            errors.append(f"{slug}: references count {len(references)} < expected min {checks['min_references']}")

        if "jurisdiction" in checks and fm.get("jurisdiction") != checks["jurisdiction"]:
            errors.append(f"{slug}: jurisdiction '{fm.get('jurisdiction')}' != expected '{checks['jurisdiction']}'")

        # Check that authority is present for intelligence skills
        if "intel" in slug and not fm.get("authority"):
            errors.append(f"{slug}: intelligence skill missing authority")

        if name == slug and not any(e.startswith(slug) for e in errors[-5:] if e):
            passed += 1
            print(f"  OK  {slug}")

    print(f"\nSlugs tested: {len(TEST_SLUGS)}")
    print(f"Passed:       {passed}")
    print(f"Errors:       {len(errors)}")

    if errors:
        print("\nFAILED:")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("\nPASSED: all MCP loading checks passed")
        sys.exit(0)

if __name__ == "__main__":
    run()
