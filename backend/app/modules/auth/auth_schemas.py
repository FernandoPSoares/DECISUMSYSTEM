# backend/app/modules/auth/auth_schemas.py

from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    """
    Representa o "contrato" de resposta do endpoint de login.
    """
    access_token: str
    token_type: str
    
class PasswordRecoveryRequest(BaseModel):
    """Schema para o corpo do pedido de recuperação de senha."""
    email: EmailStr

class PasswordResetRequest(BaseModel):
    """Schema para o corpo do pedido de redefinição de senha."""
    token: str
    nova_senha: str