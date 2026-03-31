"""
Arquivo responsável pela configuração do banco de dados.

Aqui definimos:
- conexão com o banco SQLite
- criação da engine do SQLAlchemy
- criação da sessão de acesso ao banco
- classe Base usada pelos modelos
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# URL de conexão com banco SQLite
# O arquivo usuarios.db será criado automaticamente
DATABASE_URL = "sqlite:///usuarios.db"


# Engine é responsável por conectar Python ao banco de dados
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # necessário para SQLite
)


# SessionLocal cria sessões para interagir com o banco
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base será herdada por todos os modelos do sistema
# Exemplo: class Usuario(Base)
Base = declarative_base()