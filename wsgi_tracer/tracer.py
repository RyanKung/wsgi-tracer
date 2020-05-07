from pyinstrument import Profiler
from pyinstrument.renderers import JSONRenderer

proc_name = 'wsgi_tracer'

def pre_request(worker, req):
    worker.profiler = Profiler()
    worker.profiler.start()


def post_request(worker, req, environ, resp):
    worker.profiler.stop()
    print(JSONRenderer().render(session=worker.profiler.last_session))
    print(worker.profiler.output_text(unicode=True, color=True))
