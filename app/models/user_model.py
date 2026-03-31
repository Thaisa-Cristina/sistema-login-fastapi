from sqlalchemy import Column, Integer, String
from app.database.database import Base


class Usuario(Base):
    """
    Modelo da tabela de usuários.

    Representa um usuário do sistema de login.
    Cada atributo da classe corresponde a uma coluna no banco de dados.
    """

    # Nome da tabela no banco de dados
    __tablename__ = "usuarios"

    # ID único do usuário (chave primária)
    # O banco gera automaticamente
    id = Column(Integer, primary_key=True)

    # Nome do usuário
    # nullable=False significa que o campo é obrigatório
    nome = Column(String, nullable=False)

    # Email do usuário
    # unique=True impede emails duplicados no banco
    # nullable=False torna o campo obrigatório
    email = Column(String, unique=True, nullable=False)

    # Senha do usuário
    # Armazena o hash da senha (não a senha em texto)
    senha = Column(String, nullable=False)