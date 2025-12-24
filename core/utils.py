import json, logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger("jarvis")
logging.basicConfig(level=getattr(logging, "INFO"), format="%(asctime)s %(levelname)s: %(message)s")

def load_config():
    p = Path("config.json")
    if not p.exists():
        raise FileNotFoundError("config.json not found. Please copy and edit the template.")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def ensure_data_files():
    Path("data").mkdir(exist_ok=True, parents=True)
    mem = Path("data/memory.json")
    if not mem.exists():
        mem.write_text("[]", encoding="utf-8")
    Path("data/logs").mkdir(exist_ok=True, parents=True)

def log_event(msg: str):
    ts = datetime.now().isoformat(timespec="seconds")
    p = Path("data/logs/activity.log")
    with p.open("a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")
    logger.info(msg)
