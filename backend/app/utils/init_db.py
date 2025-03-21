from app.db.models import SessionLocal, User
from app.core.security import get_password_hash

def init_db():
    """
    Inicializa o banco de dados com um usuário administrador padrão.
    Este script deve ser executado apenas uma vez, quando o banco de dados for criado.
    """
    db = SessionLocal()
    try:
        # Verificar se já existe um superusuário
        admin = db.query(User).filter(User.is_superuser == True).first()
        if not admin:
            # Criar usuário admin
            admin_user = User(
                email="admin@radioimportante.com",
                username="admin",
                hashed_password=get_password_hash("admin123"),  # Em produção, usar senha mais segura
                is_active=True,
                is_superuser=True
            )
            db.add(admin_user)
            db.commit()
            print("Usuário admin criado com sucesso!")
            print("Email: admin@radioimportante.com")
            print("Senha: admin123")
        else:
            print("Usuário admin já existe!")
            
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Iniciando configuração inicial do banco de dados...")
    init_db()
