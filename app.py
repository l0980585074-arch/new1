from flask import Flask, request, jsonify
import requests, time, hmac, hashlib, json, os
from datetime import datetime

app = Flask(__name__)

# ======== 你的派網 API 資訊 ========
API_KEY = "8p8EdGuzjN1Kw79s4vjjdDYZooBorzqgN9pZ7kxEwQ2Y9dAbi9KQJmuVpJuEGPFHb9"
API_SECRET = "HoAjDCVkMf4gWjiM77vW1Gtzrwpd6yhFA3AbdJMps0SSjJKIK4RHWF9tvqNAWIQS"
BASE_URL = "https://api.pionex.com"

# ======== 基礎測試用路由 ========

@app.route("/", methods=["GET"])
def home():
    return "Webhook server running 🌐", 200

@app.route("/ping", methods=["GET"])
def ping():
    print(f"✅ Ping received from UptimeRobot at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    return jsonify({"status": "ok", "message": "pong 💕"}), 200


# ======== 下單邏輯 ========

def make_signature(secret, payload):
    """產生 Pionex API 驗證簽章"""
    return hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()

def place_order(symbol, side, qty):
    """下市價單"""
    timestamp = str(int(time.time() * 1000))
    body = {
        "symbol": symbol,
        "orderType": "MARKET",
        "side": side,
        "quantity": qty
    }

    payload = json.dumps(body)
    sign = make_signature(API_SECRET, payload + timestamp)

    headers = {
        "X-API-KEY": API_KEY,
        "X-API-SIGN": sign,
        "X-API-TIMESTAMP": timestamp,
        "Content-Type": "application/json"
    }

    res = requests.post(f"{BASE_URL}/api/v1/order", headers=headers, data=payload)
    print(f"📦 下單回應：{res.json()}")
    return res.json()


def close_all(symbol):
    """簡易版平倉（示範用，可未來加查倉位再平）"""
    print(f"🚪 平倉 {symbol}（目前僅示範）")
    return {"status": "ok", "message": f"{symbol} 平倉指令完成（示範）"}


# ======== TradingView webhook 接收 ========

@app.route("/signal", methods=["POST"])
def signal():
    data = request.get_json()
    print(f"📩 收到 TradingView 訊號：{data}")

    action = data.get("action")
    symbol = data.get("symbol", "BTCUSDT")
    qty = data.get("qty", 0.01)

    if action == "buy":
        result = place_order(symbol, "BUY", qty)
    elif action == "sell":
        result = place_order(symbol, "SELL", qty)
    elif action == "close":
        result = close_all(symbol)
    else:
        result = {"status": "error", "message": "未知的指令"}

    return jsonify(result), 200


# ======== 主程式入口 ========

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
