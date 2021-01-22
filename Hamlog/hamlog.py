from asyncio import create_task, sleep as async_sleep, CancelledError as AsyncioCancelledError
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from dataclasses import asdict as dataclass_as_dict
from Hamlog import HamlogAPI, HamlogAPIAuthorizationError, HamlogAPIConnectionError, HamlogQSO, WsjtxQsoListener
from Utils import with_log, Observable

@with_log
class Hamlog(Observable):

    _API_RETRY_TIMEUOT = 3
    _AUTHORIZATION_UPDATE_TIMEOUT = 10

    @property
    def _api_key(self):
        return self._settings.hamlog_api_key

    @_api_key.setter
    def _api_key(self, new_value):
        self._settings.hamlog_api_key = new_value

    @property
    def _api_key_expiration_timestamp(self):
        return self._settings.hamlog_api_key_expiration_timestamp

    @_api_key_expiration_timestamp.setter
    def _api_key_expiration_timestamp(self, new_value):
        self._settings.hamlog_api_key_expiration_timestamp = new_value

    @property
    def is_authorized(self):
        if self._is_authorized is None:
            self.update_authorization_status()
        return self._is_authorized

    def __init__(self, settings):
        super().__init__()
        self._settings = settings
        self._is_authorized = None
        self._hamlog_api = HamlogAPI()
        self._authorization_status_update_task = None
        self._listeners = list()

    def _has_valid_api_key(self):
        if self._api_key:
            if self._api_key_expiration_timestamp == 0 or self._api_key_expiration_timestamp > datetime.utcnow().timestamp():
                return True
        return False

    def update_authorization_status(self):
        if self._has_valid_api_key():
            self.log.debug('Updating authorization status')
            if self._authorization_status_update_task is None:
                self._authorization_status_update_task = create_task(self._update_authorization_status_task())
        else:
            self._is_authorized = False
    
    async def _update_authorization_status_task(self):
        while True:
            self.log.debug(f'Requesting API key status for {self._api_key}')
            try:
                expiration_timestamp = await self._hamlog_api.get_api_key_expiration_timestamp(self._api_key)
                self._is_authorized = True
                self._api_key_expiration_timestamp = expiration_timestamp
                test_qso = HamlogQSO(mycall='r2axztest', call='r2axz', band='40', mode='LSB', timestamp=datetime.utcnow().timestamp())
                self.report_qso(test_qso)
                await async_sleep(self._AUTHORIZATION_UPDATE_TIMEOUT)
            except HamlogAPIAuthorizationError:
                self._is_authorized = False
                self._api_key = None
                self._api_key_expiration_timestamp = 0
                break
            except HamlogAPIConnectionError:
                async_sleep(self._API_REQUEST_RETRY_TIMEUOT)
            except AsyncioCancelledError:
                self.log.debug('Update authorization status task cancelled')

    def update_api_key(self, new_api_key):
        self.log.info(f'Got new API key: {new_api_key}')
        if (self._authorization_status_update_task):
            self._authorization_status_update_task.cancel()
        self._api_key = new_api_key
        self._api_key_expiration_timestamp = 0
        self._authorization_status_update_task = create_task(self._update_authorization_status_task())

    def authorize_agent(self):
        try:
            self._hamlog_api.authorize()
        except:
            pass

    def deauthorize_agent(self):
        if self._update_authorization_status_task:
            self._authorization_status_update_task.cancel()
            self._authorization_status_update_task = None
        if self._has_valid_api_key:
            create_task(self._hamlog_api.deauthorize_api_key(self._api_key))
            self._api_key = None
            self._api_key_expiration_timestamp = 0
            self._is_authorized = False

    def report_qso(self, qso):
        if not isinstance(qso, HamlogQSO):
            raise ValueError('qso must be HamlogQSO or its subclass')
        if self._has_valid_api_key:
            self.log.debug(f'Reporting QSO {qso}')
            qso_data = dataclass_as_dict(qso, dict_factory=lambda d: dict(x for x in d if x[1] is not None))
            create_task(self._hamlog_api.report_qso(self._api_key, qso_data))

    def process_url_scheme(self, url):
        self.log.debug(f'Processing URL scheme request: {url}')
        url_components = urlparse(url)
        if url_components.scheme == 'hamlogagent':
            method = url_components.netloc
            parsed_query = parse_qs(url_components.query)
            if method == 'setapikey':
                try:
                    new_api_key = parsed_query.get('apikey')[0]
                except:
                    new_api_key = None
                if new_api_key:
                    self.log.debug(f'About to update API key')
                    self.update_api_key(new_api_key)
                else:
                    self.log.warning(f'API key is missing in url: {url}')
            else:
                self.log.warning(f'Unsupported URL scheme method in url {url}')
        else:
            self.log.warning(f'Unsupported URL scheme in url {url}')
        return False

    async def start_listeners(self):
        wsjtx_qso_listener = WsjtxQsoListener(self.report_qso)
        self._listeners.append(wsjtx_qso_listener)
        await wsjtx_qso_listener.start()
