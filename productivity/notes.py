# productivity/notes.py
from .db import get_conn, init_db
from .utils import now_iso, dict_from_row
from typing import List, Optional
import sqlite3

def add_note(title: str, body: str = "", tags: Optional[List[str]] = None, db_path: Optional[str] = None):
    conn = init_db(db_path)
    try:
        cur = conn.cursor()
        tags_str = ",".join(tags) if tags else ""
        cur.execute(
            "INSERT INTO notes (title, body, tags, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (title, body, tags_str, now_iso(), now_iso())
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

def list_notes(limit: int = 100, db_path: Optional[str] = None):
    conn = init_db(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM notes ORDER BY created_at DESC LIMIT ?", (limit,))
        return [dict_from_row(r) for r in cur.fetchall()]
    finally:
        conn.close()

def get_note(note_id: int, db_path: Optional[str] = None):
    conn = init_db(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        return dict_from_row(cur.fetchone())
    finally:
        conn.close()

def delete_note(note_id: int, db_path: Optional[str] = None):
    conn = init_db(db_path)
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()

def edit_note(note_id: int, title: Optional[str] = None, body: Optional[str] = None, tags: Optional[List[str]] = None, db_path: Optional[str] = None):
    conn = init_db(db_path)
    try:
        cur = conn.cursor()
        # Fetch existing
        cur.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        row = cur.fetchone()
        if not row:
            return None
        existing = dict_from_row(row)
        new_title = title if title is not None else existing.get("title")
        new_body = body if body is not None else existing.get("body")
        new_tags = ",".join(tags) if tags is not None else existing.get("tags", "")
        cur.execute(
            "UPDATE notes SET title = ?, body = ?, tags = ?, updated_at = ? WHERE id = ?",
            (new_title, new_body, new_tags, now_iso(), note_id)
        )
        conn.commit()
        # fetch updated
        cur.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        return dict_from_row(cur.fetchone())
    finally:
        conn.close()

def search_notes(query: str, db_path: Optional[str] = None, limit: int = 100):
    conn = init_db(db_path)
    try:
        cur = conn.cursor()
        like = f"%{query}%"
        cur.execute(
            "SELECT * FROM notes WHERE title LIKE ? OR body LIKE ? OR tags LIKE ? ORDER BY created_at DESC LIMIT ?",
            (like, like, like, limit)
        )
        return [dict_from_row(r) for r in cur.fetchall()]
    finally:
        conn.close()
