from PySide2.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QLabel, QPushButton
from asyncio import create_task, sleep as async_sleep
from Hamlog import hamlog_client
from Utils import with_log

@with_log
class StatusWidget(QWidget):

    AUTORIZATION_STATUS_UPDATE_INTERVAL = 10

    def __init__(self):
        super().__init__()
        self.is_authorized = False
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout()
        status_group_box = QGroupBox(self.tr("Agent Status"))
        self.status_label = QLabel()
        self.authorization_button = QPushButton()
        self.authorization_button.setEnabled(False)
        self.authorization_button.clicked.connect(self.authorization_button_click)
        status_vbox_layout = QVBoxLayout()
        status_vbox_layout.addWidget(self.status_label)
        status_vbox_layout.addWidget(self.authorization_button)
        status_group_box.setLayout(status_vbox_layout)
        layout.addWidget(status_group_box)
        layout.addStretch()
        self.setLayout(layout)

    def showEvent(self, event):
        self.log.debug('Updating authorization status due to the window show event')
        self.status_label.setText(self.tr("Updating..."))
        self.authorization_button.setText(self.tr("Updating..."))
        self.authorization_button.setEnabled(False)
        create_task(self.check_autorization_status())
        return super().showEvent(event)

    async def check_autorization_status(self):
        try:
            self.log.debug('Requesting authorization status')
            self.is_authorized = await hamlog_client.get_authorization_status()
            self.log.debug(f'Got authorization status: {self.is_authorized}')
            if self.is_authorized:
                self.status_label.setText(self.tr("Authorized"))
                self.authorization_button.setText(self.tr("Unauthorize"))
            else:
                self.status_label.setText(self.tr("Unauthorized"))
                self.authorization_button.setText(self.tr("Authorize"))
            self.authorization_button.setEnabled(True)
        except Exception as e:
            self.log.exception('Failed to get authorization status')
        finally:
            if self.isVisible() and self.is_authorized:
                self.log.debug(f'Rescheduling updating authorization status in {self.AUTORIZATION_STATUS_UPDATE_INTERVAL} seconds')
                await async_sleep(self.AUTORIZATION_STATUS_UPDATE_INTERVAL)
                await self.check_autorization_status()
    
    def authorization_button_click(self):
        if self.is_authorized:
            hamlog_client.deauthorize_agent()
        else:
            hamlog_client.authorize_agent()
