# Biblioteca usada para criar e verificar hash de senha
# Passlib é uma biblioteca muito usada para segurança em aplicações Python
from passlib.context import CryptContext


# Cria um contexto de criptografia para trabalhar com senhas
# bcrypt é um dos algoritmos mais seguros para armazenar senhas
pwd_context = CryptContext(
    schemes=["bcrypt"],   # algoritmo de hash usado
    deprecated="auto"     # permite atualização automática do algoritmo no futuro
)


def gerar_hash(senha):
    """
    Função responsável por transformar a senha em hash.

    A senha nunca deve ser salva diretamente no banco.
    Em vez disso salvamos o hash da senha para garantir segurança.
    """

    # cria hash seguro da senha
    return pwd_context.hash(senha)


def verificar_senha(senha, senha_hash):
    """
    Função responsável por verificar se a senha digitada pelo usuário
    corresponde ao hash armazenado no banco de dados.
    """

    # compara senha digitada com hash salvo
    return pwd_context.verify(senha, senha_hash)