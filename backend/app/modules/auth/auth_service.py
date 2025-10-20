# backend/app/modules/auth/auth_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta

from ...core import security
from ..administration.users import users_crud, users_schemas
from . import auth_crud, auth_schemas

class AuthService:
    # ... (método de login, sem alterações) ...
    def login(self, db: Session, username_or_email: str, password: str) -> dict:
        """Lógica de negócio para autenticar um utilizador."""
        user = users_crud.usuario_crud.get_by_username_or_email(db, identifier=username_or_email)
    
        if not user or not security.verify_password(password, user.senha_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nome de utilizador ou senha incorretos")
        
        access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(data={"sub": user.usuario}, expires_delta=access_token_expires)
        
        return {"access_token": access_token, "token_type": "bearer"}

    def request_password_recovery(self, db: Session, email: str) -> None:
        """Lógica de negócio para solicitar a recuperação de senha."""
        user = users_crud.usuario_crud.get_by_username_or_email(db, identifier=email)
        if not user:
            print(f"INFO: Pedido de recuperação de senha para e-mail não registado: {email}")
            return

        token = security.create_password_reset_token()
        expires_at = datetime.utcnow() + timedelta(hours=security.PASSWORD_RESET_TOKEN_EXPIRE_HOURS)
        auth_crud.create_reset_token(db=db, user=user, token=token, expires_at=expires_at)

        reset_link = f"http://localhost:5173/reset-password?token={token}"
        
        print("\n--- SIMULAÇÃO DE ENVIO DE E-MAIL ---")
        print(f"Para: {user.email}")
        print("Assunto: Recuperação de Senha - DecisumSystem")
        print(f"Link: {reset_link}")
        print("-------------------------------------\n")
    
    # --- NOVO MÉTODO ADICIONADO ---
    def reset_password(self, db: Session, reset_request: auth_schemas.PasswordResetRequest) -> None:
        """
        Lógica de negócio para redefinir a senha usando um token.
        """
        # 1. Encontra o token na base de dados
        db_token = auth_crud.get_reset_token(db, token=reset_request.token)

        # 2. Valida o token: existe e não expirou?
        if not db_token or db_token.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O link de recuperação de senha é inválido ou expirou."
            )
        
        # 3. Encontra o utilizador associado ao token
        user = users_crud.usuario_crud.get(db, id=db_token.user_id)
        if not user:
            # Isto é um caso de erro improvável, mas importante para a segurança
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilizador associado ao token não encontrado.")

        # 4. Encripta e atualiza a nova senha
        new_hashed_password = security.get_password_hash(reset_request.nova_senha)
        update_data = users_schemas.UsuarioUpdate(senha_hash=new_hashed_password)
        users_crud.usuario_crud.update(db=db, db_obj=user, obj_in=update_data)

        # 5. Invalida o token para que não possa ser usado novamente
        auth_crud.delete_reset_token(db, token=db_token)


# Cria uma instância do serviço para ser usada pelo router
auth_service = AuthService()

