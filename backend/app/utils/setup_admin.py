import getpass
import re
from sqlalchemy.orm import Session
from app.db.models import User, SessionLocal
from app.core.security import get_password_hash

def validate_email(email: str) -> bool:
    """Validar formato do email."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> tuple[bool, str]:
    """
    Validar força da senha.
    Retorna (válido, mensagem)
    """
    if len(password) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres"
    if not any(c.isupper() for c in password):
        return False, "A senha deve conter pelo menos uma letra maiúscula"
    if not any(c.islower() for c in password):
        return False, "A senha deve conter pelo menos uma letra minúscula"
    if not any(c.isdigit() for c in password):
        return False, "A senha deve conter pelo menos um número"
    if not any(c in "!@#$%^&*(),.?\":{}|<>" for c in password):
        return False, "A senha deve conter pelo menos um caractere especial"
    return True, "Senha válida"

def setup_admin():
    """Configurar usuário administrador de forma interativa e segura."""
    db = SessionLocal()
    
    try:
        # Verificar se já existe um superusuário
        if db.query(User).filter(User.is_superuser == True).first():
            print("\n⚠️  Atenção: Já existe um usuário administrador!")
            if input("\nDeseja criar outro admin? (s/N): ").lower() != 's':
                return
        
        print("\n=== Configuração do Administrador ===\n")
        
        # Coletar email
        while True:
            email = input("Email do administrador: ").strip()
            if validate_email(email):
                break
            print("❌ Email inválido! Por favor, use um formato válido.")
        
        # Coletar username
        while True:
            username = input("Nome de usuário: ").strip()
            if len(username) >= 3:
                break
            print("❌ Nome de usuário deve ter pelo menos 3 caracteres!")
        
        # Coletar e validar senha
        while True:
            password = getpass.getpass("Senha: ")
            valid, message = validate_password(password)
            if not valid:
                print(f"❌ {message}")
                continue
            
            confirm_password = getpass.getpass("Confirme a senha: ")
            if password == confirm_password:
                break
            print("❌ As senhas não coincidem!")
        
        # Criar usuário admin
        admin_user = User(
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            is_active=True,
            is_superuser=True
        )
        
        db.add(admin_user)
        db.commit()
        
        print("\n✅ Administrador criado com sucesso!")
        print(f"\nUsuário: {username}")
        print(f"Email: {email}")
        print("\nVocê já pode fazer login no sistema.")
        
    except Exception as e:
        print(f"\n❌ Erro ao criar administrador: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    setup_admin()
