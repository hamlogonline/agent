from asyncio import create_task
from aiohttp import ClientSession as HttpClientSession, ClientTimeout as HttpClientTimeout
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from settings import application_settings
from Utils import with_log, open_url

from constants import APPLICATION_NAME, APPLICATION_VERSION

@with_log
class HamlogClient():
    _HAMLOG_DOMAIN = 'https://hamlog.online'
    _AGENT_AUTHORIZATION_URL = _HAMLOG_DOMAIN + '/account/agent.php'
    _AGENT_API_ENDPOINT_URL = _HAMLOG_DOMAIN + '/api/agent/'

    _HTTP_TIMEOUT = HttpClientTimeout(total=30)
    _HTTP_HEADERS = {
        'User-Agent': f'{(APPLICATION_NAME)} {APPLICATION_VERSION}'
    }

    def __init__(self):
        self.api_session = None

    async def get_authorization_status(self):
        self.log.debug('Obtaining authorization status')
        if application_settings.hamlog_api_key:
            self.log.debug('Checking stored Hamlog API key validity')
            (api_key_valid, _) = await self.get_api_key_status(application_settings.hamlog_api_key)
            if api_key_valid == False:
                application_settings.hamlog_api_key = None
            return api_key_valid
        else:
            self.log.debug('No stored Hamlog API key present, agent is not autorized')
            return False

    async def get_api_key_status(self, api_key):
        self.log.debug('Obtaining API key status')
        try:
            async with HttpClientSession(timeout=self._HTTP_TIMEOUT, headers=self._HTTP_HEADERS) as api_session:
                async with api_session.post(self._AGENT_API_ENDPOINT_URL, json=
                    { 'KEYSTATUS' : {
                        'APIKEY': api_key 
                    }
                }) as reponse:
                    json_response = await reponse.json()
                    self.log.debug(f'Got JSON response: {json_response}')
                    status = json_response.get('STATUS')
                    if status and status == 'OK':
                        return (True, None)
                    else:
                        self.log.warning(f'Invalid API key, response: {json_response}')
                        return (False, None)
        except:
            self.log.exception('Failed to obtain API key status')
            return (False, None)

    async def update_api_key(self, new_api_key):
        (api_key_valid, api_key_expiration_date) = await self.get_api_key_status(new_api_key)
        if api_key_valid:
            self.log.info('Got new API key')
            application_settings.hamlog_api_key = new_api_key
        else:
            self.log.error('Got invalid API key')

    def authorize_agent(self):
        authorization_url_string = self._AGENT_AUTHORIZATION_URL
        self.log.debug(f'Starting agent authorization with url: {authorization_url_string}')
        if not open_url(authorization_url_string):
            self.log.warning(f'Cannot open authorization url: {authorization_url_string}')

    async def deauthorize_agent(self):
        self.log.info('Deauthorizing agent')
        try:
            async with HttpClientSession(timeout=self._HTTP_TIMEOUT, headers=self._HTTP_HEADERS) as api_session:
                    async with api_session.post(self._AGENT_API_ENDPOINT_URL, json=
                        { 'LOGOUT' : {
                            'APIKEY': application_settings.hamlog_api_key 
                        }
                    }) as reponse:
                        json_response = await reponse.json()
                        self.log.debug(f'Got JSON response: {json_response}')
        except:
            self.log.exception('Failed to deauthorize API key')
        finally:
            application_settings.api_key = None

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
                    create_task(self.update_api_key(new_api_key))
                else:
                    self.log.warning(f'API key is missing in url: {url}')
            else:
                self.log.warning(f'Unsupported URL scheme methot in url {url}')
        else:
            self.log.warning(f'Unsupported URL scheme in url {url}')
        return False
