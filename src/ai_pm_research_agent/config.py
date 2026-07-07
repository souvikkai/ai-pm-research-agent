from __future__ import annotations

from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_yaml(path: str | Path) -> dict[str, Any]:
    import yaml

    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_sources_config(project_root: Path = PROJECT_ROOT) -> dict[str, Any]:
    return load_yaml(project_root / "config" / "sources.yaml")


def load_scoring_config(project_root: Path = PROJECT_ROOT) -> dict[str, Any]:
    return load_yaml(project_root / "config" / "scoring.yaml")
