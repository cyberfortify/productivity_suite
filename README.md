# 🧠 Personal Productivity Suite — CLI + Web

A full-featured **Productivity Suite** built in **Python** during my **Month 1 Internship at The Developers Arena**.  
It includes both **Command-Line Tools** and a **Modern FastAPI Web Dashboard** for managing notes, timers, calculator, and file organization — all built from scratch.


## 🚀 Features

### 🖥️ CLI Tools
- **Notes Manager** → Add, Edit, Search, Delete notes stored in SQLite  
- **Timer Utility** → Non-blocking background timers with live updates  
- **Calculator** → Safe arithmetic evaluator  
- **File Organizer** → Categorizes and moves files by type (preview & apply)  

### 🌐 Web Application (FastAPI + Tailwind + HTMX)
- **Responsive Web UI** (desktop & mobile friendly)  
- **Live Countdown Timers** that update in real time (`5s → 4s → 3s`)  
- **HTMX-based Dynamic Updates** (Notes search, Organizer preview, etc.)  
- **Toast Notifications** for all user actions  
- **Modern Tailwind UI** with clean layout and color scheme  


## 🧩 Tech Stack

```
| Layer | Technology Used |
|:------|:----------------|
| Backend | **Python**, **FastAPI**, **SQLite**, **Threading**, **Jinja2** |
| Frontend | **Tailwind CSS**, **HTMX**, **Vanilla JS** |
| Testing | **pytest** |
| Tools | **Uvicorn**, **Virtualenv**, **Git**, **GitHub Actions** |
````


## 📁 Folder Structure

```

productivity_suite/
├── productivity/              # CLI modules (notes, timer, calc, organizer)
│   ├── notes.py
│   ├── timer.py
│   ├── calculator.py
│   ├── organizer.py
│   └── utils.py
│
├── productivity_web/          # FastAPI web app
│   ├── app/
│   │   ├── main.py
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── notes_*.html
│   │   │   ├── timer.html
│   │   │   ├── calc.html
│   │   │   └── organizer.html
│   │   └── static/
│   └── run_web.ps1
│
├── tests/                     # pytest test suite
│   └── test_notes_timer.py
│
├── requirements.txt
├── .gitignore
├── README.md
├── LICENSE
└── run_cli.ps1

````



## ⚙️ Setup Instructions

### 🐍 1. Create and activate a virtual environment
```bash
python -m venv venv
# Activate (Windows PowerShell)
.\venv\Scripts\activate
````

### 📦 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 🧠 3. Run tests

```bash
pytest -q
```

### 🌐 4. Start the FastAPI web app

```bash
cd productivity_web
uvicorn app.main:app --reload
```

Now open [http://127.0.0.1:8000](http://127.0.0.1:8000) 🎉


## 🧠 CLI Usage (Optional)

Run the command-line version:

```bash
python -m productivity.cli
```

Example commands:

```
> notes add --title "Daily Plan" --body "Focus on Flask & API"
> timer start --seconds 60 --label "Short Break"
> calc "5*(2+3)"
> organizer preview --path "Downloads"
```


## 🧪 GitHub Actions CI

This repo includes a workflow at `.github/workflows/python-app.yml`
Every push automatically runs tests across Python 3.10 and 3.11.


## 🧑‍💻 Developer

**Aditya Vishwakarma**
B.Sc. IT Graduate | Python & Full Stack Developer
🔗 [GitHub](https://github.com/cyberfortify) • [LinkedIn](https://linkedin.com/in/imadityavk)


## ⚖️ License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
