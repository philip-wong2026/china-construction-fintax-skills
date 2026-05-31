#!/usr/bin/env python3
"""
CCFTS demo directory structure test — checks that each demo has README.md
and the required input/expected/output subdirectories.
No external dependencies.
"""

import sys
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"

REQUIRED_DEMO_STRUCTURE = {
    "README.md": "file",
    "input": "dir",
    "expected": "dir",
    "output": "dir",
}

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

        if not errors or not any(e.startswith(demo_name) for e in errors[-4:]):
            print(f"  OK  {demo_name}")

    print(f"\nDemos checked: {len(demos)}")
    print(f"Errors:        {len(errors)}")

    if errors:
        print("\nFAILED:")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("\nPASSED: all demo directories complete")
        sys.exit(0)

if __name__ == "__main__":
    run()
