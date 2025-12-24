import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

class Memory:
    def __init__(self, path: Path):
        self.path = path
        self._load()

    def _load(self):
        if not self.path.exists():
            self.memories = []
            return
        self.memories = json.loads(self.path.read_text(encoding="utf-8"))

    def _save(self):
        self.path.write_text(json.dumps(self.memories, ensure_ascii=False, indent=2), encoding="utf-8")

    def add(self, text: str):
        item = {"text": text, "ts": datetime.now().isoformat(timespec="seconds")}
        self.memories.append(item)
        self._save()

    def recent(self, n=5) -> List[Dict[str, Any]]:
        return list(reversed(self.memories))[:n]
