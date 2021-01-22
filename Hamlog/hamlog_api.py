from datetime import datetime, timezone
from aiohttp import ClientSession as HttpClientSession, ClientTimeout as HttpClientTimeout
from ssl import create_default_context as ssl_create_default_context
from certifi import where as get_ca_bundle_location
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
        'User-Agent': f'{(APPLICATION_NAME)} {APPLICATION_VERSION}'
    }

    async def _send_request(self, request):
        self.log.debug(f'Sending API request: {request}')
        try:
            async with HttpClientSession(timeout=self._HTTP_TIMEOUT, headers=self._HTTP_HEADERS) as session:
                sslcontext = ssl_create_default_context(cafile=get_ca_bundle_location())
                async with session.post(self._AGENT_API_ENDPOINT_URL, json=request, ssl=sslcontext) as response:
                    json_response = await response.json()
                    self.log.debug(f'Got JSON response: {json_response}')
                    return json_response
        except Exception as e:
            self.log.exception('Failed to perform API request')
            raise HamlogAPIConnectionError('Failed to perform API request', e)

    def is_successful(self, response):
        return response.get('STATUS') == 'OK'

    def get_response_error(self, response):
        return response.get('ERROR', 'Unknown error')

    async def get_api_key_expiration_timestamp(self, api_key):
        response = await self._send_request({
            'KEYSTATUS' : {
                'APIKEY': api_key
            }
        })
        if self.is_successful(response):
            self.log.debug('API key is valid')
            expiration_date_string = response.get('EXPIRES')
            if expiration_date_string is not None:
                try:
                    expiration_timestamp = int(expiration_date_string)
                    self.log.debug(f'API key expires on {expiration_timestamp}')
                    return expiration_timestamp
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
            raise HamlogAPIAuthorizationError(self.get_response_error(response))

    async def report_qso(self, api_key, qso_data):
        response = await self._send_request({
            'QSOADD': {
                'APIKEY' : api_key,
                'DATA' : { k.upper(): v for k, v in qso_data.items() }
            }
        })
        if not self.is_successful(response):
            raise HamlogAPIAuthorizationError(self.get_response_error(response))

    async def report_adif(self, api_key, adif_data):
        response = await self._send_request({
            'ADIFADD': {
                'APIKEY' : api_key,
                'ADIFDATA': adif_data
            }
        })
        if not self.is_successful(response):
            raise HamlogAPIAuthorizationError(self.get_response_error(response))

    def authorize(self):
        try:
            assert open_url(self._AGENT_AUTHORIZATION_URL) == True                
        except Exception as e:
            self.log.exception('Cannot open authorization URL')
            raise HamlogAPIAuthorizationError('Cannot open authorization URL', e)
