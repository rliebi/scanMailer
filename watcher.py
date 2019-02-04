#!/usr/bin/env python
# coding=utf-8

import time
from threading import Timer
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from ruamel.yaml import YAML
from sendMail import SendMail
import io
import os
import sys
import psutil
import logging
yaml = YAML()

try:
    # Python 3
    import urllib.request as urllib
except ImportError:
    # Python 2
    import urllib2 as urllib


class ScanHanlder(PatternMatchingEventHandler):
    patterns = ["*.pdf", "*.jpg"]
    recipient = ''
    cc = ''
    timeout = 10000
    timer = None

    def __init__(self, recipient, cc=None, subject='', message=''):
        super(ScanHanlder, self).__init__()
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
        # the file will be processed there
        print 'starting event'
        if self.timer and self.timer.is_alive():
            self.timer.cancel()
        self.timer = Timer(30.0, self.send_mail, [event])
        self.timer.start()

    def send_mail(self, event):
        print 'executing event'
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        mail = SendMail(self.recipient, self.subject, self.message)
        mail.add_attachment(event.src_path)
        mail.set_cc(self.cc)
        mail.send_mail()


class PathHandler(PatternMatchingEventHandler):
    patterns = ["*.yaml", "*.yml", "*.py"]
    # def __init__(self):
    #     super(PathHandler, self).__init__()

    def on_modified(self, event):
        print 'paths.yaml modified.. reloading'
        try:
            p = psutil.Process(os.getpid())
            for handler in p.connections():
                os.close(handler.fd)
        except Exception, e:
            logging.error(e)
            print e
        python = sys.executable
        os.execl(python, python, *sys.argv)


if __name__ == '__main__':
    N2watch = Observer()
    threads = []
    # N2watch.schedule(PathHandler(), '.', recursive=True)
    # threads.append(N2watch)
    with io.open("paths.yaml", 'r', encoding='utf8') as paths:
        try:
            paths = (yaml.load(paths))
            if paths:
                for i in paths:
                    path = paths[i]
                    targetPath = str(path['path'])
                    N2watch.schedule(ScanHanlder(path['to'], path['cc'], path['subject'], path['message']), targetPath,
                                     recursive=True)
                    threads.append(N2watch)

        except OSError as exc:
            print(exc)
    N2watch.start()

    try:
        while True:
            time.sleep(1)
            # print threads
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
