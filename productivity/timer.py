# productivity/timer.py
import time
import threading
import uuid
from typing import Optional, Dict, Any, List
from .db import init_db
from .utils import now_iso, dict_from_row

# Manager for non-blocking timers
class TimerManager:
    def __init__(self):
        # running: id -> {thread, cancel_event, label, seconds, start_time}
        self.running: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def start(self, seconds: int, label: Optional[str] = None) -> str:
        timer_id = str(uuid.uuid4())
        cancel_event = threading.Event()
        thread = threading.Thread(target=self._worker, args=(timer_id, seconds, label, cancel_event), daemon=True)
        with self._lock:
            self.running[timer_id] = {"thread": thread, "cancel": cancel_event, "label": label, "seconds": seconds, "start_time": time.time()}
        thread.start()
        return timer_id

    def _worker(self, timer_id: str, seconds: int, label: Optional[str], cancel_event: threading.Event):
        start = time.time()
        try:
            # sleep in small intervals to allow cancellation
            elapsed = 0.0
            interval = 0.2
            while elapsed < seconds:
                if cancel_event.is_set():
                    print(f"Timer {timer_id} cancelled.")
                    return
                time.sleep(interval)
                elapsed = time.time() - start
        finally:
            end = time.time()
            duration = int(end - start)
            conn = init_db()
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO timer_sessions (label, start_at, end_at, duration_s) VALUES (?, ?, ?, ?)",
                    (label or "", now_iso(), now_iso(), duration)
                )
                conn.commit()
            finally:
                conn.close()
            with self._lock:
                self.running.pop(timer_id, None)
            print(f"Timer {timer_id} finished — duration {duration} seconds. Label: {label}")

    def stop(self, timer_id: str) -> bool:
        with self._lock:
            info = self.running.get(timer_id)
            if not info:
                return False
            info["cancel"].set()
            return True

    def list_active(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [
                {"id": tid, "label": info["label"], "seconds": info["seconds"], "started_at": info["start_time"]}
                for tid, info in self.running.items()
            ]

    def history(self, limit: int = 100) -> List[Dict[str, Any]]:
        conn = init_db()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM timer_sessions ORDER BY id DESC LIMIT ?", (limit,))
            return [dict_from_row(r) for r in cur.fetchall()]
        finally:
            conn.close()

# module-level manager
_manager = TimerManager()

def start_timer_nonblocking(seconds: int, label: Optional[str] = None) -> str:
    return _manager.start(seconds, label)

def stop_timer(timer_id: str) -> bool:
    return _manager.stop(timer_id)

def active_timers():
    return _manager.list_active()

def timer_history(limit: int = 100):
    return _manager.history(limit)
