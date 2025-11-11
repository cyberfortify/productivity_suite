# productivity/db.py
import sqlite3
from pathlib import Path
from typing import Optional
import os

# Database location can be overridden by PRODUCTIVITY_DB env var (useful for tests)
_DEFAULT_DB_PATH = Path.home() / ".productivity_suite.db"
DB_PATH = Path(os.environ.get("PRODUCTIVITY_DB", str(_DEFAULT_DB_PATH)))

def get_conn(path: Optional[Path] = None):
    p = Path(path) if path else DB_PATH
    conn = sqlite3.connect(str(p), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(path: Optional[Path] = None):
    conn = get_conn(path)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        body TEXT,
        tags TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS timer_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        label TEXT,
        start_at TEXT,
        end_at TEXT,
        duration_s INTEGER
    )
    ''')
    conn.commit()
    return conn
