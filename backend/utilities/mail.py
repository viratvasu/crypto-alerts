import base64
import io
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from conf.settings import email_settings

conf = ConnectionConfig(
    MAIL_USERNAME=email_settings.MAIL_USERNAME,
    MAIL_PASSWORD=email_settings.MAIL_PASSWORD,
    MAIL_FROM=email_settings.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER=email_settings.MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


class Emailservice:
    @staticmethod
    async def send_email(html_content, recipients, attachments=[], cc_recipients = [], subject=""):
        try:

            email_attachments  = []

            message = MessageSchema(
                subject=subject,
                recipients=recipients,
                cc=cc_recipients,
                body=html_content,
                subtype=MessageType.html,
                attachments=email_attachments
            )
            fm = FastMail(conf)

            resp = await fm.send_message(message)
            return 'success'
        except Exception as ex:
            print(ex)
            return 'failure'