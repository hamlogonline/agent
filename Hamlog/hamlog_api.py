from asyncio import sleep as async_sleep, Event as AsyncioEvent
from datetime import datetime, timezone
from aiohttp import ClientSession as HttpClientSession, ClientTimeout as HttpClientTimeout
from ssl import create_default_context as ssl_create_default_context
try:
    from certifi import where as get_ca_bundle_location
except:
    get_ca_bundle_location = None
from constants import APPLICATION_NAME, APPLICATION_VERSION

from Utils import with_log, open_url


class HamlogAPIError(Exception):
    def __init__(self, message, error=None):
        super().__init__(message)
        self.error = error


class HamlogAPIAuthorizationError(HamlogAPIError):
    pass


class HamlogAPIConnectionError(HamlogAPIError):
    pass


@with_log
class HamlogAPI():

    _HAMLOG_DOMAIN = 'https://hamlog.online'
    _AGENT_AUTHORIZATION_URL = _HAMLOG_DOMAIN + '/account/agent.php'
    _AGENT_API_ENDPOINT_URL = _HAMLOG_DOMAIN + '/api/agent/'

    _HTTP_TIMEOUT = HttpClientTimeout(total=30)
    _HTTP_HEADERS = {
        'User-Agent': f'{APPLICATION_NAME} {APPLICATION_VERSION}'
    }

    def __init__(self):
        super().__init__()
        if get_ca_bundle_location:
            self._ssl_context = ssl_create_default_context(
                cafile=get_ca_bundle_location())
        else:
            self._ssl_context = ssl_create_default_context()

    async def _send_request(self, request):
        self.log.debug(f'Sending API request: {request}')
        try:
            async with HttpClientSession(timeout=self._HTTP_TIMEOUT, headers=self._HTTP_HEADERS) as session:
                closed_event = self._create_aiohttp_closed_event(session)
                async with session.post(self._AGENT_API_ENDPOINT_URL, json=request, ssl=self._ssl_context) as response:
                    json_response = await response.json()
                    self.log.debug(f'Got JSON response: {json_response}')
                    return json_response
                await closed_event.wait()
        except Exception as e:
            self.log.exception('Failed to perform API request')
            raise HamlogAPIConnectionError('Failed to perform API request', e)

    def is_successful(self, response):
        return response.get('STATUS') == 'OK'

    def get_response_error(self, response):
        return response.get('ERROR', 'Unknown error')

    async def get_api_key_expiration_timestamp(self, api_key):
        response = await self._send_request({
            'KEYSTATUS': {
                'APIKEY': api_key
            }
        })
        if self.is_successful(response):
            self.log.debug('API key is valid')
            callsign = response.get('CALLSIGN')
            expiration_date_string = response.get('EXPIRES')
            latest_version = response.get('CURRENT')
            if expiration_date_string is not None:
                try:
                    expiration_timestamp = int(expiration_date_string)
                    self.log.debug(
                        f'API key expires on {expiration_timestamp}')
                    return expiration_timestamp, callsign, latest_version
                except:
                    self.log.exception('Failed to parse expiration date')
            self.log.warning('Key expiration date is missing in response')
            return None
        raise HamlogAPIAuthorizationError(self.get_response_error(response))

    async def deauthorize_api_key(self, api_key):
        response = await self._send_request({
            'LOGOUT': {
                'APIKEY': api_key
            }
        })
        if not self.is_successful(response):
            raise HamlogAPIAuthorizationError(
                self.get_response_error(response))

    async def report_qso(self, api_key, qso_data):
        response = await self._send_request({
            'QSOADD': {
                'APIKEY': api_key,
                'DATA': {k.upper(): v for k, v in qso_data.items()}
            }
        })
        if not self.is_successful(response):
            raise HamlogAPIAuthorizationError(
                self.get_response_error(response))

    async def report_adif(self, api_key, adif_data):
        response = await self._send_request({
            'ADIFADD': {
                'APIKEY': api_key,
                'ADIFDATA': adif_data
            }
        })
        if not self.is_successful(response):
            raise HamlogAPIAuthorizationError(
                self.get_response_error(response))

    def authorize(self):
        try:
            assert open_url(self._AGENT_AUTHORIZATION_URL) == True
        except Exception as e:
            self.log.exception('Cannot open authorization URL')
            raise HamlogAPIAuthorizationError(
                'Cannot open authorization URL', e)

    def _create_aiohttp_closed_event(self, session) -> AsyncioEvent:
        """Work around aiohttp issue that doesn't properly close transports on exit.                                        

        See https://github.com/aio-libs/aiohttp/issues/1925#issuecomment-639080209                                          

        Returns:                                                                                                            
        An event that will be set once all transports have been properly closed.                                         
        """

        transports = 0
        all_is_lost = AsyncioEvent()

        def connection_lost(exc, orig_lost):
            nonlocal transports

            try:
                orig_lost(exc)
            finally:
                transports -= 1
                if transports == 0:
                    all_is_lost.set()

        def eof_received(orig_eof_received):
            try:
                orig_eof_received()
            except AttributeError:
                # It may happen that eof_received() is called after
                # _app_protocol and _transport are set to None.
                pass

        for conn in session.connector._conns.values():
            for handler, _ in conn:
                proto = getattr(handler.transport, "_ssl_protocol", None)
                if proto is None:
                    continue

                transports += 1
                orig_lost = proto.connection_lost
                orig_eof_received = proto.eof_received

                proto.connection_lost = functools.partial(
                    connection_lost, orig_lost=orig_lost
                )
                proto.eof_received = functools.partial(
                    eof_received, orig_eof_received=orig_eof_received
                )

        if transports == 0:
            all_is_lost.set()

        return all_is_lost
