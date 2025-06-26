import time
from pathlib import PureWindowsPath
from datetime import datetime
from typing import Dict, Tuple
# from win10toast import ToastNotifier
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# WATCH_PATH = r'\\192.168.1.231\m24h-p01gm_gm_2ppm_pkg\GM 공용 폴더'
# WATCH_PATH = r'C:\Users\hj\Documents\000_개인\hjpy\test'
WATCH_PATH = r'./test'
SLEEP_TIME = 5
DEBOUNCE = 5
IGNORE_PATTERNS = ['~$*', '*@SynoEAStream', '*@SynoResource', '@eaDir/*']
ALARM_TYPES = {'created': '생성', 'modified': '수정', 'moved': '이동', 'deleted': '삭제'}


# toaster = ToastNotifier()


def notify(title, msg):
    # toaster.show_toast(title, msg, duration=5, threaded=True)
    return


class Handler(PatternMatchingEventHandler):
    def __init__(self, debounce=DEBOUNCE, notify_func=notify):
        super().__init__(ignore_patterns=IGNORE_PATTERNS, ignore_directories=True)
        self.debounce = debounce
        self._last_ts = {}
        self.notify = notify_func
    
    def _recent(self, path):
        now = time.time()
        last = self._last_ts.get(path, 0)
        self._last_ts[path] = now
        return (now - last) < self.debounce
    
    def _get_rel_path(self, src_path):
        base_dir = PureWindowsPath(WATCH_PATH)
        src_path = PureWindowsPath(src_path)
        try:
            return str(src_path.relative_to(base_dir))
        except ValueError:
            return str(src_path)
    
    def _log_and_notify(self, src_path, event_type):
        rel_str = self._get_rel_path(src_path)
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        print(f"🔔 {timestamp}", f"[{event_type}]", rel_str)
        title = '공용폴더 변경 알림'
        msg = f"{timestamp} {ALARM_TYPES[event_type]}\n{rel_str}"
        notify(title, msg)
    
    def on_created(self, event): self._log_and_notify(event.src_path, event.event_type)
    
    def on_deleted(self, event): self._log_and_notify(event.src_path, event.event_type)
    
    def on_moved(self, event): self._log_and_notify(event.src_path, event.event_type)
    
    def on_modified(self, event):
        if self._recent(event.src_path): return
        self._log_and_notify(event.src_path, event.event_type)


def setup_observer():
    observer = Observer()
    observer.schedule(Handler(), WATCH_PATH, recursive=True)
    return observer


def run_observer_loop(observer):
    try:
        print(f"👀    {WATCH_PATH}    감시 시작!")
        while True:
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    observer = setup_observer()
    observer.start()
    run_observer_loop(observer)


if __name__ == "__main__":
    main()
