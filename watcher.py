import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import sys

from sendMail import SendMail

try:
    # Python 3
    import urllib.request as urllib
except ImportError:
    # Python 2
    import urllib2 as urllib


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.pdf", "*.jpg"]

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        print event.src_path, event.event_type  # print now only for degug
        mail = SendMail('remo@liebi.net')
        mail.add_attachment(event.src_path).send_mail()


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
