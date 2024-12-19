from modules.alerts.models import CryptoAlert, CryptoAlertHistory


class AlertRepo:
    @staticmethod
    async def create_alert(data, db_session):
        new_alert = CryptoAlert(
            user_email=data.user_email,
            crypto_symbol=data.crypto_symbol,
            price_threshold=data.price_threshold,
            condition=data.condition
        )

        db_session.add(new_alert)
        db_session.commit()
        db_session.refresh(new_alert)
        return new_alert
    
    @staticmethod
    async def get_alert(id, db_session):
        return db_session.query(CryptoAlert).filter(CryptoAlert.id == id, CryptoAlert.is_active == True).first()
    
    @staticmethod
    async def update_alert(alert_obj, data, db_session):
      alert_obj.price_threshold = data.price_threshold
      alert_obj.condition = data.condition
      db_session.commit()
      db_session.refresh(alert_obj)
      return alert_obj
    
    @staticmethod
    async def inactive_alert(alert_obj, db_session):
      alert_obj.is_active = False
      db_session.commit()
      db_session.refresh(alert_obj)
      return alert_obj
    
    @staticmethod
    async def get_all_alerts(user_email, db_session):
      return db_session.query(CryptoAlert).filter(CryptoAlert.user_email == user_email, CryptoAlert.is_active == True).all()
    
    @staticmethod
    async def get_alert_history(alert_id, db_session):
      return db_session.query(CryptoAlertHistory).filter(CryptoAlertHistory.alert_id == alert_id).all()