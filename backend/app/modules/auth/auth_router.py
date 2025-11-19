# backend/app/modules/auth/auth_router.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import auth_schemas, auth_service
from ...core.dependencies import get_db

router = APIRouter(
    tags=["Autenticação"]
)

@router.post("/login/token", response_model=auth_schemas.Token)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Autentica um utilizador e devolve um token de acesso JWT.
    """
    return auth_service.auth_service.login(
        db, username_or_email=form_data.username, password=form_data.password
    )

# --- NOVO ENDPOINT DE RECUPERAÇÃO DE SENHA ---
@router.post("/password-recovery", status_code=status.HTTP_202_ACCEPTED)
def request_password_recovery_endpoint(
    recovery_request: auth_schemas.PasswordRecoveryRequest,
    db: Session = Depends(get_db)
):
    """
    Inicia o fluxo de recuperação de senha para um e-mail.
    Devolve sempre 202 Accepted para não revelar se o e-mail existe na base de dados.
    """
    auth_service.auth_service.request_password_recovery(db, email=recovery_request.email)
    return Response(status_code=status.HTTP_202_ACCEPTED)

@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
def reset_password_endpoint(
    reset_request: auth_schemas.PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """

    Valida um token de recuperação e define uma nova senha para o utilizador.
    """
    auth_service.auth_service.reset_password(db, reset_request=reset_request)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
