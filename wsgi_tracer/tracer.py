from pyinstrument import Profiler
from pyinstrument.renderers import JSONRenderer
from time import time
import json
import os
import logging
from wsgi_tracer.utils import get_tracer_info
from functools import wraps

def wsgi_wrapper(worker, wsgi):

    if hasattr(wsgi, 'origin'):
        return wsgi

    @wraps(wsgi)
    def _(environ, resp):
        _.origin = wsgi
        start_time = time()
        profile = Profiler()
        profile.start()
        ret = wsgi(environ, resp)
        profile.stop()
        record = {
            'versionn': 'v1',
            'proc_name': worker.cfg.proc_name,
            'services': "%s:%s" % (environ['SERVER_NAME'], environ['SERVER_PORT']),
            'protocol': environ['SERVER_PROTOCOL'],
            'endpoint': environ['PATH_INFO'],
            'apitrace': {
                'trace_id': get_tracer_info(environ),
                'req_time': start_time,
                'resp_time': time()
            },
            'stacktrace': json.loads(JSONRenderer().render(session=profile.last_session))
        }
        if hasattr(worker, 'apm_log'):
            worker.apm_log.info(record)
        else:
            worker.log.info(record)
        return ret
    return _


def trace_wsgi(worker):
    worker.wsgi.wsgi_app = wsgi_wrapper(worker, worker.wsgi.wsgi_app)


def setup_logger(worker, logfile=None):
    if not logfile:
        worker.apm_log = worker.log
        return

    logger = logging.getLogger("APMLogger")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logfile, "w")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    logfmt = logging.Formatter(
        r"%(asctime)s [%(process)d] [%(levelname)s] %(message)s"
    )
    fh.setFormatter(logfmt)
    worker.apm_log = logger
