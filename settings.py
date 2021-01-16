from Utils import with_log
from PySide2.QtCore import QSettings

@with_log
class ApplicationSettings():

    SETTINGS_KEY_HAMLOG_API_KEY = 'hamlog_api_key'
    SETTINGS_KEY_HAMLOG_API_KEY_EXPIRATION_TIMESTAMP = 'hamlog_api_key_expiration_timestamp'

    def __init__(self):
        super().__init__()
        self.settings = QSettings()
    
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

application_settings = ApplicationSettings()
