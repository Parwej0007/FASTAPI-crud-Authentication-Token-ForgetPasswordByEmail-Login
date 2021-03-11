from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from typing import List

conf = ConnectionConfig(
    MAIL_USERNAME = "parwejalam270@gmail.com",
    MAIL_PASSWORD = "",
    MAIL_FROM = "Parwejalam270@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com", # gmail mail connection
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True
)



async def  send_mail(subject: str, recipient: List, message: str):
    message_s = MessageSchema(
        subject= subject,
        recipients= recipient,
        body= message,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message=message_s)

    return {"status": "sent messgae"}