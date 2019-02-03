# coding=utf-8
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import yaml

from sendMail import SendMail

try:
    # Python 3
    import urllib.request as urllib
except ImportError:
    # Python 2
    import urllib2 as urllib


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.pdf", "*.jpg"]
    recipient = ''
    cc = ''

    def __init__(self, recipient, cc=None, subject='', message=''):
        super(MyHandler, self).__init__()
        self.subject = subject
        self.message = message
        if cc is None:
            cc = []
        self.recipient = recipient
        self.cc = cc

    def set_recipient(self, recipient):
        self.recipient = recipient

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
        mail = SendMail(self.recipient, self.subject, self.message)
        mail.add_attachment(event.src_path)
        mail.set_cc(self.cc)
        mail.send_mail()


if __name__ == '__main__':
    N2watch = Observer()
    threads = []
    with open("paths.yaml", 'r') as paths:
        try:
            paths = (yaml.load(paths))
            for i in paths:
                path = paths[i]
                targetPath = str(path['path'])
                print targetPath
                N2watch.schedule(MyHandler(path['to'], path['cc'], path['subject'], path['message']), targetPath,
                                 recursive=True)
                threads.append(N2watch)
        except yaml.YAMLError as exc:
            print(exc)

    N2watch.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        N2watch.stop()
    N2watch.join()

    # args = sys.argv[1:]
    # observer = Observer()
    # observer.schedule(MyHandler(), path=args[0] if args else '.')
    # observer.start()
    #
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     observer.stop()
    #
    # observer.join()
