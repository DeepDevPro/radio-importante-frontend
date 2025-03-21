from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Nome do projeto
    PROJECT_NAME: str = "Radio Importante API"
    VERSION: str = "1.0.0"
    
    # Configurações do servidor
    HOST: str = os.getenv("API_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # Configurações de segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY", "sua_chave_secreta_muito_segura")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configurações do banco de dados
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_USER: str = os.getenv("DB_USER", "jrdeep")
    DB_PASS: str = os.getenv("DB_PASS", "")
    DB_NAME: str = os.getenv("DB_NAME", "radioimportante")
    
    # URL do banco de dados
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Configurações do CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",  # Frontend em desenvolvimento
        "http://localhost:4173",  # Frontend em preview
        os.getenv("FRONTEND_URL", "")  # URL do frontend em produção
    ]
    
    # Configurações do Digital Ocean Spaces
    DO_SPACES_REGION: str = os.getenv("DO_SPACES_REGION", "")
    DO_SPACES_BUCKET: str = os.getenv("DO_SPACES_BUCKET", "")
    DO_SPACES_KEY: str = os.getenv("DO_SPACES_KEY", "")
    DO_SPACES_SECRET: str = os.getenv("DO_SPACES_SECRET", "")

    class Config:
        case_sensitive = True

# Instância global das configurações
settings = Settings() 