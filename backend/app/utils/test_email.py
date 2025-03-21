from app.core.email import send_email

def test_send_email():
    """Testa o envio de email."""
    try:
        result = send_email(
            email_to="jrdeep@gmail.com",  # Email para onde será enviado o teste
            subject="Teste de Email - Radio Importante",
            template_name="reset_password.html",
            template_data={
                "project_name": "Radio Importante",
                "username": "jrdeep@gmail.com",
                "reset_url": "http://localhost:5173/reset-password?token=teste",
                "valid_hours": 24
            }
        )
        
        if result:
            print("\n✅ Email enviado com sucesso!")
        else:
            print("\n❌ Falha ao enviar email.")
            
    except Exception as e:
        print(f"\n❌ Erro ao enviar email: {e}")

if __name__ == "__main__":
    test_send_email()
