from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"File modified: {event.src_path}")

    def on_created(self, event):
        if not event.is_directory:
            print(f"File created: {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"File deleted: {event.src_path}")

from watchdog.observers import Observer

if __name__ == "__main__":
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path="data/", recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
