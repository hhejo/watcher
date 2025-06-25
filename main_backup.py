from time import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler


WATCH_PATH = r'./test'


class Handler(FileSystemEventHandler):
    def _log(self, event: FileSystemEvent, dest=''):
        print(time.datetime.now(), event.event_type, event.is_directory, event.src_path, dest)
    def on_created(self, e: FileSystemEvent): self._log(e)
    def on_modified(self, e: FileSystemEvent): self._log(e)
    def on_deleted(self, e: FileSystemEvent): self._log(e)
    def on_moved(self, e: FileSystemEvent): self._log(e)


if __name__ == '__main__':
    observer = Observer()
    observer.schedule(Handler(), path=WATCH_PATH, recursive=True)
    observer.start()
    print('start')
