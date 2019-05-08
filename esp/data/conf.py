AP_IF_SSID = 'TooSmart Coffee'
CONNECT_RETRIES = 3
CONNECTION_TIME = 6.0

ERROR_LOG_FILENAME = 'error.log'

try:
    from .local_conf import *
except ImportError:
    pass
