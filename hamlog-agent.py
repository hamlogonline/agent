#!/usr/bin/env python

""" hamlog-agent: desktop agent software for Hamlog online logging platform """

from sys import exit as sys_exit
from PySide6.QtWidgets import QApplication
from UI import MainWindow

if __name__ == '__main__':
    application = QApplication()
    mainWindow = MainWindow()
    mainWindow.show()
    sys_exit(application.exec_())
