#!/usr/bin/python
# encoding: utf-8

from flask import Flask

from web.api import api

app = Flask(__name__)
app.debug = True

app.register_blueprint(api)


@app.route("/")
def home():
    return app.send_static_file('index.html')


@app.route("/<path:path>")
def load_static(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run(threaded=True)
