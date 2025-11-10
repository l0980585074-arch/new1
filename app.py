from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# 🏠 首頁（測試 Render 是否啟動）
@app.route("/", methods=["GET"])
def home():
    return "Webhook server running 🌐", 200


# 📩 接收 TradingView / 外部訊號
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

    return jsonify({"status": "ok", "received": data})


# 💖 自動喚醒 Render：UptimeRobot 會定時打這條
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "message": "pong 💕"}), 200


# 🚀 啟動 Flask（Render 自動設定 PORT）
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
