from pyinstrument import Profiler
from pyinstrument.renderers import JSONRenderer
from time import time
import json
import logging
from functools import wraps, partial
import random
from wsgi_tracer.utils import get_tracer_info
from wsgi_tracer.mapper import tree2list



def profile_fn(fn, sample_filter=lambda x: x, sample_mapper=lambda x: x):
    profile = Profiler()
    profile.start()
    ret = fn()
    profile.stop()
    sample_data = json.loads(JSONRenderer().render(session=profile.last_session))
    sample_data['root_frame'] = sample_filter(sample_mapper(sample_data['root_frame']))
    return ret, sample_data


def do_sample(rate):
    return not random.randrange(0, rate)

def do_log(worker, msg):
    if hasattr(worker, 'apm_log'):
        worker.apm_log.info(msg)
    else:
        worker.log.info(msg)



def wsgi_wrapper(
        worker,
        sample_rate,
        sample_filter,
        sample_mapper,
        wsgi
):

    if hasattr(wsgi, 'origin'):
        return wsgi

    @wraps(wsgi)
    def _(environ, resp, *args, **kwargs):
        _.origin = wsgi

        start_time = time()

        if do_sample(sample_rate):
            ret, profile = profile_fn(partial(wsgi, environ, resp, *args, **kwargs), sample_filter, sample_mapper)
        else:
            ret, profile = wsgi(environ, resp, *args, **kwargs), {}

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
            'stacktrace': profile
        }

        do_log(worker, record)
        return ret
    return _


def trace_wsgi(worker, sample_rate=1, sample_filter=lambda x: x, sample_mapper=tree2list):
    worker.wsgi.wsgi_app = wsgi_wrapper(
        worker,
        sample_rate,
        sample_filter,
        sample_mapper,
        worker.wsgi.wsgi_app,
    )


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
