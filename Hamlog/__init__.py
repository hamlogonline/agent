from .hamlog_api import HamlogAPI as HamlogAPI
from .hamlog_api import HamlogAPIAuthorizationError as HamlogAPIAuthorizationError
from .hamlog_api import HamlogAPIConnectionError as HamlogAPIConnectionError
from .hamlog_agent import HamlogAgent as HamlogAgent

from settings import application_settings

hamlog_agent = HamlogAgent(application_settings)
