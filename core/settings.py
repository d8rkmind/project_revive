from threading import BoundedSemaphore


class Server:
    server_address = '0.0.0.0'
    server_port = 30000
    ping_time = 4


class Threading_params:
    MAX_THREADS = 100
    thread_limiter = BoundedSemaphore(MAX_THREADS)
