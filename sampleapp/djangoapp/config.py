import os
from functools import partial

from wsgi_tracer.tracer import trace_wsgi, setup_logger, tree2list
from wsgi_tracer.filter import compose, threshold_time, not_include

proc_name = "sampleapp"



def pre_fork(_, worker):
    logfile = logfile = os.getenv('apm_logfile', None)
    setup_logger(worker, logfile)


def pre_request(worker, _):
    trace_wsgi(
        worker,
        sample_rate=1,
        sample_mapper=tree2list,
        sample_filter=compose(
            [
                partial(threshold_time, threshold=0.5),
                partial(not_include, path="django")
            ]
        )
    )
