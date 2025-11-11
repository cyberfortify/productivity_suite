# productivity/db_init.py
import sqlite3
from pathlib import Path
import os
import logging
from datetime import datetime

logger = logging.getLogger("productivity.db_init")

DEFAULT_DB = "/opt/render/project/src/productivity_data/productivity_suite.db"

def get_db_path():
    return os.environ.get("PRODUCTIVITY_DB", DEFAULT_DB)

def ensure_db_and_tables(db_path: str | None = None):
    """
    Ensure a sqlite DB file exists and required tables are present.
    Idempotent: safe to call at each startup.
    """
    db_path = db_path or get_db_path()
    p = Path(db_path)
    # ensure parent directories exist
    p.parent.mkdir(parents=True, exist_ok=True)

    created = False
    if not p.exists():
        logger.info("DB file not found, creating: %s", db_path)
        # create empty file (sqlite will create tables below)
        p.touch()
        created = True

    conn = sqlite3.connect(str(p))
    cur = conn.cursor()

    # NOTES table - simple schema used by the app/tests
    cur.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        tags TEXT DEFAULT '',
        created_at TEXT NOT NULL
    );
    """)

    # Timers history (optional) - keeps finished timers
    cur.execute("""
    CREATE TABLE IF NOT EXISTS timers_history (
        id TEXT PRIMARY KEY,
        label TEXT,
        start_ts REAL,
        end_ts REAL,
        duration_s INTEGER
    );
    """)

    # any other tables you rely on can be added here
    conn.commit()
    conn.close()
    if created:
        logger.info("DB created and tables initialized at %s", db_path)
    else:
        logger.info("DB exists; ensured tables present at %s", db_path)

    return str(p)
