from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from ai_pm_research_agent.storage.models import CandidateItem
from ai_pm_research_agent.utils.text import stable_fingerprint


SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
  fingerprint TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  source TEXT NOT NULL,
  url TEXT NOT NULL,
  category TEXT NOT NULL,
  published_at TEXT,
  author TEXT,
  raw_text TEXT,
  abstract TEXT,
  metadata_json TEXT
);
"""


class ItemStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.db_path)
        self.connection.execute(SCHEMA)

    def upsert_items(self, items: list[CandidateItem]) -> None:
        rows = []
        for item in items:
            rows.append(
                (
                    stable_fingerprint(item.title, item.url),
                    item.title,
                    item.source,
                    item.url,
                    item.category,
                    item.published_at.isoformat() if item.published_at else None,
                    item.author,
                    item.raw_text,
                    item.abstract,
                    json.dumps(item.metadata),
                )
            )
        self.connection.executemany(
            """
            INSERT OR REPLACE INTO items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()
