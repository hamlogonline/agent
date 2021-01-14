from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from settings import application_settings
from Utils import with_log

@with_log
class HamlogClient():

    _HAMLOG_DOMAIN = 'https://hamlog.online'
    _AGENT_AUTHORIZATION_URL = _HAMLOG_DOMAIN + '/account/agent.php'

    def __init__(self):
        self.hamlog_api_key = application_settings.hamlog_api_key

    async def get_authorization_status(self):
        self.log.debug('Obtaining authorization status')
        if self.hamlog_api_key:
            self.log.debug('Checking stored Hamlog API key validity')
            return False
        else:
            self.log.debug('No stored Hamlog API key present, agent is not autorized')
            return False

    def authorize_agent(self):
        authorization_url_string = self._AGENT_AUTHORIZATION_URL
        self.log.debug(f'Starting agent authorization with url: {authorization_url_string}')
        authorization_url = QUrl(authorization_url_string)
        if not QDesktopServices.openUrl(authorization_url):
            self.log.warning(f'Cannot open authorization url: {authorization_url_string}')

    def deauthorize_agent(self):
        self.log.debug('Deauthorizing agent')
