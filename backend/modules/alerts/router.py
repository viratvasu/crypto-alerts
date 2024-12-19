from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from conf.db_conf import get_db
from modules.alerts.requests import CryptoAlertCreate
from modules.alerts.repository import AlertRepo

alerts_router = APIRouter()

@alerts_router.post("/alerts/")
async def create_alert(alert: CryptoAlertCreate, db: Session = Depends(get_db)):
    """Create a new price alert."""
    # TODO: implement validations if any
    return await AlertRepo.create_alert(alert, db)

@alerts_router.put("/alerts/{alert_id}")
async def update_alert(alert_id: int, alert_data: CryptoAlertCreate, db: Session = Depends(get_db)):
    """updated given alert"""
    alert_obj = await AlertRepo.get_alert(alert_id, db)
    if not alert_obj:
        raise HTTPException(status_code=404, detail="Alert not found.")
    #TODO: implement validations 
    return await AlertRepo.update_alert(alert_obj, alert_data, db)

@alerts_router.delete("/alerts/{alert_id}")
async def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    """inactivate or delete given alert"""
    alert_obj = await AlertRepo.get_alert(alert_id, db)
    if not alert_obj:
        raise HTTPException(status_code=404, detail="Alert not found.")
    return await AlertRepo.inactive_alert(alert_obj, db)

@alerts_router.get("/alerts/user/{user_email}")
async def get_user_alerts(user_email: str, db: Session = Depends(get_db)):
    """return all the active alerts"""
    return await AlertRepo.get_all_alerts(user_email, db)

@alerts_router.get("/alerts/{alert_id}/history")
async def get_alert_history(alert_id: int, db: Session = Depends(get_db)):
    return await AlertRepo.get_alert_history(alert_id, db)