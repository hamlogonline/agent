
from sys import platform as sys_platform

from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QApplication, QStyle, QMenu
from PySide6.QtGui import QAction

class TrayedMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        if sys_platform != 'darwin':
            self.tray_icon.setContextMenu(self.create_tray_icon_context_menu())
        self.tray_icon.activated.connect(self.show)
        self.tray_icon.show()

    def create_tray_icon_context_menu(self):
        tray_menu = QMenu()
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        quit_action = QAction("Exit", self)
        qApplication = QApplication.instance()
        quit_action.triggered.connect(qApplication.quit)
        tray_menu.addAction(quit_action)
        tray_menu.addSeparator()
        return tray_menu

    def show(self):
        super().show()
        self.activateWindow()
        self.raise_()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
