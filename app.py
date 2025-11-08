from flask import Flask, request
import requests, hmac, hashlib, time, os

app = Flask("pionex-webhook")

API_KEY = os.environ.get("PIONEX_API_KEY")
SECRET = os.environ.get("PIONEX_SECRET")

def pionex_request(endpoint, data):
    timestamp = str(int(time.time() * 1000))
    payload = f"{endpoint}{timestamp}{data}".encode()
    sign = hmac.new(SECRET.encode(), payload, hashlib.sha256).hexdigest()
    headers = {
        "PIONEX-KEY": API_KEY,
        "PIONEX-SIGNATURE": sign,
        "PIONEX-TIMESTAMP": timestamp,
        "Content-Type": "application/json"
    }
    return requests.post(f"https://api.pionex.com{endpoint}", headers=headers, data=data)

@app.route("/signal", methods=["POST"])
def signal():
    data = request.json
    print("✅ 收到訊號：", data)

    if data.get("action") == "buy":
        order = '{"symbol":"BTC_USDT","side":"BUY","type":"MARKET","quantity":0.01}'
        pionex_request("/api/v1/order", order)
    elif data.get("action") == "sell":
        order = '{"symbol":"BTC_USDT","side":"SELL","type":"MARKET","quantity":0.01}'
        pionex_request("/api/v1/order", order)

    return {"status": "ok"}

if "pionex-webhook" == "main":
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

