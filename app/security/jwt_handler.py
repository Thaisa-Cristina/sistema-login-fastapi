# Biblioteca usada para trabalhar com datas
from datetime import datetime, timedelta

# Biblioteca usada para criar e verificar tokens JWT
from jose import jwt, JWTError


# --------------------------------------------------
# Chave secreta usada para assinar os tokens
# Em projetos reais isso ficaria em variável de ambiente
# --------------------------------------------------

SECRET_KEY = "chave_super_secreta"

# algoritmo usado para criptografia do token
ALGORITHM = "HS256"


# --------------------------------------------------
# Função responsável por criar um token JWT
# --------------------------------------------------

def criar_token(email):

    # define tempo de expiração do token
    expire = datetime.utcnow() + timedelta(hours=2)

    # dados que serão armazenados dentro do token
    payload = {
        "sub": email,   # subject → identifica o usuário
        "exp": expire   # tempo de expiração
    }

    # gera o token criptografado
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


# --------------------------------------------------
# Função responsável por validar o token JWT
# --------------------------------------------------

def verificar_token(token):

    try:

        # decodifica o token usando a chave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # retorna o email salvo dentro do token
        return payload.get("sub")

    except JWTError:

        # se o token for inválido ou expirado
        return None