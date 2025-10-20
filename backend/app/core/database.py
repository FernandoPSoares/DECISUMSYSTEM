from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://meu_usuario:minha_senha_super_segura@localhost:5432/meu_banco"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Esta é a nossa única e verdadeira BASE para os modelos
Base = declarative_base()

