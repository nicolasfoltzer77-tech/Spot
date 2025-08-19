import os
import time
import hmac
import hashlib
import requests

API_KEY = os.getenv("MEXC_API_KEY")
API_SECRET = os.getenv("MEXC_API_SECRET")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

BASE_URL = "https://api.mexc.com"


def sign(payload: str) -> str:
    """Return HMAC SHA256 signature."""
    if API_SECRET is None:
        raise ValueError("MEXC_API_SECRET not set")
    return hmac.new(API_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()


def place_order(symbol: str, side: str, type_: str, quantity: str, price: str) -> requests.Response:
    """Place a spot order on MEXC."""
    timestamp = int(time.time() * 1000)
    payload = f"symbol={symbol}&side={side}&type={type_}&quantity={quantity}&price={price}&timestamp={timestamp}"
    signature = sign(payload)
    headers = {"X-MEXC-APIKEY": API_KEY}
    url = f"{BASE_URL}/api/v3/order"
    return requests.post(url, headers=headers, data=f"{payload}&signature={signature}")


def send_telegram(message: str) -> None:
    """Send a message via Telegram bot."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials missing. Skipping message send.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})


def main() -> None:
    required = [API_KEY, API_SECRET, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]
    if not all(required):
        print("Environment variables missing. Set MEXC_API_KEY, MEXC_API_SECRET, TELEGRAM_TOKEN and TELEGRAM_CHAT_ID.")
        return
    try:
        response = place_order("BTCUSDT", "BUY", "LIMIT", "0.001", "20000")
        send_telegram(f"Order response: {response.json()}")
    except Exception as exc:
        print(f"Error placing order or sending message: {exc}")


if __name__ == "__main__":
    main()
