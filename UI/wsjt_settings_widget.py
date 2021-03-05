from PySide2.QtCore import Slot
from PySide2.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFormLayout, QLineEdit, QCheckBox
from asyncio import create_task, sleep as async_sleep
from Hamlog import hamlog
from Utils import with_log

from settings import application_settings

from Hamlog import hamlog

@with_log
class WsjtSettingsWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        group_box = QGroupBox(self.tr("WSJT Settings"))
        layout.addWidget(group_box)
        settings_hbox = QHBoxLayout(group_box)

        wsjt_port_settings_layout = QFormLayout()
        wsjt_port_line_edit = QLineEdit()
        wsjt_port_line_edit.setText(str(application_settings.wsjt_unicast_udp_port))
        wsjt_port_line_edit.editingFinished.connect(self.wsjt_port_line_edit_editing_finished)
        wsjt_port_settings_layout.addRow(self.tr("WSJT Port:"), wsjt_port_line_edit)
        settings_hbox.addLayout(wsjt_port_settings_layout)

        wsjt_forwarding_settings_layout = QFormLayout()
        wsjt_forwarding_checkbox = QCheckBox()
        wsjt_forwarding_checkbox.setChecked(application_settings.wsjt_unicast_udp_repeater_enabled)
        wsjt_forwarding_checkbox.stateChanged.connect(self.wsjt_forwarding_checkbox_state_changed)
        wsjt_forwarding_settings_layout.addRow(self.tr("Forwarding:"), wsjt_forwarding_checkbox)
        wsjt_forwarding_port_line_edit = QLineEdit()
        wsjt_forwarding_port_line_edit.setText(str(application_settings.wsjt_unicast_udp_repeater_port))
        wsjt_forwarding_port_line_edit.editingFinished.connect(self.wsjt_forwarding_port_line_edit_editing_finished)
        wsjt_forwarding_settings_layout.addRow(self.tr("Port:"), wsjt_forwarding_port_line_edit)
        settings_hbox.addLayout(wsjt_forwarding_settings_layout)

        settings_hbox.addStretch()

    def wsjt_port_line_edit_editing_finished(self):
        try:
            new_value = int(self.sender().text())
            old_value = application_settings.wsjt_unicast_udp_port
            assert (new_value > 1023)
            assert (new_value < 65536)
            if new_value != old_value:
                application_settings.wsjt_unicast_udp_port = new_value
                create_task(hamlog.start_listeners())
        except:
            self.sender().setText(str(application_settings.wsjt_unicast_udp_port))

    def wsjt_forwarding_port_line_edit_editing_finished(self):
        try:
            new_value = int(self.sender().text())
            old_value = application_settings.wsjt_unicast_udp_repeater_port
            assert (new_value > 1023)
            assert (new_value < 65536)
            if new_value != old_value:
                application_settings.wsjt_unicast_udp_repeater_port = new_value
        except:
            self.sender().setText(str(application_settings.wsjt_unicast_udp_repeater_port))
        
    def wsjt_forwarding_checkbox_state_changed(self, state):
        application_settings.wsjt_unicast_udp_repeater_enabled = self.sender().isChecked()
    