#!/usr/bin/env python3
"""
CCFTS skill integrity test — checks frontmatter parseability, filename==name,
depends_on/references resolvability, and quality fields for all skill files.
No external dependencies.
"""

import os
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"
SKIP_FILES = {"README.md", "_template-skill.md"}
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

def run():
    all_files = [p for p in sorted(SKILLS_DIR.rglob("*.md")) if p.name not in SKIP_FILES]
    errors = []
    all_slugs = set()

    for fp in all_files:
        relpath = str(fp.relative_to(SKILLS_DIR))
        fm = parse_frontmatter(fp)

        # Check 1: frontmatter parseable
        if fm is None:
            errors.append(f"{relpath}: frontmatter not parseable")
            continue

        name = fm.get("name", "")
        all_slugs.add(name)

        # Check 2: has quality_tier
        if "quality_tier" not in fm:
            errors.append(f"{relpath}: missing quality_tier")

        # Check 3: has verified_by
        if "verified_by" not in fm:
            errors.append(f"{relpath}: missing verified_by")

        # Check 4: filename stem == name
        if name and fp.stem != name:
            errors.append(f"{relpath}: stem '{fp.stem}' != name '{name}'")

        # Check 5: category must be valid
        category = fm.get("category", "")
        valid_categories = {"foundation", "financial-reporting", "accounting", "tax", "analysis", "management", "intelligence"}
        if category and category not in valid_categories:
            errors.append(f"{relpath}: unknown category '{category}'")

    # Check 6: cross-references resolvable
    for fp in all_files:
        fm = parse_frontmatter(fp)
        if not fm:
            continue
        relpath = str(fp.relative_to(SKILLS_DIR))
        for field in ("depends_on", "references"):
            deps = fm.get(field, [])
            if isinstance(deps, str):
                deps = [deps]
            for dep in deps:
                dep = dep.strip()
                if not dep or dep == "null":
                    continue
                if dep not in all_slugs:
                    errors.append(f"{relpath}: {field} '{dep}' not found")

    print(f"Files checked: {len(all_files)}")
    print(f"Known slugs:   {len(all_slugs)}")
    print(f"Errors:        {len(errors)}")

    if errors:
        print("\nFAILED:")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("\nPASSED: all integrity checks passed")
        sys.exit(0)

if __name__ == "__main__":
    run()
