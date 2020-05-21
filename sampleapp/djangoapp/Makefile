run:
	gunicorn --config config.py djangoapp.wsgi
test:
	gunicorn --config config.py djangoapp.wsgi --workers=1 --timeout=1000000
