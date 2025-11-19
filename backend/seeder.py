# backend/seeder.py

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app import models
from app.core.security import get_password_hash
import uuid

# --- DADOS INICIAIS ATUALIZADOS ---
ROLES = {
    "admin": "Administrador",
    "operador": "Operador",
}

PERMISSIONS = {
    # --- MÓDULO: ADMINISTRAÇÃO ---
    "usuarios:ler":             { "descricao": "Permite listar e ver utilizadores", "module": "administration" },
    "usuarios:criar":           { "descricao": "Permite criar novos utilizadores", "module": "administration" },
    "usuarios:editar":          { "descricao": "Permite editar os dados de utilizadores", "module": "administration" },
    "usuarios:ativar_desativar": { "descricao": "Permite ativar ou desativar utilizadores", "module": "administration" },
    "usuarios:definir_senha":   { "descricao": "Permite que um admin defina a senha de um utilizador", "module": "administration" },
    
    "roles:ler":               { "descricao": "Permite ver funções e as suas permissões", "module": "administration" },
    "roles:criar":             { "descricao": "Permite criar novas funções", "module": "administration" },
    "roles:editar":            { "descricao": "Permite editar o nome de uma função", "module": "administration" },
    "roles:editar_permissoes": { "descricao": "Permite atribuir/remover permissões de uma função", "module": "administration" },
    "roles:ativar_desativar":  { "descricao": "Permite ativar ou desativar funções", "module": "administration" },

    # --- MÓDULO: INVENTÁRIO ---
    "inventory:admin":       { "descricao": "Permite acesso total ao módulo de inventário", "module": "inventory" },
    "inventory:read":        { "descricao": "Permite ler dados do módulo de inventário", "module": "inventory" },
    
    # Locais (Corrige o erro 403)
    "locais:ler":            { "descricao": "Ver locais", "module": "inventory" },
    "locais:criar":          { "descricao": "Criar locais", "module": "inventory" },
    "locais:editar":         { "descricao": "Editar locais", "module": "inventory" },
    "locais:ativar_desativar": { "descricao": "Ativar/Desativar locais", "module": "inventory" },

    # --- MÓDULO: MANUTENÇÃO (CMMS) - NOVAS PERMISSÕES ---
    
    # Fabricantes
    "manufacturers:ler":      { "descricao": "Ver lista de fabricantes", "module": "maintenance" },
    "manufacturers:criar":    { "descricao": "Criar fabricantes", "module": "maintenance" },
    "manufacturers:editar":   { "descricao": "Editar fabricantes", "module": "maintenance" },
    "manufacturers:eliminar": { "descricao": "Eliminar/Desativar fabricantes", "module": "maintenance" },

    # Equipas
    "teams:ler":      { "descricao": "Ver equipas de manutenção", "module": "maintenance" },
    "teams:criar":    { "descricao": "Criar equipas", "module": "maintenance" },
    "teams:editar":   { "descricao": "Editar equipas", "module": "maintenance" },
    "teams:eliminar": { "descricao": "Eliminar equipas", "module": "maintenance" },

    # Técnicos
    "technicians:ler":      { "descricao": "Ver técnicos", "module": "maintenance" },
    "technicians:criar":    { "descricao": "Criar técnicos", "module": "maintenance" },
    "technicians:editar":   { "descricao": "Editar técnicos", "module": "maintenance" },
    "technicians:eliminar": { "descricao": "Eliminar técnicos", "module": "maintenance" },

    # Ativos (Assets)
    "assets:ler":      { "descricao": "Ver ativos", "module": "maintenance" },
    "assets:criar":    { "descricao": "Criar ativos", "module": "maintenance" },
    "assets:editar":   { "descricao": "Editar ativos", "module": "maintenance" },
    "assets:eliminar": { "descricao": "Eliminar ativos", "module": "maintenance" },

    # Ordens de Serviço (Work Orders)
    "work_orders:ler":      { "descricao": "Ver ordens de serviço", "module": "maintenance" },
    "work_orders:criar":    { "descricao": "Criar ordens de serviço", "module": "maintenance" },
    "work_orders:editar":   { "descricao": "Editar ordens de serviço (status, atribuição)", "module": "maintenance" },
    "work_orders:eliminar": { "descricao": "Eliminar ordens de serviço (apenas rascunhos)", "module": "maintenance" },
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

    # 1. Criar Permissões
    for perm_id, perm_data in PERMISSIONS.items():
        db_perm = db.query(models.Permission).filter(models.Permission.id == perm_id).first()
        if not db_perm:
            db.add(models.Permission(
                id=perm_id, 
                descricao=perm_data["descricao"],
                module=perm_data["module"]
            ))
            print(f"  - Permissão '{perm_id}' criada.")
    db.commit()

    # 2. Criar Funções (Roles)
    for role_id, role_name in ROLES.items():
        db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
        if not db_role:
            db.add(models.Role(id=role_id, nome=role_name, is_system_role=(role_id == "admin")))
            print(f"  - Função '{role_id}' criada.")
    db.commit()

    # 3. Atribuir TODAS as permissões ao Admin
    admin_role = db.query(models.Role).filter(models.Role.id == "admin").first()
    if admin_role:
        all_perms = db.query(models.Permission).all()
        # Isto garante que, mesmo que adicione novas permissões depois,
        # ao rodar o seeder, o admin ganha acesso a elas.
        admin_role.permissions = all_perms
        db.commit()
        print("  - Todas as permissões foram atribuídas à função 'admin'.")

    # 4. Criar Utilizador Admin (se não existir)
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
    else:
        print(f"  - Utilizador '{ADMIN_USER['usuario']}' já existe.")

    print("\nSemeação da base de dados concluída!")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        # Garante que as tabelas existem antes de semear
        models.Base.metadata.create_all(bind=engine)
        seed_initial_data(db)
    finally:
        db.close()