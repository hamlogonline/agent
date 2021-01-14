#!/usr/bin/env python

""" hamlog-agent: desktop agent software for Hamlog online logging platform """

from sys import exit as sys_exit
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication
from qasync import QEventLoop
from asyncio import set_event_loop

from constants import APPLICATION_NAME, APPLICATION_ORGANIZATION_NAME, APPLICATION_ORGANIZATION_DOMAIN

from UI import MainWindow

if __name__ == '__main__':
    QCoreApplication.setApplicationName(APPLICATION_NAME)
    QCoreApplication.setOrganizationName(APPLICATION_ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(APPLICATION_ORGANIZATION_DOMAIN)
    application = QApplication()
    event_loop = QEventLoop(application)
    set_event_loop(event_loop)
    mainWindow = MainWindow()
    mainWindow.show()
    with event_loop:
        sys_exit(event_loop.run_forever())
