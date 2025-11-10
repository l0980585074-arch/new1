from flask import Flask, request, jsonify
import os

# 建立 Flask App
app = Flask("app")

# ✅ 首頁路由（檢查伺服器狀態）
@app.route("/", methods=["GET"])
def home():
    return "Webhook server running 🌐", 200

# ✅ 接收訊號路由
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

# 自動喚醒機制：Render 防止睡著，用這個供監控系統 Ping
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "message": "pong 🏓"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
print("✅ Signal received:", data, "🚀")
