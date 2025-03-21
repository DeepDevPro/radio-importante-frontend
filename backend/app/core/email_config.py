from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

conf = ConnectionConfig(
	MAIL_USERNAME=os.getenv("SMTO_USER"),
	MAIL_PASSWORD=os.getenv("SMTP_PASSWORD"),
	MAIL_FROM=os.getenv("SMTP_USER"),
	MAIL_PORT=587,
	MAIL_SERVER="smtp.gmail.com",
	MAIL_STARTTLS=True,
	MAIL_SSL_TLS=False,
	USE_CREDENTIALS=True,
	VALIDATE_CERTS=True
)

fastmail = FastMail(conf)
