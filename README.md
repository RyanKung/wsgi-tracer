wsgi_tracer
================

# TL;DR

wsgi-tracer is a AMP implentation for WSGI(PEP3333) protocol based application by workaround `gunicorn`.

## Design:

   T0, ts
D <---------------->E <------------------->
                    |
                   / \
			      /   \
			     X     Y



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

# Useage

Add Follow code to your `config.py`
```
from wsgi_tracer import *
```

For seperated APM logging file, use follow arg on your gunicorn command

```
 --env=apm_logfile=apm.log
```
