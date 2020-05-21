wsgi_tracer
================

# TL;DR

wsgi-tracer is a AMP implentation for WSGI(PEP3333) protocol based application by workaround `gunicorn`.

```
pip install wsgi_tracer
```

# Design:

						+----------------------------------+
						|                                  |
						|            WSGI APP              |
						|  (Flask/Django/AIOHTTP/Etc...)   |
						+----------------------------------+
						                 |
						                 |
						+----------------------------------+
						|                                  |
						|             wsgi_tracer:         |
						|        Callable[wsgi] -> wsgi    |
						+----------------------------------+
						                 |
						                 |
						+-----------------------------------+
						|                                   |
						|  Gunicorn.worker.wsgi.wsgi_app    |
						| Callable[Env, resp] -> Iterable   |
						+-----------------------------------+


# Protocol

For integration, any requester should add `X-APM-TRACER=<uuid>:<timestamp>` to request HEADERS.

For Monitor, we provide JSON as LOG output:

* JSON:

```json
{
	version: <wsgi_tracer version: &str>,
	proc_name: <proc name: &str>,
	services: <server name>:<server port>,
	protocol: <request protocol>,
	endpoint: <http_url: &str>,
	stacktrace: <stack_trace_log>,
	apitrace: {
        trace_id: <Request TracerID: &str>,
		req_time: <Request timestamp: u32>,
		resp_time: <Response timestamp: u32>,
	}
}
```

# Usage


```python
import os
from functools import partial

from wsgi_tracer.tracer import trace_wsgi, setup_logger, tree2list
from wsgi_tracer.filter import compose, threshold_time, app_only

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
                partial(app_only, worker=worker)
            ]
        )
    )
```

# Customize Filter & Mapper

Mapper & Filter should obey follow types:

```python
Callable[data, args] -> data
```

Example:

```
def module_path(data, path):
    return [d for d in data if path in d['file_path']]


def app_only(data, worker):
    return [d for d in data if worker.wsgi.root_path in d['file_path']]
```
