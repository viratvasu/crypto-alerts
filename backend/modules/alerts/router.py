from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from conf.db_conf import get_db

alerts_router = APIRouter()

# @alerts_router.post("/alerts/")
# def create_alert(user_id: str, symbol: str, price_threshold: float, db: Session = Depends(get_db)):
#     """Create a new price alert."""
#     if symbol not in TOP_CRYPTOS:
#         raise HTTPException(status_code=400, detail="Unsupported cryptocurrency.")
#     alert = CryptoAlert(user_id=user_id, symbol=symbol, price_threshold=price_threshold)
#     db.add(alert)
#     db.commit()
#     db.refresh(alert)
#     return alert
   

# @alerts_router.get("/alerts/")
# def get_alerts(user_id: str = None, db: Session = Depends(get_db)):
#     """Retrieve all alerts or alerts for a specific user."""
#     if user_id:
#         return db.query(CryptoAlert).filter(CryptoAlert.user_id == user_id).all()