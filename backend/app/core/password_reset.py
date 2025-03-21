from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def create_password_reset_token(email:str) -> str:
	"""
	Cria um token para recuperação de senha
	"""
	# Define a expiração do token em 30 minutos
	expire = datetime.utcnow() + timedelta(minutes=30)

	# Cria o payload do token
	to_encode = {
		"exp": expire,
		"sub": email,
		"type": "password_reset"
	}

	# Gera o token
	encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
	return encoded_jwt

def verify_password_reset_token(token: str) -> str:
	"""
	Verifica o token de recuperaçnao de senha e retorna o email
	"""
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
		if payload.get("type") != "password_reset":
			return None
		return payload.get("sub")
	except:
		return None

