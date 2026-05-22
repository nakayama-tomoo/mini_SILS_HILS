from __future__ import annotations

import json
from pathlib import Path


def load_version(version_id: str) -> dict:

    repo_root = (
        Path(__file__)
        .resolve()
        .parents[4]
    )

    version_file = (
        repo_root
        / "versions"
        / f"{version_id}.json"
    )

    with version_file.open(
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)
