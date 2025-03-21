import os
from typing import List
from emails.template import JinjaTemplate
import emails
from jinja2 import Environment, select_autoescape, PackageLoader
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações de email
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAILS_FROM_EMAIL = SMTP_USER
EMAILS_FROM_NAME = "Radio Importante"

# Configuração do Jinja2 para templates
env = Environment(
    loader=PackageLoader("app", "templates"),
    autoescape=select_autoescape(['html', 'xml'])
)

def send_email(
    email_to: str,
    subject: str,
    template_name: str,
    template_data: dict = None
) -> bool:
    """
    Envia um email usando um template.
    """
    if template_data is None:
        template_data = {}

    # Carregar o template
    template = env.get_template(f"email/{template_name}")
    html_content = template.render(**template_data)

    # Criar o email
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(EMAILS_FROM_NAME, EMAILS_FROM_EMAIL)
    )

    # Enviar o email
    response = message.send(
        to=email_to,
        smtp={
            "host": SMTP_HOST,
            "port": SMTP_PORT,
            "user": SMTP_USER,
            "password": SMTP_PASSWORD,
            "tls": True,
        }
    )

    return response.status_code == 250

def send_password_reset_email(email_to: str, token: str) -> bool:
    """
    Envia email de recuperação de senha.
    """
    project_name = "Radio Importante"
    subject = f"{project_name} - Recuperação de Senha"
    
    # URL de recuperação (ajuste conforme seu frontend)
    reset_url = f"http://localhost:5173/reset-password?token={token}"
    
    return send_email(
        email_to=email_to,
        subject=subject,
        template_name="reset_password.html",
        template_data={
            "project_name": project_name,
            "username": email_to,
            "reset_url": reset_url,
            "valid_hours": 24
        }
    )
