#!/usr/bin/env python3
"""
Minimal keyword-level QA checks for selected skills.

Each YAML file under tests/qa_pairs/ describes one skill and the keywords that
must or must not appear in that skill text. This is not semantic AI evaluation;
it is a lightweight guardrail for catching obvious content regressions.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
QA_DIR = Path(__file__).resolve().parent / "qa_pairs"

REQUIRED_FIELDS = {"skill_file", "question", "must_contain", "must_not_contain"}


def _strip_quotes(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _load_simple_yaml(path):
    data = {}
    current_key = None

    for line_no, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue

        stripped = line.strip()
        if stripped.startswith("- "):
            if current_key is None:
                raise ValueError(f"{path.name}:{line_no}: list item without a field")
            data.setdefault(current_key, []).append(_strip_quotes(stripped[2:]))
            continue

        if ":" not in stripped:
            raise ValueError(f"{path.name}:{line_no}: expected 'field: value'")

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        current_key = key
        if value:
            data[key] = _strip_quotes(value)
        else:
            data[key] = []

    return data


def _load_yaml(path):
    try:
        import yaml  # type: ignore
    except ImportError:
        return _load_simple_yaml(path)

    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: YAML root must be a mapping")
    return data


def _validate_case(path, errors):
    try:
        case = _load_yaml(path)
    except Exception as exc:
        errors.append(f"{path.name}: failed to parse YAML ({exc})")
        return

    missing_fields = sorted(REQUIRED_FIELDS - set(case))
    if missing_fields:
        errors.append(f"{path.name}: missing fields: {', '.join(missing_fields)}")
        return

    skill_file = case["skill_file"]
    skill_path = (REPO_ROOT / skill_file).resolve()
    skills_root = (REPO_ROOT / "skills").resolve()
    if skills_root not in skill_path.parents:
        errors.append(f"{path.name}: skill_file must be under skills/: {skill_file}")
        return
    if not skill_path.is_file():
        errors.append(f"{path.name}: skill file not found: {skill_file}")
        return

    must_contain = case.get("must_contain") or []
    must_not_contain = case.get("must_not_contain") or []
    if not isinstance(must_contain, list) or not isinstance(must_not_contain, list):
        errors.append(f"{path.name}: must_contain and must_not_contain must be lists")
        return

    text = skill_path.read_text(encoding="utf-8")
    for keyword in must_contain:
        if keyword not in text:
            errors.append(f"{path.name}: missing required keyword in {skill_file}: {keyword}")
    for keyword in must_not_contain:
        if keyword in text:
            errors.append(f"{path.name}: forbidden keyword appears in {skill_file}: {keyword}")


def run():
    if not QA_DIR.exists():
        print("SKIP: tests/qa_pairs/ directory does not exist")
        sys.exit(0)

    qa_files = sorted(list(QA_DIR.glob("*.yaml")) + list(QA_DIR.glob("*.yml")))
    if not qa_files:
        print("SKIP: no QA YAML files found under tests/qa_pairs/")
        sys.exit(0)

    errors = []
    for path in qa_files:
        _validate_case(path, errors)
        if not any(e.startswith(path.name) for e in errors):
            print(f"  OK  {path.name}")

    print(f"\nQA pairs checked: {len(qa_files)}")
    print(f"Errors:           {len(errors)}")

    if errors:
        print("\nFAILED:")
        for error in errors:
            print(f"  ✗ {error}")
        sys.exit(1)

    print("\nPASSED: all skill QA keyword checks passed")
    sys.exit(0)


if __name__ == "__main__":
    run()
