from datetime import datetime
from typing import Any

def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"

def dict_from_row(row: Any) -> dict:
    if row is None:
        return {}
    return {k: row[k] for k in row.keys()}
