import threading
from fastapi import FastAPI, WebSocket, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from conf.db_conf import init_db
from modules.crypto.routes import crypto_router
from modules.alerts.router import alerts_router
from modules.crypto.services.binance import start_binance_ws
from conf.tasks import check_and_send_alerts

# create main app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (need to configure for security reasons)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# include remaining app routes
app.include_router(crypto_router)
app.include_router(alerts_router)

# scheduler = BackgroundScheduler()
scheduler = AsyncIOScheduler()
def start_scheduler():
    scheduler.add_job(check_and_send_alerts, IntervalTrigger(minutes=5))
    scheduler.start()

@app.on_event("startup")
def startup_event():
    """Start necessary connections and background tasks on FastAPI startup."""
    init_db()
    threading.Thread(target=start_binance_ws, daemon=True).start() # Start Binance WebSocket in the background
    start_scheduler()
    

@app.on_event("shutdown")
def shutdown():
    """Shutdown the scheduler gracefully when FastAPI app shuts down."""
    scheduler.shutdown()