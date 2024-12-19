from sqlalchemy import Column, Integer, String, Float, Boolean
from conf.db_conf import Base

# Database Models
class CryptoAlert(Base):
    __tablename__ = "crypto_alerts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)  # User identifier
    symbol = Column(String, index=True)  # Cryptocurrency symbol
    price_threshold = Column(Float, nullable=False)  # Price threshold
    is_triggered = Column(Boolean, default=False)  # Trigger status
