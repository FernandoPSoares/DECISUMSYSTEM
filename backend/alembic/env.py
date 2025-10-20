# backend/alembic/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# --- 1. IMPORTAÇÕES ADICIONAIS ---
# Adiciona o caminho do nosso projeto ao Python Path para garantir que as importações funcionam
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importa o nosso pacote 'models' para que o Alembic "veja" todas as tabelas
from app import models
# Importa a nossa 'Base' a partir do core, que é a fonte da verdade para os metadados
from app.core.database import Base

# Esta é a configuração do Alembic, que lê o alembic.ini
config = context.config

# Interpreta o ficheiro de configuração para o logging do Python.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- 2. DEFINIR O 'target_metadata' ---
# Diz ao Alembic que os metadados de todas as nossas tabelas estão na 'Base'
# que importámos do nosso ficheiro 'database.py'. Como o 'app.models' foi
# importado acima, todas as nossas tabelas já estão "registadas" nesta Base.
target_metadata = Base.metadata

# ... (o resto do ficheiro de configuração, que lida com a conexão, continua igual)
def run_migrations_offline() -> None:
    # ... (sem alterações)
    pass

def run_migrations_online() -> None:
    # ... (sem alterações)
    pass

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

    
