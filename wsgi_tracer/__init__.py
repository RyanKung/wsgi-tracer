from wsgi_tracer.tracer import trace_wsgi, setup_logger, tree2list
import os

__all__ = ['setup_logger', 'pre_fork', 'pre_request']



def pre_fork(server, worker):
    logfile = logfile = os.getenv('apm_logfile', None)
    setup_logger(worker, logfile)


def pre_request(worker, req):
    trace_wsgi(worker)
