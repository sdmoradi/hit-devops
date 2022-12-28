from flask import Flask, jsonify, render_template, request
import sys
from datetime import datetime
import logging
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    req_time = datetime.now().strftime("%Y-%d-%m  %H:%M:%S")
    log = {
        "url": request.url,
        "time": req_time,
        "client_ip": request.remote_addr,
        "service_name": "medusa"
    }
    app.logger.error(log)
    return render_template("index.html")


@app.route("/version", methods=["GET", "POST"])
def version():
    version = "0.0.0"
    with open("version.txt") as f:
        version = f.read()
    output = {"APP": "Medusa", "Version": version.strip()}
    return jsonify(output)


if __name__ == "__main__":
    handler = logging.StreamHandler(sys.stdout)
    app.logger.addHandler(handler)
    app.run(debug=True)
