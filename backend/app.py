from fastapi import FastAPI, WebSocket, HTTPException, Depends
import threading
import asyncio
from sqlalchemy.orm import Session
from database import SessionLocal, CryptoAlert, init_db
from binance import start_binance_ws, crypto_prices, TOP_CRYPTOS

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Start WebSocket in a separate thread
@app.on_event("startup")
def startup_event():
    """Start necessary background tasks on FastAPI startup."""
    init_db()
    # Start Binance WebSocket in the background
    threading.Thread(target=start_binance_ws, daemon=True).start()


@app.get("/prices")
def get_prices():
    """Endpoint to fetch current cryptocurrency prices in INR."""
    global crypto_prices
    return {"crypto_prices": crypto_prices}


@app.websocket("/ws/prices")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint to stream live crypto prices in INR."""
    await websocket.accept()
    try:
        while True:
            await websocket.send_json({"crypto_prices": crypto_prices})
            await asyncio.sleep(1)  # Push updates every second
    except Exception as e:
        print("WebSocket Error:", e)
    finally:
        await websocket.close()
        

@app.post("/alerts/")
def create_alert(user_id: str, symbol: str, price_threshold: float, db: Session = Depends(get_db)):
    """Create a new price alert."""
    if symbol not in TOP_CRYPTOS:
        raise HTTPException(status_code=400, detail="Unsupported cryptocurrency.")
    alert = CryptoAlert(user_id=user_id, symbol=symbol, price_threshold=price_threshold)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert
   

@app.get("/alerts/")
def get_alerts(user_id: str = None, db: Session = Depends(get_db)):
    """Retrieve all alerts or alerts for a specific user."""
    if user_id:
        return db.query(CryptoAlert).filter(CryptoAlert.user_id == user_id).all()
