# notify.py
import platform


def get_notifier():
    system = platform.system()
    if system == "Windows":
        try:
            from windows_toasts import WindowsToaster, Toast
            toaster = WindowsToaster("Watcher")
            def notify(title, body):
                toast = Toast([title, body])
                toaster.show_toast(toast)
        except ImportError:
            def notify(title, body):
                print(f"[알림] {title}: {body} (WindowsToaster 미설치)")
    elif system == "Darwin":
        try:
            import os, pync
            os.environ["TERMINAL_NOTIFIER_PATH"] = "/opt/homebrew/bin/terminal-notifier"
            def notify(title, body):
                pync.notify(body, title=title)
        except ImportError:
            def notify(title, body):
                print(f"[알림] {title}: {body} (pync 미설치)")
    else:
        def notify(title, body):
            print(f"🔔 {title}: {body}")
    return notify
