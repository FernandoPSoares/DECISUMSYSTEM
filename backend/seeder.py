# backend/seeder.py

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app import models
from app.core.security import get_password_hash
import uuid

# --- DADOS INICIAIS ATUALIZADOS ---
# A estrutura agora inclui o módulo de cada permissão.
ROLES = {
    "admin": "Administrador",
    "operador": "Operador",
}

PERMISSIONS = {
    # Módulo de Administração
    "usuarios:ler":           { "descricao": "Permite listar e ver utilizadores", "module": "administration" },
    "usuarios:criar":         { "descricao": "Permite criar novos utilizadores", "module": "administration" },
    "usuarios:editar":        { "descricao": "Permite editar os dados de utilizadores", "module": "administration" },
    "usuarios:ativar_desativar": { "descricao": "Permite ativar ou desativar utilizadores", "module": "administration" },
    "usuarios:definir_senha": { "descricao": "Permite que um admin defina a senha de um utilizador", "module": "administration" },
    
    "roles:ler":              { "descricao": "Permite ver funções e as suas permissões", "module": "administration" },
    "roles:criar":            { "descricao": "Permite criar novas funções", "module": "administration" },
    "roles:editar":           { "descricao": "Permite editar o nome de uma função", "module": "administration" },
    "roles:editar_permissoes": { "descricao": "Permite atribuir/remover permissões de uma função", "module": "administration" },
    "roles:ativar_desativar": { "descricao": "Permite ativar ou desativar funções", "module": "administration" },

    # Módulo de Inventário
    "inventory:admin":      { "descricao": "Permite acesso total ao módulo de inventário", "module": "inventory" },
    "inventory:read":       { "descricao": "Permite ler dados do módulo de inventário", "module": "inventory" },
}

ADMIN_USER = {
    "id": str(uuid.uuid4()),
    "usuario": "admin.sistema",
    "email": "admin@email.com",
    "senha": "senha123",
    "role_id": "admin",
}

def seed_initial_data(db: Session):
    print("A iniciar a semeação da base de dados...")

    # --- LÓGICA DE SEMEAÇÃO ATUALIZADA ---
    # O loop agora extrai os dados completos da permissão.
    for perm_id, perm_data in PERMISSIONS.items():
        db_perm = db.query(models.Permission).filter(models.Permission.id == perm_id).first()
        if not db_perm:
            db.add(models.Permission(
                id=perm_id, 
                descricao=perm_data["descricao"],
                module=perm_data["module"]  # <-- Passa o valor do módulo para o modelo
            ))
            print(f"  - Permissão '{perm_id}' criada.")
    db.commit()

    # O resto da lógica continua igual
    for role_id, role_name in ROLES.items():
        db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
        if not db_role:
            db.add(models.Role(id=role_id, nome=role_name, is_system_role=(role_id == "admin")))
            print(f"  - Função '{role_id}' criada.")
    db.commit()

    admin_role = db.query(models.Role).filter(models.Role.id == "admin").first()
    if admin_role:
        all_perms = db.query(models.Permission).all()
        admin_role.permissions = all_perms
        db.commit()
        print("  - Todas as permissões foram atribuídas à função 'admin'.")

    admin_user_obj = db.query(models.Usuario).filter(models.Usuario.usuario == ADMIN_USER["usuario"]).first()
    if not admin_user_obj:
        hashed_password = get_password_hash(ADMIN_USER["senha"])
        new_admin = models.Usuario(
            id=ADMIN_USER["id"],
            usuario=ADMIN_USER["usuario"],
            email=ADMIN_USER["email"],
            senha_hash=hashed_password,
            role_id=ADMIN_USER["role_id"],
            is_active=True
        )
        db.add(new_admin)
        db.commit()
        print(f"  - Utilizador administrador '{ADMIN_USER['usuario']}' criado com sucesso.")
        print(f"    -> Senha: '{ADMIN_USER['senha']}'")

    print("\nSemeação da base de dados concluída!")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        models.Base.metadata.create_all(bind=engine)
        seed_initial_data(db)
    finally:
        db.close()