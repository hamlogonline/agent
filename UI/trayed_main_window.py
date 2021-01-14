
from sys import platform as sys_platform

from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QApplication, QStyle, QMenu
from PySide6.QtGui import QAction

class TrayedMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tray_icon = QSystemTrayIcon(self)
        self.update_tray_icon_image()
        self.update_tray_icon_tooltip()
        if sys_platform != 'darwin':
            self.tray_icon.setContextMenu(self.create_tray_icon_context_menu())
        self.tray_icon.activated.connect(self.show)
        self.tray_icon.show()

    def get_current_tray_icon_image(self):
        return self.style().standardIcon(QStyle.SP_ComputerIcon)

    def update_tray_icon_image(self):
        self.tray_icon.setIcon(self.get_current_tray_icon_image())

    def get_tray_icon_tooltip(self):
        return self.tr("Default tooltip")

    def update_tray_icon_tooltip(self):
        self.tray_icon.setToolTip(self.get_tray_icon_tooltip())

    def create_tray_icon_context_menu(self):
        tray_menu = QMenu()
        show_action = QAction(self.tr("Show"), self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        quit_action = QAction(self.tr("Exit"), self)
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
