# Sample Gunicorn configuration file.
import multiprocessing

#
# Server socket
#
bind = "127.0.0.1:8018"
# bind = 'unix:/tmp/gunicorn.api-nethub.sock'
backlog = 2048

#
# Worker processes
#
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
timeout = 120
keepalive = 2

#
# Debugging
#
debug = True
spew = False

#
# Server mechanics
#
daemon = False
pidfile = "/var/python-apps/alquiler_perfil/run/lock.lock"
umask = 0
user = "www-data"
group = None
tmp_upload_dir = "/var/python-apps/alquiler_perfil/tmp/"

#
#   Logging
#
loglevel = 'info'
errorlog = '/var/python-apps/alquiler_perfil/log/error.log'
accesslog = '/var/python-apps/alquiler_perfil/log/access.log'


#
# Process naming
#
proc_name = "alquiler_perfil-unix"

preload = True