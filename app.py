from flask import Flask, request, jsonify

app = Flask("app")

@app.route("/", methods=["GET"])
def home():
    return "Webhook server running 🟢", 200

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
