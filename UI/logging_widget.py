from logging import Handler as LoggingHandler, Formatter as LogFormatter, getLogger

from PySide6.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout, QGroupBox

from constants import APPLICATION_LOG_FORMAT, APPLICATION_LOG_LEVEL

class PlainTextLoggingHandler(LoggingHandler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)    
    
    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

    def get_widget(self):
        return self.widget

class LoggingWidget(QWidget):
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
        logging_handler = PlainTextLoggingHandler(self)
        logging_handler.setFormatter(LogFormatter(APPLICATION_LOG_FORMAT))
        logger = getLogger()
        logger.addHandler(logging_handler)
        logger.setLevel(APPLICATION_LOG_LEVEL)
        group_box_layout.addWidget(logging_handler.get_widget())
