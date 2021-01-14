from Utils import with_log
from PySide2.QtCore import QSettings

@with_log
class ApplicationSettings():

    SETTINGS_KEY_HAMLOG_API_KEY = 'hamlog_api_key'

    def __init__(self):
        super().__init__()
        self.settings = QSettings()
    
    @property
    def hamlog_api_key(self):
        stored_hamlog_api_key = self.settings.value(self.SETTINGS_KEY_HAMLOG_API_KEY, None, type=str)
        self.log.debug(f'Retrieved stored Hamlog API key: {stored_hamlog_api_key}')
        return stored_hamlog_api_key

    @hamlog_api_key.setter
    def hamlog_api_key(self, value):
        self.log.debug(f'Storing new Hamlog API key: {value}')
        self.settings.setValue(self.SETTINGS_KEY_HAMLOG_API_KEY, value)

application_settings = ApplicationSettings()