wsgi-tracer
================

# TL;DR

wsgi-tracer is a AMP implentation for WSGI(PEP3333) protocol based application by workaround `gunicorn`.

# Protocol

For integration, end devices should add `X-APM-TRACER=<uuid>:<timestamp>` to request HEADERS.
