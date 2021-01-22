#!/usr/bin/env python

""" hamlog-agent: desktop agent software for Hamlog online logging platform """

from sys import exit as sys_exit
from PySide2.QtCore import QCoreApplication, QEvent
from PySide2.QtWidgets import QApplication
from qasync import QEventLoop
from asyncio import set_event_loop, create_task

from constants import APPLICATION_NAME, APPLICATION_ORGANIZATION_NAME, APPLICATION_ORGANIZATION_DOMAIN
from UI import MainWindow
from Hamlog import hamlog
from Utils import with_log

@with_log
class HamlogAgentApplication(QApplication):
    def event(self, ev):
        if ev.type() == QEvent.FileOpen:
            return hamlog.process_url_scheme(ev.url().toString())
        else:
            return super().event(ev)

if __name__ == '__main__':
    QCoreApplication.setApplicationName(APPLICATION_NAME)
    QCoreApplication.setOrganizationName(APPLICATION_ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(APPLICATION_ORGANIZATION_DOMAIN)
    application = HamlogAgentApplication()
    event_loop = QEventLoop(application)
    set_event_loop(event_loop)
    mainWindow = MainWindow()
    mainWindow.show()
    create_task(hamlog.start_listeners())
    with event_loop:
        sys_exit(event_loop.run_forever())
