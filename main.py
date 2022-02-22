import json
import sys
import time
import os

from watchdog.events import RegexMatchingEventHandler
from watchdog.observers import Observer
import requests
import base64


class CsvFilesWatcher:
    def __init__(self, src_path):
        self.__src_path = src_path
        self.__event_handler = FileSystemEventHandler()
        self.__event_observer = Observer()

    def run(self):
        self.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        self.__schedule()
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_path,
            recursive=True
        )


class FileSystemEventHandler(RegexMatchingEventHandler):
    # THUMBNAIL_SIZE = (128, 128)
    files_Regex = [r".*[^_thumbnail]\.csv$"]

    def __init__(self):
        super().__init__(self.files_Regex)

    def on_created(self, event):
        self.process(event)

    def process(self, event):
        filename, ext = os.path.splitext(event.src_path)
        filename = f"{filename}.csv"
        # encoded_file = base64.encodebytes(filename)
        files = {'upload_file': open(filename, 'rb')}
        print("\n\nFilename is =====================", filename)
        URL='http://localhost:8013/quality_control/measurement_sheet'
        r = requests.get(url=URL, files=files)
        print("FILE ____________________", r)

if __name__ == "__main__":
    src_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    CsvFilesWatcher(src_path).run()
