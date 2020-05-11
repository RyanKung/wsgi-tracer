from gunicorn.glogging import Logger

class APMLogger(Logger):
    def with_logfile(self, f):
        self.logfile = f
