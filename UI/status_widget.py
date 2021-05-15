from PySide2.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from asyncio import create_task, sleep as async_sleep
from Hamlog import hamlog
from Utils import with_log

@with_log
class StatusWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.create_ui()
        hamlog.add_observer('_is_authorized', self.authorization_status_did_change)
        self.update_ui()

    def create_ui(self):
        layout = QVBoxLayout()
        status_group_box = QGroupBox(self.tr("Agent Status"))
        self.status_label = QLabel()
        self.authorization_button = QPushButton()
        self.authorization_button.setFocus()
        status_vbox_layout = QVBoxLayout()
        status_vbox_layout.addWidget(self.status_label)
        status_vbox_layout.addWidget(self.authorization_button)
        status_group_box.setLayout(status_vbox_layout)
        layout.addWidget(status_group_box)
        self.setLayout(layout)

    def update_ui(self):
        is_authorized = hamlog.is_authorized
        try:
            self.authorization_button.clicked.disconnect()
        except:
            pass
        if is_authorized == None:
            self.status_label.setText(self.tr("Updating..."))
            self.authorization_button.setText(self.tr("Updating..."))
            self.authorization_button.setEnabled(False)
        else:
            if is_authorized:
                self.status_label.setText(self.tr("Authorized"))
                self.authorization_button.setText(self.tr("Deauthorize"))
                self.authorization_button.clicked.connect(self.deauthorize_click)
            else:
                self.status_label.setText(self.tr("Unauthorized"))
                self.authorization_button.setText(self.tr("Authorize"))
                self.authorization_button.clicked.connect(self.authorize_click)
            self.authorization_button.setEnabled(True)
        self.repaint()

    def authorization_status_did_change(self):
        self.update_ui()

    def authorize_click(self):
        hamlog.authorize_agent()

    def deauthorize_click(self):
        hamlog.deauthorize_agent()
