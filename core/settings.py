import os
import ssl
import random
import string
from threading import BoundedSemaphore

import certifi

sslcert = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
sslcert.verify_mode = ssl.CERT_REQUIRED
sslcert.load_verify_locations(cafile=os.path.relpath(
    certifi.where()), capath=None, cadata=None)


class Server:
    server_address = '0.0.0.0'
    server_port = 30000
    ping_time = 4
    ssl = sslcert
    storage = f"db/{''.join(random.choices(string.ascii_uppercase + string.digits, k= 5))}.result"


class Threading_params:
    MAX_THREADS = 100
    thread_limiter = BoundedSemaphore(MAX_THREADS)
