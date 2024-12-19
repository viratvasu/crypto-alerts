import os
from dotenv import load_dotenv

load_dotenv()

ENV_FILE = os.getenv("ENV_FILE", ".env")


class APISettings():
    DB_URL: str = os.getenv("DB_URL")
    BINANCE_WS_URL :str = os.getenv("BINANCE_WS_URL")
    TOP_CRYPTOS: str = os.getenv("TOP_CRYPTOS", "").split(",")
    
api_settings = APISettings()