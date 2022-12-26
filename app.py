from flask import Flask, jsonify, render_template
import sys
import json
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

log = '{"url": "hit.local/version","time": "2022-01-01 14:22:33","client_ip": "0.0.0.0","service_name": "medusa"}'
json_log = json.loads(log)
json_formatted_log = json.dumps(json_log, indent=1)

@app.route("/", methods=["GET", "POST"])
def home():
    app.logger.info(json_formatted_log)
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
