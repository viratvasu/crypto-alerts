import asyncio
from fastapi import APIRouter,WebSocket
from conf.cache import crypto_prices

crypto_router = APIRouter()

@crypto_router.get("/prices")
def get_prices():
    """Endpoint to fetch current cryptocurrency prices in INR."""
    global crypto_prices
    return {"crypto_prices": crypto_prices}

@crypto_router.websocket("/ws/prices")
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