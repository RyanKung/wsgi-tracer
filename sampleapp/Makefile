run:
	gunicorn --config config.py pong.pong:app --env=apm_logfile=/var/log/apps/apm.log
test:
	gunicorn --config config.py pong.pong:app --timeout=1000000 --workers=1
beat:
	filebeat -e -v -c $(PWD)/filebeat.yml
