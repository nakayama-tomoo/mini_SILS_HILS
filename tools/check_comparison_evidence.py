from __future__ import annotations

from pathlib import Path
import sys


REQUIRED_FILES = [
    Path(
        "artifacts/phase20-sils-hils-comparison/comparison_summary.txt"
    ),
]


def main() -> int:
    missing = []

    for file_path in REQUIRED_FILES:
        if not file_path.exists():
            missing.append(file_path)

    if missing:
        for file_path in missing:
            print(f"[FAIL] Missing: {file_path}")

        return 1

    print("[PASS] Comparison evidence exists.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

