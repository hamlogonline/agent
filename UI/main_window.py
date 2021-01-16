from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PySide2.QtGui import QIcon

from .trayed_main_window import TrayedMainWindow
from .status_widget import StatusWidget
from .logging_widget import LoggingWidget

from constants import APPLICATION_NAME, APPLICATION_VERSION

from Utils import with_log, get_resource_path

@with_log
class MainWindow(TrayedMainWindow):
    def __init__(self):
        super().__init__()
        self.create_ui()
        self.log.info(f'{APPLICATION_NAME} {APPLICATION_VERSION} started')

    def create_ui(self):
        print(str(get_resource_path() / 'res' / 'tray_icon.png'))
        self.tray_icon.setIcon(QIcon(str(get_resource_path() / 'res' / 'tray_icon.png')))
        self.setWindowTitle(f'{self.tr(APPLICATION_NAME)} {APPLICATION_VERSION}')
        central_widget = QWidget()
        central_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        central_widget.setMinimumSize(800, 300)
        self.status_widget = StatusWidget()
        self.logging_widget = LoggingWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.status_widget)
        layout.addWidget(self.logging_widget)
        layout.addStretch()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
