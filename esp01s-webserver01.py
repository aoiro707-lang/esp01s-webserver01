from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import requests

app = Flask(__name__)
CORS(app)

relay_state = "OFF"
@app.route("/relay", methods=["GET", "POST"])
def relay():
    global relay_state, wifi_name, esp_online

    if request.method == "POST":
        data = request.get_json()
        if data:
            if data.get("state") in ["ON", "OFF"]:
                relay_state = data["state"]
            if "wifi" in data:
                wifi_name = data["wifi"]
            esp_online = True

        return jsonify({
            "state": relay_state,
            "wifi": wifi_name,
            "online": esp_online
        })

    return jsonify({
        "state": relay_state,
        "wifi": wifi_name,
        "online": esp_online
    })


@app.route("/")
def home():
    return "ESP01S Server Running"

@app.route("/relay", methods=["GET", "POST"])
def relay():
    global relay_state

    if request.method == "POST":
        data = request.get_json()
        if data and data.get("state") in ["ON", "OFF"]:
            relay_state = data["state"]
        return jsonify({"state": relay_state})

    return jsonify({"state": relay_state})


# ====== ANTI SLEEP (Render Free) ======
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
