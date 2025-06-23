import json, os, sys, time, pathlib, threading
from datetime import datetime
from typing import Dict, Tuple
# from win10toast import ToastNotifier
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

# ---------------- 사용자 설정 ---------------- #
# WATCH_PATH  = r"\\192.168.1.231\공유폴더"   # 감시할 네트워크 폴더
WATCH_PATH = '/content/sample_data'
INTERVAL    = 5                            # 초 단위 폴링 주기
STATE_FILE  = "state.json"                  # 이전 상태 저장 파일
TITLE       = "공용 폴더 변경 알림"          # 알림 제목
# ------------------------------------------- #

# toaster = ToastNotifier()                   # 윈도우 토스트 객체


def load_state() -> Dict[str, float]:
    """state.json → {파일: mtime} dict"""
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: Dict[str, float]) -> None:
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f)


def snapshot() -> Dict[str, float]:
    """폴더 내 모든 파일의 마지막 수정 시각(dict)"""
    result = {}
    for root, _, files in os.walk(WATCH_PATH):
        for name in files:
            full = os.path.join(root, name)
            try:
                result[full] = os.path.getmtime(full)
            except FileNotFoundError:
                # 스캔 도중 삭제될 수 있음 – 무시
                pass
    return result


def diff(prev: Dict[str, float], curr: Dict[str, float]) -> Tuple[list, list]:
    """prev→curr 비교 → (신규/갱신 파일 목록, 삭제 파일 목록)"""
    updated = []
    deleted = []

    # 추가 또는 수정
    for path, mtime in curr.items():
        if path not in prev or mtime > prev[path]:
            updated.append(path)

    # 삭제
    for path in prev:
        if path not in curr:
            deleted.append(path)

    return updated, deleted


def notify(files: list) -> None:
    """윈도우 토스트 알림"""
    if not files:
        return
    max_show = 5
    body = "\n".join([pathlib.Path(f).name for f in files[:max_show]])
    if len(files) > max_show:
        body += f"\n외 {len(files)-max_show}개 파일"
    # toaster.show_toast(TITLE, body, duration=5, threaded=True)
    print(files)


class PollHandler(FileSystemEventHandler):
    """watchdog용 핸들러 – 실제로는 안 쓰고 타이머에서 처리"""
    pass


def main_loop():
    prev_state = load_state()
    while True:
        curr_state = snapshot()
        updated, _ = diff(prev_state, curr_state)
        if updated:
            notify(updated)
        save_state(curr_state)
        prev_state = curr_state
        time.sleep(INTERVAL)


if __name__ == "__main__":
    # 네트워크 드라이브가 잠자기 상태일 때 끊기지 않도록 try/except
    try:
        t = threading.Thread(target=main_loop, daemon=True)
        t.start()
        # 메인 스레드는 watchdog으로 '폴링 감시' – 파일 수백만 개일 때 조금 더 효율적
        observer = PollingObserver(timeout=INTERVAL)
        observer.schedule(PollHandler(), WATCH_PATH, recursive=True)
        observer.start()
        t.join()  # 쓰레드가 끝날 때까지 대기
    except KeyboardInterrupt:
        observer.stop()
    observer.join()