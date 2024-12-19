import json
import time
from websocket import WebSocketApp

TOP_CRYPTOS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "DOGEUSDT"]
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws"
crypto_prices = {}  # Dictionary to store prices

def start_binance_ws():
    """Start Binance WebSocket connection with reconnection support."""
    def on_message(ws, message):
        global crypto_prices
        data = json.loads(message)
        symbol = data.get("s")  # Symbol
        price = float(data.get("c", 0))  # Current price in USDT
        crypto_prices[symbol] = price
        print(crypto_prices)

    def on_open(ws):
        """Callback when WebSocket opens."""
        payload = {
            "method": "SUBSCRIBE",
            "params": [f"{crypto.lower()}@ticker" for crypto in TOP_CRYPTOS],
            "id": 1,
        }
        ws.send(json.dumps(payload))
        print("Subscribed to Binance WebSocket streams.")

    def on_error(ws, error):
        """Callback when there is an error."""
        print(f"WebSocket Error: {error}")

    def on_close(ws, close_status_code, close_msg):
        """Callback when WebSocket closes."""
        print(f"WebSocket closed: {close_status_code} - {close_msg}")
        print("Attempting to reconnect...")
        reconnect()

    def reconnect():
        """Reconnect with exponential backoff."""
        delay = 1  # Start with a 1-second delay
        max_delay = 60  # Cap the delay at 60 seconds
        while True:
            try:
                print(f"Reconnecting in {delay} seconds...")
                time.sleep(delay)
                ws = create_ws()
                ws.run_forever()
                break  # Exit loop on successful connection
            except Exception as e:
                print(f"Reconnect failed: {e}")
                delay = min(max_delay, delay * 2)  # Increase the delay (exponential backoff)

    def create_ws():
        """Create a WebSocketApp instance."""
        return WebSocketApp(
            BINANCE_WS_URL,
            on_message=on_message,
            on_open=on_open,
            on_error=on_error,
            on_close=on_close,
        )

    # Initial WebSocket connection
    ws = create_ws()
    ws.run_forever()