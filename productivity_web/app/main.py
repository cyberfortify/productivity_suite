from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from productivity import notes as notes_service
from productivity import timer as timer_service
from productivity import calculator as calc_service
from productivity import organizer as organizer_service
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

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

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Notes pages
@app.get("/notes", response_class=HTMLResponse)
def notes_list(request: Request):
    items = notes_service.list_notes()
    return templates.TemplateResponse("notes_list.html", {"request": request, "notes": items})

@app.get("/notes/add", response_class=HTMLResponse)
def notes_add_form(request: Request):
    return templates.TemplateResponse("notes_add.html", {"request": request})

@app.post("/notes/add")
def notes_add(request: Request, title: str = Form(...), body: str = Form(""), tags: str = Form("")):
    tags_list = [t.strip() for t in tags.split(",")] if tags.strip() else []
    notes_service.add_note(title, body, tags=tags_list)
    return RedirectResponse(url="/notes", status_code=303)

@app.get("/notes/{note_id}", response_class=HTMLResponse)
def notes_show(request: Request, note_id: int):
    n = notes_service.get_note(note_id)
    return templates.TemplateResponse("notes_show.html", {"request": request, "note": n})

@app.get("/notes/{note_id}/edit", response_class=HTMLResponse)
def notes_edit_form(request: Request, note_id: int):
    n = notes_service.get_note(note_id)
    return templates.TemplateResponse("notes_edit.html", {"request": request, "note": n})

@app.post("/notes/{note_id}/edit")
def notes_edit(request: Request, note_id: int, title: str = Form(None), body: str = Form(None), tags: str = Form(None)):
    tags_list = [t.strip() for t in tags.split(",")] if tags is not None and tags.strip() else None
    notes_service.edit_note(note_id, title=title, body=body, tags=tags_list)
    return RedirectResponse(url=f"/notes/{note_id}", status_code=303)

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
