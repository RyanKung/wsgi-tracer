import os
from functools import partial

from wsgi_tracer.tracer import trace_wsgi, setup_logger, tree2list, filter_time

proc_name = "sampleapp"



def pre_fork(server, worker):
    logfile = logfile = os.getenv('apm_logfile', None)
    setup_logger(worker, logfile)


def pre_request(worker, req):
    trace_wsgi(worker, sample_rate=1, sample_mapper=tree2list, sample_filter=partial(filter_time, threshold=0.5))
