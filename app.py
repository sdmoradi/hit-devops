import json
import logging
import os
from datetime import datetime

from flask import Flask, jsonify, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# The app is only exposed through the Kubernetes ingress. Trust one proxy hop
# so request.remote_addr resolves to the client IP supplied by that ingress.
# If the ingress topology changes, update this value to match the trusted hops.
if os.getenv("TRUST_PROXY_HEADERS", "true").lower() == "true":
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

handler = logging.StreamHandler()
handler.setStream(__import__("sys").stdout)
handler.setFormatter(logging.Formatter("%(message)s"))
app.logger.handlers.clear()
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
app.logger.propagate = False


def log_request() -> None:
    """Emit one JSON object per request so container log collectors can parse it."""
    event = {
        "url": f"{request.host}{request.path}",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "client_ip": request.remote_addr or "unknown",
        "service_name": "medusa",
    }
    app.logger.info(json.dumps(event, separators=(",", ":"), ensure_ascii=False))


@app.route("/", methods=["GET"])
def home():
    log_request()
    return render_template("index.html")


@app.route("/version", methods=["GET"])
def version():
    log_request()
    with open("version.txt", encoding="utf-8") as version_file:
        app_version = version_file.read().strip()
    return jsonify({"APP": "Medusa", "Version": app_version})


if __name__ == "__main__":
    # Local development only. Production runs under Gunicorn in the container.
    app.run(host="0.0.0.0", port=5000, debug=False)
