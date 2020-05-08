from pyinstrument import Profiler
from pyinstrument.renderers import JSONRenderer
from time import time
import json

proc_name = 'wsgi_tracer'

def get_tracer_info(env):
    return env.get('HTTP_X_APM_TRACER', "null:null")


def pre_request(worker, req):
    worker.profiler = Profiler()
    worker.profiler.start()
    worker.start_time = time()


def post_request(worker, req, environ, resp):
    worker.profiler.stop()
    record = {
        'versionn': 'v1',
        'proc_name': proc_name,
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
    worker.log.info(record)
