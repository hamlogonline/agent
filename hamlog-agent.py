#!/usr/bin/env python

""" hamlog-agent: desktop agent software for Hamlog online logging platform """

from sys import exit as sys_exit

from PySide6 import QtCore, QtWidgets, QtGui

from UI import MainWindow

if __name__ == '__main__':
    application = QtWidgets.QApplication()
    mainWindow = MainWindow()
    sys_exit(application.exec_())
