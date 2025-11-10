from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Webhook server running 🌐", 200

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong 💥", "status": "ok"}), 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    action = data.get("action")
    symbol = data.get("symbol")
    amount = data.get("amount")

    if action not in ["buy", "sell"]:
        return jsonify({"error": "Invalid action"}), 400

    return jsonify({
        "status": "success",
        "message": f"Executed {action} for {symbol} amount {amount}"
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
