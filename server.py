from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import requests

app = Flask(__name__)
CORS(app)

relay_state = "OFF"
wifi_name = "UNKNOWN"
last_seen = 0

@app.route("/")
def home():
    return "ESP01S Web Server Running"

@app.route("/relay", methods=["GET", "POST"])
def relay():
    global relay_state, wifi_name, last_seen

    if request.method == "POST":
        data = request.get_json(silent=True)
        if data:
            if data.get("state") in ["ON", "OFF"]:
                relay_state = data["state"]
            if "wifi" in data:
                wifi_name = data["wifi"]
            last_seen = int(time.time())

        return jsonify({
            "state": relay_state,
            "wifi": wifi_name,
            "online": True
        })

    online = (time.time() - last_seen) < 30

    return jsonify({
        "state": relay_state,
        "wifi": wifi_name,
        "online": online
    })


# ===== ANTI SLEEP (Render Free) =====
def keep_alive():
    while True:
        try:
            requests.get("https://esp01s-webserver01.onrender.com/")
        except:
            pass
        time.sleep(600)  # 10 phút

threading.Thread(target=keep_alive, daemon=True).start()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
