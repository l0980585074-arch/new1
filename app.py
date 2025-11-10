from flask import Flask, request
import json, time, os

app = Flask(__name__)

# ---- TEST MODE SWITCH ----
TEST_MODE = True   # ← True = simulate only, False = real order

# ---- MAIN ENDPOINT ----
@app.route("/signal", methods=["POST"])
def signal():
    data = request.json
    print("✅ Signal received:", data)

    action = data.get("action")      # "buy" or "sell"
    symbol = data.get("symbol", "BTC_USDT")
    qty = float(data.get("qty", 0.01))

    # Simulate order
    if TEST_MODE:
        print(f"[TEST MODE] {action.upper()} {symbol} {qty}")
        return {"status": "ok", "mode": "test"}

    # --- REAL ORDER PLACEHOLDER ---
    # Here we will call Pionex API later
    print(f"Real order would be sent: {action.upper()} {symbol} {qty}")
    return {"status": "ok", "mode": "live"}

# ---- START SERVER ----
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
