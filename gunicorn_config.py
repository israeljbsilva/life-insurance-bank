from multiprocessing import cpu_count

from os import environ as env


def max_workers():
    """
    Number of maximum workers
    ref: http://docs.gunicorn.org/en/latest/design.html#how-many-workers
    :return: Returns the maximum number of workers
    """
    default = 2 * cpu_count() + 1
    return int(env.get("WEB_CONCURRENCY", default))


def max_threads():
    """
    Number of maximum threads per worker
    ref: http://docs.gunicorn.org/en/stable/settings.html#threads
    :return: Returns the number of maximum threads per worker
    """
    default = 4 * cpu_count()
    return int(env.get("WORKER_CONCURRENCY", default))


def max_worker_connections():
    default = 1024
    return int(env.get("WORKER_CONNECTIONS", default))


# ======================
# Setting default values
# ======================

# Reference: http://docs.gunicorn.org/en/stable/settings.html

# The type of workers to use.
worker_class = 'gevent'

# The number of worker processes for handling requests.
workers = max_workers()

# The number of worker threads for handling requests.
threads = 1  # we're using a sync-worker (gevent) where threads are not recommended

# The maximum number of simultaneous clients.
worker_connections = max_worker_connections()

# Load application code before the worker processes are forked.
preload_app = False

# Workers silent for more than this many seconds are killed and restarted.
timeout = 61

# The number of seconds to wait for requests on a Keep-Alive connection.
keepalive = 1

# The maximum number of pending connections.
backlog = 2048

# Send Gunicorn logs to syslog.
syslog = True

# Makes Gunicorn use the parameter as program-name in the syslog entries.
syslog_prefix = 'GUNICORN'

# The granularity of Error log outputs.
loglevel = 'debug'

# The Access log file to write to.
accesslog = '-'


for k, value in env.items():  # type: str
    if k.startswith("GUNICORN_"):
        key = k.split('_', 1)[1].lower()
        locals()[key] = value
