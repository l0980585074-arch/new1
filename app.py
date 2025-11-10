from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# 🏠 首頁（Render 測試頁）
@app.route("/", methods=["GET"])
def home():
    return "Webhook server running 🌐", 200

# 📩 接收 TradingView 或外部訊號
@app.route("/signal", methods=["POST"])
def signal():
    data = request.get_json()
    print("✅ Signal received:", data)

    action = data.get("action")
    symbol = data.get("symbol")
    qty = data.get("qty")

    if action == "buy":
        print(f"[TEST MODE] BUY {symbol} {qty}")
    elif action == "sell":
        print(f"[TEST MODE] SELL {symbol} {qty}")
    else:
        print("⚠️ Unknown action")

    return jsonify({"status": "ok", "received": data}), 200

# 💖 UptimeRobot 保活用的 Ping 路由
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "message": "pong 💕"}), 200

# 🚀 Render 啟動設定
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
