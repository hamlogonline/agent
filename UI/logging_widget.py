from logging import Handler as LoggingHandler, Formatter as LogFormatter, getLogger
from PySide2.QtCore import Signal as QtSignal, QObject
from PySide2.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout, QGroupBox

from constants import APPLICATION_LOG_FORMAT, APPLICATION_LOG_LEVEL

class PlainTextLoggingHandler(LoggingHandler):

    def __init__(self, _append_log_signal):
        super().__init__()
        self._log_widget = QPlainTextEdit()
        self._log_widget.setReadOnly(True)
        self._append_log_signal = _append_log_signal
        self._append_log_signal.connect(self._log_widget.appendPlainText)
    
    def emit(self, record):
        msg = self.format(record)
        self._append_log_signal.emit(msg)

    def get_widget(self):
        return self._log_widget

class LoggingWidget(QWidget):

    _append_log_signal = QtSignal(str)

    def __init__(self):
        super().__init__()
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        group_box = QGroupBox(self.tr("Agent Log"))
        layout.addWidget(group_box)
        group_box_layout = QVBoxLayout()
        group_box.setLayout(group_box_layout)
        logging_handler = PlainTextLoggingHandler(self._append_log_signal)
        logging_handler.setFormatter(LogFormatter(APPLICATION_LOG_FORMAT))
        logger = getLogger()
        logger.addHandler(logging_handler)
        logger.setLevel(APPLICATION_LOG_LEVEL)
        group_box_layout.addWidget(logging_handler.get_widget())
