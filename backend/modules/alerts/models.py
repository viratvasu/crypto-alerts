import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Float, Boolean, Enum
from conf.db_conf import Base

# class ConditionEnum(enum.Enum):
#     above = "above"
#     below = "below"
  
# class NotificationStatusEnum(enum.Enum):
#     pending = "pending"
#     sent = "sent"
#     failed = "failed"

# Database Models
class CryptoAlert(Base):
    __tablename__ = "crypto_alerts"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String)
    crypto_symbol = Column(String, index=True)
    price_threshold = Column(Float, nullable=False)  # Price threshold
    condition = Column(String) # above/below # TODO: can use enums here instead
    last_alert_sent_at = Column(DateTime)
    last_alert_sent_price = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

class CryptoAlertHistory(Base):
    __tablename__ = "crypto_alert_history"
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("crypto_alerts.id"))
    sent_price = Column(Float)
    notification_status = Column(String) # TODO: can use enums here instead
    alert_received_at = Column(DateTime)
    notification_sent_at = Column(DateTime)
    is_active = Column(Boolean)
    created_at = Column(DateTime)
    
    
