from flask import Flask, render_template, jsonify
from datetime import datetime
import socket
import psutil
import os

app = Flask(__name__)

refresh_counter = 0


def get_private_ip():
    """
    Returns container/private IP address.
    Works on Docker as well as AWS EC2.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Unavailable"


@app.route("/")
def home():
    global refresh_counter
    refresh_counter += 1

    instance_name = os.getenv("APP_NAME", "Unknown Instance")
    container_hostname = socket.gethostname()

    cpu = psutil.cpu_percent(interval=0.2)
    memory = psutil.virtual_memory().percent

    return render_template(
        "index.html",
        hostname=instance_name,
        container_hostname=container_hostname,
        private_ip=get_private_ip(),
        cpu=cpu,
        memory=memory,
        refresh=refresh_counter,
        current_time=datetime.now().strftime("%d %b %Y | %I:%M:%S %p"),
    )


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "instance": os.getenv("APP_NAME", "Unknown Instance"),
        "hostname": socket.gethostname()
    }), 200


@app.route("/info")
def info():
    return jsonify({
        "instance": os.getenv("APP_NAME", "Unknown Instance"),
        "hostname": socket.gethostname(),
        "private_ip": get_private_ip(),
        "cpu": psutil.cpu_percent(interval=0.2),
        "memory": psutil.virtual_memory().percent,
        "refresh_count": refresh_counter
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )