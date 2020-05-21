run:
	gunicorn --config config.py djangoapp.wsgi
test:
	gunicorn --config config.py djangoapp.wsgi --workers=1 --timeout=1000000

test_async:
	gunicorn --config config.py djangoapp.wsgi --workers=1 --timeout=1000000 -k=gevent
