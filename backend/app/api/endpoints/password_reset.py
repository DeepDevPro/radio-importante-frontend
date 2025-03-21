from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt

from app.core.security import create_access_token, get_password_hash
from app.core.config import settings
from app.core.email import send_password_reset_email
from app.db.models import User, get_db
from pydantic import BaseModel, EmailStr

router = APIRouter()

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str

def generate_password_reset_token(email: str) -> str:
    """Gera um token temporário para reset de senha."""
    expires_delta = timedelta(hours=24)
    return create_access_token(
        data={"sub": email, "type": "password_reset"},
        expires_delta=expires_delta
    )

def verify_password_reset_token(token: str) -> Optional[str]:
    """Verifica o token de reset de senha e retorna o email se válido."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "password_reset":
            return None
        return payload.get("sub")
    except:
        return None

@router.post("/request-password-reset", status_code=status.HTTP_200_OK)
async def request_password_reset(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """Solicita reset de senha enviando email com token."""
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        # Não revelamos se o email existe ou não por segurança
        return {"message": "Se o email existir, você receberá as instruções de recuperação."}
    
    token = generate_password_reset_token(request.email)
    send_password_reset_email(email_to=request.email, token=token)
    return {"message": "Email de recuperação enviado com sucesso!"}

@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
):
    """Reset a senha usando o token recebido por email."""
    email = verify_password_reset_token(reset_data.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido ou expirado"
        )
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    user.hashed_password = get_password_hash(reset_data.new_password)
    db.commit()
    
    return {"message": "Senha alterada com sucesso!"}
