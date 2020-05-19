from wsgi_tracer.tracer import wsgi_wrapper, setup_logger
import os

__all__ = ['wsgi_wrapper', 'setup_logger', 'pre_fork', 'pre_request']



def pre_fork(server, worker):
    logfile = logfile = os.getenv('apm_logfile', None)
    setup_logger(worker, logfile)


def pre_request(worker, req):
    worker.wsgi.wsgi_app = wsgi_wrapper(worker, worker.wsgi.wsgi_app)
