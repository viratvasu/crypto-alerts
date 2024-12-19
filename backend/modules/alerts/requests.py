from pydantic import BaseModel


class CryptoAlertCreate(BaseModel):
    user_email: str
    crypto_symbol: str
    price_threshold: float
    condition: str  # 'above' or 'below'