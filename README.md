# MEXC Spot Trading Bot

This repository provides a simple Python script that can place a spot limit order on MEXC and forward the exchange response to a Telegram chat.

## Usage

1. Export the required environment variables:
   - `MEXC_API_KEY`
   - `MEXC_API_SECRET`
   - `TELEGRAM_TOKEN`
   - `TELEGRAM_CHAT_ID`
2. Run the script:

```bash
python mexc_bot.py
```

When all variables are provided, the bot submits a BTCUSDT limit order and sends the JSON response to the configured Telegram chat. Without credentials the script prints a helpful message and exits.
