from flask import Flask, render_template
import socket
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    hostname = socket.gethostname()

    return render_template(
        "index.html",
        hostname=hostname,
        current_time=datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    )

@app.route("/health")
def health():
    return {
        "status": "healthy"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)