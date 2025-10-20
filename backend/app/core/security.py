# backend/app/core/security.py

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
import secrets

class TokenData(BaseModel):
    """
    Representa a estrutura de dados interna do payload de um token JWT.
    --- MUDANÇA CRÍTICA AQUI ---
    O campo agora é 'sub', para corresponder ao padrão JWT.
    """
    sub: Optional[str] = None

# --- Configuração de Segurança ---
SECRET_KEY = "uma-chave-secreta-muito-dificil-de-adivinhar-012345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

PASSWORD_RESET_TOKEN_EXPIRE_HOURS = 1 # O token de recuperação irá expirar em 1 hora

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Funções de Senha ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# --- Funções de Token JWT ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_username_from_token(token: str) -> Optional[str]:
    """Descodifica um token JWT e retorna o nome de utilizador (sub)."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
        # --- MUDANÇA CRÍTICA AQUI ---
        # Agora devolvemos o campo 'sub'.
        return token_data.sub
    except (JWTError, ValidationError):
        return None

# --- 2. NOVA FUNÇÃO PARA TOKENS DE RECUPERAÇÃO ---
def create_password_reset_token() -> str:
    """Gera um token aleatório e seguro para a recuperação de senha."""
    return secrets.token_urlsafe(32)