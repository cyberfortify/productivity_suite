# tests/test_notes_timer.py
import os
import tempfile
import time
from productivity import notes, timer

def test_notes_add_edit_search_delete():
    # use a temp db file
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        # add
        nid = notes.add_note("Test Title", "Body content", tags=["a","b"], db_path=path)
        assert isinstance(nid, int)
        # list
        lst = notes.list_notes(db_path=path)
        assert len(lst) == 1
        # get
        got = notes.get_note(nid, db_path=path)
        assert got["title"] == "Test Title"
        # edit
        notes.edit_note(nid, title="New Title", body=None, tags=None, db_path=path)
        got2 = notes.get_note(nid, db_path=path)
        assert got2["title"] == "New Title"
        # search
        res = notes.search_notes("New", db_path=path)
        assert any(r["id"] == nid for r in res)
        # delete
        c = notes.delete_note(nid, db_path=path)
        assert c == 1
        lst2 = notes.list_notes(db_path=path)
        assert len(lst2) == 0
    finally:
        os.remove(path)

def test_timer_nonblocking_and_history():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        # point DB to temp file for isolation
        os.environ["PRODUCTIVITY_DB"] = path
        # start a short timer
        tid = timer.start_timer_nonblocking(1, label="t1")
        assert isinstance(tid, str)
        # there should be an active timer
        act = timer.active_timers()
        assert any(a["id"] == tid for a in act)
        # wait for it to finish
        time.sleep(1.5)
        # active should no longer contain it
        act2 = timer.active_timers()
        assert not any(a["id"] == tid for a in act2)
        # history should contain at least one entry
        hist = timer.timer_history()
        assert any(h.get("label","") == "t1" for h in hist)
    finally:
        # cleanup
        os.remove(path)
        os.environ.pop("PRODUCTIVITY_DB", None)
