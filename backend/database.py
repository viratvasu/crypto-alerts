from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database Configuration
SQLITE_DB_URL = "sqlite:///./alerts.db"
engine = create_engine(SQLITE_DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for models
Base = declarative_base()


# Database Models
class CryptoAlert(Base):
    __tablename__ = "crypto_alerts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)  # User identifier
    symbol = Column(String, index=True)  # Cryptocurrency symbol
    price_threshold = Column(Float, nullable=False)  # Price threshold
    is_triggered = Column(Boolean, default=False)  # Trigger status


# Create tables (ensure this runs at least once)
def init_db():
    Base.metadata.create_all(bind=engine)
