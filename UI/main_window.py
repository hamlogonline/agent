from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QMessageBox
from PySide2.QtGui import QIcon

from .trayed_main_window import TrayedMainWindow
from .status_widget import StatusWidget
from .wsjt_settings_widget import WsjtSettingsWidget
from .log_widget import LogWidget

from constants import APPLICATION_NAME, APPLICATION_VERSION

from Utils import with_log, get_resource_path

from datetime import datetime

from Hamlog import hamlog


@with_log
class MainWindow(TrayedMainWindow):

    log_qso_signal = Signal(str, str, str, str, str)
    unauthorized_qso_signal = Signal()

    def __init__(self):
        super().__init__()
        self._create_ui()
        hamlog.log_callback = self.log_qso
        hamlog.unauthorized_qso_callback = self.unauthorized_qso
        self.log.info(f'{APPLICATION_NAME} {APPLICATION_VERSION} started')

    def _create_ui(self):
        self.tray_icon.setIcon(
            QIcon(str(get_resource_path() / 'res' / 'tray_icon.png')))
        self.setWindowTitle(
            f'{self.tr(APPLICATION_NAME)} {APPLICATION_VERSION}')
        self.setWindowIcon(
            QIcon(str(get_resource_path() / 'res' / 'tray_icon.png')))
        central_widget = QWidget()
        central_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        central_widget.setMinimumSize(800, 300)
        self.log_widget = LogWidget()
        self.log_qso_signal.connect(self.log_widget.log_qso)
        self.unauthorized_qso_signal.connect(self._unauthorized_qso)
        self.log_widget.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.wsjt_settings_widget = WsjtSettingsWidget()
        self.status_widget = StatusWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.log_widget)
        layout.addWidget(self.wsjt_settings_widget)
        layout.addWidget(self.status_widget)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def log_qso(self, callsign, datetime, band, mode, status):
        self.log_qso_signal.emit(callsign, datetime.strftime(
            '%Y-%m-%d %H:%M:%S'), band, mode, status)

    def unauthorized_qso(self):
        self.unauthorized_qso_signal.emit()

    def _unauthorized_qso(self):
        msg_box = QMessageBox(self)
        msg_box.setAttribute(Qt.WA_DeleteOnClose, True)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setWindowTitle(self.tr("Hamlog Agent Error"))
        msg_box.setText(self.tr("Hamlog Agent is not authorized"))
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setModal(False)
        msg_box.exec()
