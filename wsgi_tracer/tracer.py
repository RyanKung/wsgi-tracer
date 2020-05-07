from pyinstrument import Profiler
from pyinstrument.renderers import JSONRenderer
from time import time
import json

proc_name = 'wsgi_tracer'

def get_tracer_info(env):
    return env.get('HTTP_X_APM_TRACER', "null:null").split(":")


def pre_request(worker, req):
    worker.profiler = Profiler()
    worker.profiler.start()


def post_request(worker, req, environ, resp):
    worker.profiler.stop()
    traceid, ts = get_tracer_info(environ)
    record = {
        'versionn': 'v1',
        'proc_name': proc_name,
        'services': "%s:%s" % (environ['SERVER_NAME'], environ['SERVER_PORT']),
        'protocol': environ['SERVER_PROTOCOL'],
        'endpoint': environ['PATH_INFO'],
        'apitrace': {
            'trace_id': traceid,
            'req_time': ts,
            'resp_time': time()
        },
        'stacktrace': json.loads(JSONRenderer().render(session=worker.profiler.last_session))
    }
    print(record)
