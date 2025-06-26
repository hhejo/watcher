import platform

if platform.system() == "Windows":
    WATCH_PATH = r'\\192.168.1.231\m24h-p01gm_gm_2ppm_pkg\GM 공용 폴더'
elif platform.system() == "Darwin":
    WATCH_PATH = r'./test'
else:
    WATCH_PATH = r'./test'


SLEEP_TIME = 5
DEBOUNCE = 5
IGNORE_PATTERNS = ["~$*", "*@SynoEAStream", "*@SynoResource", "@eaDir/*"]
ALARM_TYPES = {"created": "생성", "modified": "수정", "moved": "이동", "deleted": "삭제"}