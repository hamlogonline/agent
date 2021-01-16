from .hamlog_api import HamlogAPI as HamlogAPI
from .hamlog_api import HamlogAPIAuthorizationError as HamlogAPIAuthorizationError
from .hamlog_api import HamlogAPIConnectionError as HamlogAPIConnectionError
from .hamlog import Hamlog as Hamlog

from settings import application_settings

hamlog = Hamlog(application_settings)
