run:
	gunicorn --config config.py pong.pong:app --env=apm_logfile=/var/log/apps/apm.log
test:
	gunicorn --config config.py pong.pong:app --timeout=1000000 --workers=1
test_async:
	gunicorn --config config.py pong.pong:app --timeout=1000000 --workers=1 --worker_class=gevent

beat:
	filebeat -e -v -c $(PWD)/filebeat.yml
