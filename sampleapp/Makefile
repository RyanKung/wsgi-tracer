run:
	gunicorn --config config.py pong.pong:app --env=apm_logfile=/var/log/apps/apm.log
beat:
	filebeat -e -v -c $(PWD)/filebeat.yml
