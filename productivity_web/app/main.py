from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from productivity import notes as notes_service
from productivity import timer as timer_service
from productivity import calculator as calc_service
from productivity import organizer as organizer_service
from productivity import db_init
from pathlib import Path
import os
import logging
import sys
from fastapi import HTTPException
from fastapi.responses import PlainTextResponse
import sqlite3

# configure logging to stdout so Render captures it
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("productivity_web")

app = FastAPI(title="Productivity Suite (Web)")

# Compute paths relative to this file (productivity_web/app/main.py)
BASE_DIR = Path(__file__).resolve().parent   # points to productivity_web/app
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# Ensure static directory exists (create empty dir if missing so StaticFiles won't crash)
if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)

# Use explicit string paths to avoid problems
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Mount static using absolute/robust path
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Global exception handler: log full traceback and return friendly message
@app.exception_handler(Exception)
async def all_exception_handler(request, exc):
    # log full traceback
    logger.exception("Unhandled exception for request %s %s", request.method, request.url)
    # return a friendly PlainTextResponse (avoids exposing internals to users)
    return PlainTextResponse("Internal Server Error (logged). Please check server logs.", status_code=500)

@app.on_event("startup")
def startup_event():
    try:
        db_path = db_init.get_db_path()
        db_init.ensure_db_and_tables(db_path)
        logger.info("DB initialization check OK: %s", db_path)
    except Exception:
        logger.exception("Failed to initialize DB on startup")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
# -----------------------
# Notes pages (replace existing notes block with this)
# -----------------------

@app.get("/notes", response_class=HTMLResponse)
def notes_list(request: Request):
    items = notes_service.list_notes()
    return templates.TemplateResponse("notes_list.html", {"request": request, "notes": items})


# Show add form (GET) — MUST appear before /notes/{note_id}
@app.get("/notes/add", response_class=HTMLResponse)
def notes_add_form(request: Request):
    # render the add form (template can accept title/body/tags/error if present)
    return templates.TemplateResponse("notes_add.html", {"request": request, "title": "", "body": "", "tags": "", "error": None})


# Add note (POST)
@app.post("/notes/add", response_class=HTMLResponse)
def notes_add(request: Request, title: str = Form(...), body: str = Form(""), tags: str = Form("")):
    """
    Robust notes add handler: uses the shared PRODUCTIVITY_DB path, logs exceptions,
    and returns a friendly page on error instead of a raw 500.
    """
    try:
        # sanitize inputs
        title = (title or "").strip()
        body = (body or "").strip()
        # normalize tags: accept comma-separated string and convert to list
        tags_list = None
        if tags is not None:
            tags = tags.strip()
            tags_list = [t.strip() for t in tags.split(",")] if tags else []

        # Use the same DB path used by startup initializer
        from productivity import db_init
        db_path = db_init.get_db_path()

        # Call service explicitly with db_path to avoid ambiguity
        # some implementations accept db_path kwarg
        try:
            nid = notes_service.add_note(title, body, tags=tags_list, db_path=db_path)
        except TypeError:
            # fallback if service signature doesn't accept db_path
            nid = notes_service.add_note(title, body, tags=tags_list)

        logger.info("Added note id=%s title=%s", nid, title)
        # redirect to notes list on success
        return RedirectResponse(url="/notes", status_code=303)

    except Exception:
        # log full traceback to server logs (Render will capture this)
        logger.exception("Failed to add note: title=%s", title)
        # show the add form again with a friendly error message and prefilled inputs
        return templates.TemplateResponse(
            "notes_add.html",
            {
                "request": request,
                "title": title,
                "body": body,
                "tags": tags,
                "error": "Failed to add note. The error was logged on the server.",
            },
            status_code=500,
        )


# Show single note (note_id must be int)
@app.get("/notes/{note_id}", response_class=HTMLResponse)
def notes_show(request: Request, note_id: int):
    n = notes_service.get_note(note_id)
    return templates.TemplateResponse("notes_show.html", {"request": request, "note": n})


# Edit form
@app.get("/notes/{note_id}/edit", response_class=HTMLResponse)
def notes_edit_form(request: Request, note_id: int):
    n = notes_service.get_note(note_id)
    return templates.TemplateResponse("notes_edit.html", {"request": request, "note": n})


# Edit POST
@app.post("/notes/{note_id}/edit", response_class=HTMLResponse)
def notes_edit(request: Request, note_id: int, title: str = Form(None), body: str = Form(None), tags: str = Form(None)):
    tags_list = [t.strip() for t in tags.split(",")] if tags is not None and tags.strip() else None
    notes_service.edit_note(note_id, title=title, body=body, tags=tags_list)
    return RedirectResponse(url=f"/notes/{note_id}", status_code=303)


# Delete
@app.post("/notes/{note_id}/delete")
def notes_delete(request: Request, note_id: int):
    notes_service.delete_note(note_id)
    return RedirectResponse(url="/notes", status_code=303)


