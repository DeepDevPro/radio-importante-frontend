from app.db.models import User, SessionLocal

def list_users():
    """Lista todos os usuários do sistema."""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        
        if not users:
            print("\n❌ Nenhum usuário encontrado no sistema!")
            return
            
        print("\n=== Usuários do Sistema ===\n")
        for user in users:
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Admin: {'Sim' if user.is_superuser else 'Não'}")
            print(f"Ativo: {'Sim' if user.is_active else 'Não'}")
            print("-" * 30)
            
    except Exception as e:
        print(f"\n❌ Erro ao listar usuários: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    list_users()
