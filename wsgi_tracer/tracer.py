from pyinstrument import Profiler
from pyinstrument.renderers import JSONRenderer
from time import time
import json
import os
import logging
from wsgi_tracer.settings import APMLog
from wsgi_tracer.utils import get_tracer_info



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


def pre_fork(server, worker):
    logfile = logfile = os.getenv('apm_logfile', None)
    setup_logger(worker, logfile)


def pre_request(worker, req):
    worker.profiler = Profiler()
    worker.profiler.start()
    worker.start_time = time()


def post_request(worker, req, environ, resp):
    worker.profiler.stop()
    record = {
        'versionn': 'v1',
        'proc_name': worker.cfg.proc_name,
        'services': "%s:%s" % (environ['SERVER_NAME'], environ['SERVER_PORT']),
        'protocol': environ['SERVER_PROTOCOL'],
        'endpoint': environ['PATH_INFO'],
        'apitrace': {
            'trace_id': get_tracer_info(environ),
            'req_time': worker.start_time,
            'resp_time': time()
        },
        'stacktrace': json.loads(JSONRenderer().render(session=worker.profiler.last_session))
    }
    import pdb;pdb.set_trace()
    worker.apm_log.info(record)
