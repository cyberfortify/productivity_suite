# Productivity Suite - Web App (Phase 2 Scaffold)

This scaffold reuses the existing `productivity` Python package (CLI) and exposes simple web pages
for Notes and Timer using FastAPI and Jinja2 templates.

## Run locally

1. From project root, activate your venv (same one where CLI lives).
2. Install web requirements:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   uvicorn app.main:app --reload
   ```
4. Open http://127.0.0.1:8000 in your browser.

Notes and timers use the same DB (`~/.productivity_suite.db`) by default.

## Next steps
- Add API endpoints (JSON) for AJAX/HTMX.
- Add authentication.
- Add nicer UI with Tailwind or React.
