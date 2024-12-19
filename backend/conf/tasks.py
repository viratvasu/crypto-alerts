from sqlalchemy import or_
from conf.db_conf import get_db
from conf.cache import crypto_prices
from modules.alerts.models import CryptoAlert, CryptoAlertHistory
from datetime import datetime, timedelta
import logging
from utilities.mail import Emailservice

alert_cooldown_time = 10 # in minutes # TODO: move this to config

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_alert_email_template_data(email, symbol, current_price):
    return """
    Hi {},\n
    Your alert for {} has been triggered.\n
    Current price is {}\n
    """.format(email, symbol, current_price)
  
  
async def check_and_send_alerts():
    logger.info("starting the alert sending...")

    global crypto_prices
    db = next(get_db())

    for symbol, current_crypto_price in crypto_prices.items():
        # Fetch active alerts for each crypto symbol and apply the conditions
        alerts = db.query(CryptoAlert).filter(
            CryptoAlert.is_active == True,
            CryptoAlert.crypto_symbol == symbol,  # Match alert's symbol with the dictionary key (e.g., 'BTC')
            or_(
                CryptoAlert.last_alert_sent_at == None,
                CryptoAlert.last_alert_sent_at < datetime.utcnow() - timedelta(minutes=alert_cooldown_time)
            ),
            # Only select alerts that match the crypto price condition
            or_(
                (CryptoAlert.condition == "above") & (current_crypto_price > CryptoAlert.price_threshold),
                (CryptoAlert.condition == "below") & (current_crypto_price < CryptoAlert.price_threshold)
            )
        ).all()

        logger.debug(f"Fetched alerts for symbol {symbol}: {alerts}")
        
        if not alerts:
            logger.info(f"No active alerts for {symbol} that match the conditions.")
        
        for alert in alerts:
            logger.info(f"Processing alert: {alert.id}, Sending price: {current_crypto_price}")
            
            # send an email notification
            await Emailservice.send_email(get_alert_email_template_data(alert.user_email, symbol, current_crypto_price),recipients=[alert.user_email], subject="Alert for {}".format(symbol))

            # Create a record in CryptoAlertHistory
            alert_history = CryptoAlertHistory(
                alert_id=alert.id,
                sent_price=current_crypto_price,
                notification_status="sent",  # Assuming this value indicates successful notification
                alert_received_at=datetime.utcnow(),
                notification_sent_at=datetime.utcnow(),
                is_active=True,
                created_at=datetime.utcnow()
            )

            try:
                db.add(alert_history)  # Add the alert history record to the session
                db.commit()  # Commit the changes to the DB
                logger.info(f"Alert history for alert {alert.id} successfully saved.")
            except Exception as e:
                logger.error(f"Failed to commit the alert history for alert {alert.id}. Error: {e}")
                db.rollback()  # Rollback the transaction on error
            
            try:
                alert.last_alert_sent_at = datetime.utcnow()
                alert.last_alert_sent_price = current_crypto_price
                db.commit()  # Commit the changes to the CryptoAlert
                logger.info(f"Alert {alert.id} updated with new alert sent time and price.")
            except Exception as e:
                logger.error(f"Failed to commit updates for alert {alert.id}. Error: {e}")
                db.rollback()  # Rollback on error
