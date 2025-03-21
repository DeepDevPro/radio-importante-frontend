from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.core.password_reset import create_password_reset_token, verify_password_reset_token
from app.core.config import settings

from app.core.security import (
    verify_password,
    create_access_token,
    get_password_hash
)
from app.core.password_reset import create_password_reset_token
from app.core.email import send_password_reset_email
from app.db.models import User, get_db
from app.api.schemas import Token, User as UserSchema, UserCreate
from app.api.deps import get_current_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class PasswordResetRequest(BaseModel):
    email: EmailStr

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserSchema)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user

@router.post("/request-password-reset")
async def request_password_reset(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    # Verificar se o usuário existe
    user = db.query(User).filter(User.email == request.email).first()
    
    # Por segurança, não revelamos se o email existe ou não
    if user:
        # Criar o token de recuperação
        token = create_password_reset_token(user.email)

        # Enviar o email de recuperação
        success = send_password_reset_email(user.email, token)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao enviar o email de recuperação"
            )
        
    return {
        "message": "Se o email existir em nossa base, você receberá as instruções para redefinir sua senha."
    }

class PasswordReset(BaseModel):
    token: str
    new_password: str

@router.post("/reset-password")
async def reset_password(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
):
    # Verificar o token
    email = verify_password_reset_token(reset_data.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Token inválido ou expirado"
        )
    
    # Buscar o usuário
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usiário não encontrado"
        )
    
    # Atualizar a senha
    user.hashed_password = get_password_hash(reset_data.new_password)
    db.commit()

    return {"message": "Senha atualizada com sucesso"}

