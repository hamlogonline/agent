from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PySide2.QtGui import QIcon

from .trayed_main_window import TrayedMainWindow
from .status_widget import StatusWidget
from .wsjt_settings_widget import WsjtSettingsWidget

from constants import APPLICATION_NAME, APPLICATION_VERSION

from Utils import with_log, get_resource_path

@with_log
class MainWindow(TrayedMainWindow):
    def __init__(self):
        super().__init__()
        self.create_ui()
        self.log.info(f'{APPLICATION_NAME} {APPLICATION_VERSION} started')

    def create_ui(self):
        self.tray_icon.setIcon(QIcon(str(get_resource_path() / 'res' / 'tray_icon.png')))
        self.setWindowTitle(f'{self.tr(APPLICATION_NAME)} {APPLICATION_VERSION}')
        self.setWindowIcon(QIcon(str(get_resource_path() / 'res' / 'tray_icon.png')))
        central_widget = QWidget()
        central_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        central_widget.setMinimumSize(800, 300)
        self.status_widget = StatusWidget()
        self.wsjt_settings_widget = WsjtSettingsWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.wsjt_settings_widget)
        layout.addWidget(self.status_widget)
        layout.addStretch()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
