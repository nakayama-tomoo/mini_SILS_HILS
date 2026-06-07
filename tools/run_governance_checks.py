from __future__ import annotations

import subprocess
import sys


COMMANDS = [
    ["python", "tools/check_traceability.py"],
    ["python", "tools/generate_evidence_manifest.py"],
    ["python", "tools/generate_coverage_matrix.py"],
    ["python", "tools/check_coverage.py"],
    ["python", "tools/generate_version_matrix.py"],
    ["python", "tools/run_v2_validation.py"],
    ["python", "tools/validate_traceability_consistency.py"],
    ["python", "tools/check_comparison_evidence.py"],
]


def main() -> int:
    for command in COMMANDS:
        print("")
        print("RUN:", " ".join(command))

        result = subprocess.run(command)

        if result.returncode != 0:
            print("")
            print("Governance checks: FAIL")
            return result.returncode

    print("")
    print("Governance checks: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
