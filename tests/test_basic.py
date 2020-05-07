import pytest
import sys
from gunicorn import config
from gunicorn.app.wsgiapp import WSGIApplication
from gunicorn.app.base import Application

from wsgi_tracer import tracer


def get_config():
    return tracer.__file__


class AltArgs:
    def __init__(self, args=None):
        self.args = args or []
        self.orig = sys.argv

    def __enter__(self):
        sys.argv = self.args

    def __exit__(self, exc_type, exc_inst, traceback):
        sys.argv = self.orig



class WSGIApp(WSGIApplication):
    def __init__(self):
        super().__init__("no_usage", prog="gunicorn_test")

    def load(self):
        pass


class NoConfigApp(Application):
    def __init__(self):
        super().__init__("no_usage", prog="gunicorn_test")

    def init(self, parser, opts, args):
        pass

    def load(self):
        pass


def test_defaults():
    c = config.Config()
    for s in config.KNOWN_SETTINGS:
        assert c.settings[s.name].validator(s.default) == c.settings[s.name].get()

def test_callable_validation():
    c = config.Config()
    def func(a, b):
        pass
    c.set("pre_fork", func)
    assert c.pre_fork == func
    pytest.raises(TypeError, c.set, "pre_fork", 1)
    pytest.raises(TypeError, c.set, "pre_fork", lambda x: True)
