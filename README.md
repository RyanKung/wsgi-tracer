wsgi_tracer
================

# TL;DR

wsgi-tracer is a AMP implentation for WSGI(PEP3333) protocol based application by workaround `gunicorn`.

## Design:

T0: T0, ts
D <---------------->E
                    |
T1: hash(T0), ts   / \
			      /   \
			     X     Y
				 |
T2: hash(T1), ts |
				 |
T3: hash(T2),ts	 Z


1. Device D request Endpoint Server E with tracer `<T0, ts_0>`;
2. Endpoint Server E recieved `<T0, ts_0>` and request:
   2.1 X with `hash(T0), ts_1` as `T1`, which response `hash(T1), ts_2`
   2.2 Y with `hash(T0), ts_3` as `T1`
       2.2.1 and request Z with `hash(T1), ts_4` as `T2` which response `hash(T2), ts_5`
       2.2.2 and response `(hash(T2), ts_5), (hash(T1), ts_6)`
   and response / log:
   `(hash(T0), ts_0), (hash(T0), ts_1), (hash(T1), ts_2),
    (hash(T0), ts_3), (hash(T1), ts_4), (hash(T2), ts_5),
	(hash(T1), ts_6)`

# Protocol

For integration, any devices should add `X-APM-TRACER=<uuid>:<timestamp>` to request HEADERS.

For Monitor, we provide JSON as LOG output:

* JSON:

```json
{
	version: <wsgi_tracer version: &str>,
	proc_name: <proc name: &str>,
	endpoint: <http_url: &str>,
	stacktrace: <stack_trace_log>,
	request: {
        trace_id: <Request TracerID: &str>,
		req_time: <Request timestamp: u32>,
		resp_time: <Response timestamp: u32>,
	}
}
```
