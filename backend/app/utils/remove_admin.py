from sqlalchemy.orm import Session
from app.db.models import User, SessionLocal

def remove_default_admin():
    """Remove o usuário admin padrão do sistema."""
    db = SessionLocal()
    try:
        # Encontrar o usuário admin original
        default_admin = db.query(User).filter(
            User.username == "admin",
            User.email == "admin@radioimportante.com"
        ).first()

        if default_admin:
            print("\n⚠️  Atenção: Você está prestes a remover o usuário admin padrão!")
            print(f"\nUsuário: {default_admin.username}")
            print(f"Email: {default_admin.email}")
            
            # Verificar se existe pelo menos outro admin no sistema
            other_admins = db.query(User).filter(
                User.is_superuser == True,
                User.id != default_admin.id
            ).all()
            
            if not other_admins:
                print("\n❌ Erro: Não é possível remover o único usuário administrador do sistema!")
                print("Crie outro administrador antes de remover este.")
                return
            
            print("\nOutros administradores disponíveis:")
            for admin in other_admins:
                print(f"- {admin.username} ({admin.email})")
            
            confirm = input("\nDigite 'REMOVER' para confirmar a remoção: ")
            
            if confirm == "REMOVER":
                db.delete(default_admin)
                db.commit()
                print("\n✅ Usuário admin padrão removido com sucesso!")
            else:
                print("\n❌ Operação cancelada!")
        else:
            print("\n❌ Usuário admin padrão não encontrado!")
            
    except Exception as e:
        print(f"\n❌ Erro ao remover usuário: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    remove_default_admin()
