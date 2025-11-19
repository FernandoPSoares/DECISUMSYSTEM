# backend/app/modules/auth/auth_crud.py

from sqlalchemy.orm import Session
from datetime import datetime

from ... import models

def create_reset_token(db: Session, *, user: models.Usuario, token: str, expires_at: datetime) -> models.PasswordResetToken:
    """Cria e guarda um novo token de recuperação na base de dados."""
    db_token = models.PasswordResetToken(
        token=token,
        user_id=user.id,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def get_reset_token(db: Session, *, token: str) -> models.PasswordResetToken:
    """Busca um token de recuperação na base de dados."""
    return db.query(models.PasswordResetToken).filter(models.PasswordResetToken.token == token).first()

def delete_reset_token(db: Session, *, token: models.PasswordResetToken) -> None:
    """Apaga um token de recuperação da base de dados."""
    db.delete(token)
    db.commit()