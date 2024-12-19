from fastapi import FastAPI, WebSocket, HTTPException, Depends
import threading
from conf.db_conf import init_db
from modules.crypto.routes import crypto_router
from modules.alerts.router import alerts_router
from modules.crypto.services.binance import start_binance_ws

# create main app
app = FastAPI()

# include remaining app routes
app.include_router(crypto_router)
app.include_router(alerts_router)

@app.on_event("startup")
def startup_event():
    """Start necessary connections and background tasks on FastAPI startup."""
    init_db()
    threading.Thread(target=start_binance_ws, daemon=True).start() # Start Binance WebSocket in the background
