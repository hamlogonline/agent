from Utils import with_log
from PySide2.QtCore import QSettings
from constants import APPLICATION_ORGANIZATION_NAME, APPLICATION_NAME

@with_log
class ApplicationSettings():

    SETTINGS_KEY_HAMLOG_API_KEY                         = 'hamlog_api_key'
    SETTINGS_KEY_HAMLOG_API_KEY_EXPIRATION_TIMESTAMP    = 'hamlog_api_key_expiration_timestamp'
    SETTINGS_KEY_WSJT_UNICAST_UDP_PORT                  = 'wsjt_unicast_udp_port'
    SETTINGS_KEY_WSJT_UNICAST_UDP_REPEATER_ENABLED      = 'wsjt_unicast_udp_repeater_enabled'
    SETTINGS_KEY_WSJT_UNICAST_UDP_REPEATER_ADDR         = 'wsjt_unicast_udp_repeater_addr'
    SETTINGS_KEY_WSJT_UNICAST_UDP_REPEATER_PORT         = 'wsjt_unicast_udp_repeater_port'

    SETTINGS_DEFAULT_WSJT_UNICAST_UDP_PORT              = 2237
    SETTINGS_DEFAULT_WSJT_UNICAST_UDP_REPEATER_ENABLED  = True
    SETTINGS_DEFAULT_WSJT_UNICAST_UDP_REPEATER_ADDR     = '127.0.0.1'
    SETTINGS_DEFAULT_WSJT_UNICAST_UDP_REPEATER_PORT     = 3373

    def __init__(self):
        super().__init__()
        self.settings = QSettings(QSettings.Format.NativeFormat, QSettings.Scope.UserScope,
            APPLICATION_ORGANIZATION_NAME, APPLICATION_NAME)
    
    @property
    def hamlog_api_key(self):
        stored_hamlog_api_key = self.settings.value(self.SETTINGS_KEY_HAMLOG_API_KEY, None, type=str)
        self.log.debug(f'Retrieved stored Hamlog API key: {stored_hamlog_api_key}')
        return stored_hamlog_api_key

    @hamlog_api_key.setter
    def hamlog_api_key(self, new_value):
        self.log.debug(f'Storing new Hamlog API key: {new_value}')
        self.settings.setValue(self.SETTINGS_KEY_HAMLOG_API_KEY, new_value)

    @property
    def hamlog_api_key_expiration_timestamp(self):
        stored_hamlog_api_key_expiration_timestamp = self.settings.value(self.SETTINGS_KEY_HAMLOG_API_KEY_EXPIRATION_TIMESTAMP, 0, type=int)
        self.log.debug(f'Retrieved stored Hamlog API key expiration timestamp: {stored_hamlog_api_key_expiration_timestamp}')
        return stored_hamlog_api_key_expiration_timestamp
    
    @hamlog_api_key_expiration_timestamp.setter
    def hamlog_api_key_expiration_timestamp(self, new_value):
        self.log.debug(f'Storing new Hamlog API key expiration timestamp: {new_value}')
        self.settings.setValue(self.SETTINGS_KEY_HAMLOG_API_KEY_EXPIRATION_TIMESTAMP, new_value)

    @property
    def wsjt_unicast_udp_port(self):
        stored_wsjt_udp_port = self.settings.value(self.SETTINGS_KEY_WSJT_UNICAST_UDP_PORT, self.SETTINGS_DEFAULT_WSJT_UNICAST_UDP_PORT, type=int)
        self.log.debug(f'Retrieved stored wsjt unicast UDP port: {stored_wsjt_udp_port}')
        return stored_wsjt_udp_port

    @wsjt_unicast_udp_port.setter
    def wsjt_unicast_udp_port(self, new_value):
        self.log.debug(f'Storing new wsjt unicast UDP port: {new_value}')
        self.settings.setValue(self.SETTINGS_KEY_WSJT_UNICAST_UDP_PORT, new_value)

    @property
    def wsjt_unicast_udp_repeater_addr(self):
        stored_unicast_udp_repeater_addr = self.settings.value(self.SETTINGS_KEY_WSJT_UNICAST_UDP_REPEATER_ADDR, self.SETTINGS_DEFAULT_WSJT_UNICAST_UDP_REPEATER_ADDR, type=str)
        self.log.debug(f'Retrieved stored wsjt unicast repeater addr: {stored_unicast_udp_repeater_addr}')
        return stored_unicast_udp_repeater_addr

    @wsjt_unicast_udp_repeater_addr.setter
    def wsjt_unicast_udp_repeater_addr(self, new_value):
        self.log.debug(f'Storing new wsjt unicast UDP repeater addr: {new_value}')
        self.settings.setValue(self.SETTINGS_KEY_WSJT_UNICAST_UDP_REPEATER_ADDR, new_value)

    @property
    def wsjt_unicast_udp_repeater_enabled(self):
        stored_unicast_udp_repeater_enabled = self.settings.value(self.SETTINGS_KEY_WSJT_UNICAST_UDP_REPEATER_ENABLED, self.SETTINGS_DEFAULT_WSJT_UNICAST_UDP_REPEATER_ENABLED, type=bool)
        self.log.debug(f'Retrieved stored wsjt unicast repeater enabled flag: {stored_unicast_udp_repeater_enabled}')
        return stored_unicast_udp_repeater_enabled

    @wsjt_unicast_udp_repeater_enabled.setter
    def wsjt_unicast_udp_repeater_enabled(self, new_value):
        self.log.debug(f'Storing new wsjt unicast UDP repeater enabled flash: {new_value}')
        self.settings.setValue(self.SETTINGS_KEY_WSJT_UNICAST_UDP_REPEATER_ENABLED, new_value)

    @property
    def wsjt_unicast_udp_repeater_port(self):
        stored_unicast_udp_repeater_port = self.settings.value(self.SETTINGS_KEY_WSJT_UNICAST_UDP_REPEATER_PORT, self.SETTINGS_DEFAULT_WSJT_UNICAST_UDP_REPEATER_PORT, type=int)
        self.log.debug(f'Retrieved stored wsjt unicast repeater port: {stored_unicast_udp_repeater_port}')
        return stored_unicast_udp_repeater_port

    @wsjt_unicast_udp_repeater_port.setter
    def wsjt_unicast_udp_repeater_port(self, new_value):
        self.log.debug(f'Storing new wsjt unicast UDP repeater port: {new_value}')
        self.settings.setValue(self.SETTINGS_KEY_WSJT_UNICAST_UDP_REPEATER_PORT, new_value)

application_settings = ApplicationSettings()
