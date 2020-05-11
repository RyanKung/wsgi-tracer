from gunicorn.config import Setting
from gunicorn.config import validate_string
from gunicorn.config import KNOWN_SETTINGS

class APMLog(Setting):
    name = "apm_logfile"
    section = "Logging"
    cli = ["--apm-logfile"]
    meta = "FILE"
    validator = validate_string
    default = None
    desc = """\
        The APM log file to write to, for default, will write to errofile
        """

KNOWN_SETTINGS.append(APMLog)
