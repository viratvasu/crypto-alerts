import os
from dotenv import load_dotenv

load_dotenv()

ENV_FILE = os.getenv("ENV_FILE", ".env")


class APISettings():
    DB_URL: str = os.getenv("DB_URL")
    BINANCE_WS_URL :str = os.getenv("BINANCE_WS_URL")
    TOP_CRYPTOS: str = os.getenv("TOP_CRYPTOS", "").split(",")
    
class EmailSettings():
    MAIL_USERNAME = str = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = str = os.getenv('MAIL_PASSWORD')
    MAIL_SERVER = str = os.getenv('MAIL_SERVER')
    MAIL_FROM = str = os.getenv('MAIL_FROM')
    
api_settings = APISettings()
email_settings = EmailSettings()