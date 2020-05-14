import os
from flask import Flask
from functools import reduce
import time

app = Flask(__name__)

def some_fn():
    time.sleep(1)
    return "pong"

@app.route('/')
def pong():
    time.sleep(1)
    return some_fn()

wsgi_app = app.wsgi_app

if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=os.getenv("PORT", 8000))
