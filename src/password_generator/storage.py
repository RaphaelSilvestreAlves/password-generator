from __future__ import annotations
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime, UTC
from typing import List


@dataclass
class Entry:
    password: str
    created_at: str

    @classmethod
    def create(cls, password: str) -> Entry:
        return cls(password=password, created_at=datetime.now(UTC).isoformat())


class Storage:
    def __init__(self, path: str | Path = "passwords.json"):
        self.path = Path(path)

    def _read_file(self) -> list[dict]:
        if not self.path.exists() or self.path.stat().st_size == 0:
            return []
        try:
            with self.path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def load(self) -> List[Entry]:
        return [Entry(**item) for item in self._read_file()]

    def save(self, entry: Entry) -> None:
        entries = self._read_file()
        entries.append(asdict(entry))
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
