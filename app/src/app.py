import os
import socket

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify(
        {
            "service": "devops-lab",
            "hostname": socket.gethostname(),
            "version": os.environ.get("APP_VERSION", "1.0.0"),
        }
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/greeting")
def greeting():
    if os.environ.get("FEATURE_NEW_GREETING", "").lower() == "true":
        return jsonify({"greeting": "Hello from the new greeting!"})

    return jsonify({"greeting": "Hello from the old greeting!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
