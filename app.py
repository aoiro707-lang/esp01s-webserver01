from flask import Flask, request, jsonify, render_template
import time

app = Flask(__name__)

relay_state = "OFF"
wifi_name = "UNKNOWN"
last_ping = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/relay")
def relay():
    global relay_state
    state = request.args.get("state")
    if state in ["ON", "OFF"]:
        relay_state = state
    return jsonify({"state": relay_state})

@app.route("/status")
def status():
    online = (time.time() - last_ping) < 10
    return jsonify({
        "online": online,
        "state": relay_state,
        "wifi": wifi_name if online else ""
    })

@app.route("/ping")
def ping():
    global last_ping, wifi_name
    wifi_name = request.args.get("wifi", "UNKNOWN")
    last_ping = time.time()
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
