from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy

from .trayed_main_window import TrayedMainWindow
from .status_widget import StatusWidget
from .logging_widget import LoggingWidget

from constants import APPLICATION_NAME, APPLICATION_VERSION

from Utils import with_log

@with_log
class MainWindow(TrayedMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'{self.tr(APPLICATION_NAME)} {APPLICATION_VERSION}')
        self.create_ui()
        self.log.info(f'{APPLICATION_NAME} {APPLICATION_VERSION} started')

    def create_ui(self):
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
