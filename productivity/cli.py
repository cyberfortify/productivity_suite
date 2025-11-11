# productivity/cli.py
import click
from . import __version__
from .notes import add_note, list_notes, get_note, delete_note, edit_note, search_notes
from .timer import start_timer_nonblocking, stop_timer, active_timers, timer_history
from .organizer import organize_folder
from .calculator import calc
from .db import init_db

@click.group()
@click.version_option(version=__version__)
def cli():
    """Productivity Suite CLI"""
    init_db()

# Notes commands
@cli.group()
def notes():
    """Notes operations"""
    pass

@notes.command("add")
@click.argument("title")
@click.option("--body", "-b", default="", help="Body text for the note")
@click.option("--tags", "-t", multiple=True, help="Tags for the note")
@click.option("--db", default=None, help="Optional DB path (for testing)")
def notes_add(title, body, tags, db):
    nid = add_note(title, body, list(tags), db_path=db)
    click.echo(f"Note added with id: {nid}")

@notes.command("list")
@click.option("--limit", "-n", default=50)
@click.option("--db", default=None, help="Optional DB path (for testing)")
def notes_list(limit, db):
    rows = list_notes(limit, db_path=db)
    for r in rows:
        click.echo(f"[{r['id']}] {r['title']} — {r.get('tags','')}")

@notes.command("show")
@click.argument("note_id", type=int)
@click.option("--db", default=None, help="Optional DB path (for testing)")
def notes_show(note_id, db):
    r = get_note(note_id, db_path=db)
    if not r:
        click.echo("Note not found.")
        return
    click.echo(f"Title: {r['title']}\nBody:\n{r.get('body','')}")

@notes.command("delete")
@click.argument("note_id", type=int)
@click.option("--db", default=None, help="Optional DB path (for testing)")
def notes_delete(note_id, db):
    c = delete_note(note_id, db_path=db)
    if c:
        click.echo("Deleted.")
    else:
        click.echo("Not found.")

@notes.command("edit")
@click.argument("note_id", type=int)
@click.option("--title", default=None, help="New title")
@click.option("--body", default=None, help="New body")
@click.option("--tags", "-t", multiple=True, help="New tags (replaces existing)")
@click.option("--db", default=None, help="Optional DB path (for testing)")
def notes_edit(note_id, title, body, tags, db):
    tags_list = list(tags) if tags else None
    res = edit_note(note_id, title=title, body=body, tags=tags_list, db_path=db)
    if not res:
        click.echo("Note not found.")
    else:
        click.echo(f"Updated note [{note_id}].")

@notes.command("search")
@click.argument("query")
@click.option("--limit", "-n", default=50)
@click.option("--db", default=None, help="Optional DB path (for testing)")
def notes_search(query, limit, db):
    rows = search_notes(query, db_path=db, limit=limit)
    for r in rows:
        click.echo(f"[{r['id']}] {r['title']} — {r.get('tags','')}")

# Timer group (non-blocking)
@cli.group()
def timer():
    """Timer operations (non-blocking)"""
    pass

@timer.command("start")
@click.argument("seconds", type=int)
@click.option("--label", "-l", default=None)
def timer_start(seconds, label):
    """Start a non-blocking timer for SECONDS"""
    tid = start_timer_nonblocking(seconds, label)
    click.echo(f"Started timer: {tid}")

@timer.command("stop")
@click.argument("timer_id")
def timer_stop(timer_id):
    ok = stop_timer(timer_id)
    if ok:
        click.echo(f"Stopped timer: {timer_id}")
    else:
        click.echo(f"No active timer with id: {timer_id}")

@timer.command("active")
def timer_active():
    active = active_timers()
    if not active:
        click.echo("No active timers.")
        return
    for a in active:
        click.echo(f"{a['id']} — {a['label']} — {a['seconds']}s")

@timer.command("history")
@click.option("--limit", "-n", default=50)
def timer_history_cmd(limit):
    hist = timer_history(limit)
    for h in hist:
        click.echo(f"[{h['id']}] {h.get('label','')} — {h.get('duration_s',0)}s")

# Organizer (existing)
@cli.command()
@click.argument("source")
@click.option("--apply", is_flag=True, default=False, help="Move files instead of dry-run")
def organize(source, apply):
    """Organize files in SOURCE folder by extension"""
    actions = organize_folder(source, dry_run=not apply)
    if not apply:
        click.echo("Dry-run (no changes):")
    for src, tgt in actions:
        click.echo(f"{src.name} -> {tgt.name}")

# Calculator (existing)
@cli.command()
@click.argument("expr")
def calc_cmd(expr):
    """Evaluate a simple arithmetic expression"""
    try:
        res = calc(expr)
        click.echo(f"Result: {res}")
    except Exception as e:
        click.echo(f"Error: {e}")

if __name__ == '__main__':
    cli()
