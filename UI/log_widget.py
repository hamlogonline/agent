from PySide2.QtCore import Slot
from PySide2.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTableWidget, QAbstractItemView, QTableWidgetItem, QHeaderView
from PySide2.QtGui import Qt

from Utils import with_log

@with_log
class LogWidget(QWidget):
    
    MAX_LOG_SIZE = 100

    def __init__(self):
        super().__init__()
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout()
        log_group_box = QGroupBox(self.tr("Reported QSOs"))
        self.log_table_widget = self.create_log_table_widget()
        log_vbox_layout = QVBoxLayout()
        log_vbox_layout.addWidget(self.log_table_widget)
        log_group_box.setLayout(log_vbox_layout)
        layout.addWidget(log_group_box)
        self.setLayout(layout)

    def create_log_table_widget(self):
        table_widget = QTableWidget()
        table_widget.setColumnCount(5)
        table_widget.setHorizontalHeaderLabels([
            self.tr("Call Sign"),
            self.tr("UTC Time"),
            self.tr("Band"),
            self.tr("Mode"),
            self.tr("Status"),
        ])
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table_widget.verticalHeader().setVisible(False)
        return table_widget

    def log_qso(self, callsign, datetime, band, mode, status):
        row_count = self.log_table_widget.rowCount()
        if row_count == self.MAX_LOG_SIZE:
            self.log_table_widget.removeRow(row_count - 1)
        color = Qt.green if status == 'OK' else Qt.red
        self.log_table_widget.insertRow(0)
        self.log_table_widget.setItem(0, 0, QTableWidgetItem(callsign))
        self.log_table_widget.setItem(0, 1, QTableWidgetItem(datetime))
        self.log_table_widget.setItem(0, 2, QTableWidgetItem(band))
        self.log_table_widget.setItem(0, 3, QTableWidgetItem(mode))
        self.log_table_widget.setItem(0, 4, QTableWidgetItem(status))
        for column_index in range(self.log_table_widget.columnCount()):
            self.log_table_widget.item(0, column_index).setBackground(color)
        self.log_table_widget.scrollToTop()