# HTMX: notes search (returns partial)
@app.get("/notes/search", response_class=HTMLResponse)
def notes_search(request: Request, q: str = ""):
    if q:
        items = notes_service.search_notes(q)
    else:
        items = notes_service.list_notes()
    return templates.TemplateResponse("notes_list_partial.html", {"request": request, "notes": items})

# Timer endpoints (pages)
@app.get("/timer", response_class=HTMLResponse)
def timer_page(request: Request):
    active = timer_service.active_timers()
    history = timer_service.timer_history(limit=50)
    return templates.TemplateResponse("timer.html", {"request": request, "active": active, "history": history})

@app.post("/timer/start", response_class=HTMLResponse)
def timer_start(request: Request, seconds: int = Form(...), label: str = Form(None)):
    # start timer (non-blocking)
    tid = timer_service.start_timer_nonblocking(int(seconds), label=label)
    # prepare updated page context so user sees active timers immediately
    active = timer_service.active_timers()
    history = timer_service.timer_history(limit=50)
    # return the timer page with a message that triggers a toast
    return templates.TemplateResponse("timer.html", {"request": request, "active": active, "history": history, "message": f"Started timer {tid}"})

@app.post("/timer/stop", response_class=HTMLResponse)
def timer_stop(request: Request, timer_id: str = Form(...)):
    stopped = timer_service.stop_timer(timer_id)
    active = timer_service.active_timers()
    history = timer_service.timer_history(limit=50)
    msg = f"Stopped timer {timer_id}" if stopped else f"No active timer {timer_id}"
    return templates.TemplateResponse("timer.html", {"request": request, "active": active, "history": history, "message": msg})

# JSON endpoint for polling active timers (used by client-side JS)
@app.get("/timer/active-json")
def timer_active_json():
    active = timer_service.active_timers()
    history = timer_service.timer_history(limit=10)
    # We can optionally return HTML for the history rows to make client update easier
    # Render history rows server-side:
    history_html = ""
    for h in history:
        history_html += f"<tr class='border-t'><td class='py-2'>{h.get('id')}</td><td class='py-2'>{h.get('label')}</td><td class='py-2'>{h.get('duration_s')} s</td></tr>"
    return JSONResponse({"active": active, "history_html": history_html})

# Calculator pages (HTMX-enabled)
@app.get("/calc", response_class=HTMLResponse)
def calc_page(request: Request):
    return templates.TemplateResponse("calc.html", {"request": request})

@app.post("/calc", response_class=HTMLResponse)
def calc_eval(request: Request, expr: str = Form(...)):
    try:
        result = calc_service.calc(expr)
        return templates.TemplateResponse("calc_result_partial.html", {"request": request, "result": result})
    except Exception as e:
        return templates.TemplateResponse("calc_result_partial.html", {"request": request, "error": str(e)})

# Organizer pages (HTMX-enabled preview/apply)
@app.get("/organizer", response_class=HTMLResponse)
def organizer_page(request: Request):
    return templates.TemplateResponse("organizer.html", {"request": request, "actions": None, "message": None})

@app.post("/organizer/preview", response_class=HTMLResponse)
def organizer_preview(request: Request, source: str = Form(...)):
    try:
        actions = organizer_service.organize_folder(source, dry_run=True)
        actions_readable = [(str(src.name), str(tgt.name)) for src, tgt in actions]
        return templates.TemplateResponse("organizer_actions_partial.html", {"request": request, "actions": actions_readable, "message": "Preview (dry-run) — no changes applied."})
    except Exception as e:
        return templates.TemplateResponse("organizer_actions_partial.html", {"request": request, "actions": None, "message": f"Error: {e}"})

@app.post("/organizer/apply", response_class=HTMLResponse)
def organizer_apply(request: Request, source: str = Form(...)):
    try:
        actions = organizer_service.organize_folder(source, dry_run=False)
        actions_readable = [(str(src.name), str(tgt.name)) for src, tgt in actions]
        return templates.TemplateResponse("organizer_actions_partial.html", {"request": request, "actions": actions_readable, "message": "Organizer applied successfully."})
    except Exception as e:
        return templates.TemplateResponse("organizer_actions_partial.html", {"request": request, "actions": None, "message": f"Error: {e}"})


@app.get("/health", response_class=JSONResponse)
def health():
    # check DB path from env (fall back to default)
    db_path = os.environ.get("PRODUCTIVITY_DB", "/opt/render/project/src/productivity_data/productivity_suite.db")
    info = {"ok": True, "db_path": db_path, "db_exists": False, "tables": None}
    try:
        p = Path(db_path)
        info["db_exists"] = p.exists()
        # If DB exists, try to list tables
        if p.exists():
            conn = sqlite3.connect(str(p))
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            rows = cur.fetchall()
            info["tables"] = [r[0] for r in rows]
            conn.close()
    except Exception as e:
        logger.exception("Health-check DB error")
        info["ok"] = False
        info["error"] = str(e)
    return info