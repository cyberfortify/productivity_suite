# productivity/db_init.py
import sqlite3
from pathlib import Path
import os
import logging

logger = logging.getLogger("productivity.db_init")
DEFAULT_DB = "/opt/render/project/src/productivity_data/productivity_suite.db"

def get_db_path():
    return os.environ.get("PRODUCTIVITY_DB", DEFAULT_DB)

def ensure_db_and_tables(db_path: str | None = None):
    db_path = db_path or get_db_path()
    p = Path(db_path)
    p.parent.mkdir(parents=True, exist_ok=True)

    created = False
    if not p.exists():
        logger.info("DB file not found, creating: %s", db_path)
        p.touch()
        created = True

    conn = sqlite3.connect(str(p))
    cur = conn.cursor()

    # Create table if missing (base schema)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        tags TEXT DEFAULT '',
        created_at TEXT NOT NULL
        -- DON'T include updated_at here to avoid altering if present; we handle below
    );
    """)

    # Ensure columns we expect exist, add them if not
    def ensure_column(table, column, column_def):
        cur.execute("PRAGMA table_info(%s);" % table)
        cols = [r[1] for r in cur.fetchall()]
        if column not in cols:
            logger.info("Adding missing column %s to %s", column, table)
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {column_def};")

    # Add updated_at column (text)
    ensure_column("notes", "updated_at", "updated_at TEXT")

    # Timers history table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS timers_history (
        id TEXT PRIMARY KEY,
        label TEXT,
        start_ts REAL,
        end_ts REAL,
        duration_s INTEGER
    );
    """)

    conn.commit()
    conn.close()

    if created:
        logger.info("DB created and tables initialized at %s", db_path)
    else:
        logger.info("DB exists; ensured tables/columns at %s", db_path)

    return str(p)
