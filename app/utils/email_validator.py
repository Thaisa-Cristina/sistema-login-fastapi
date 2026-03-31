# Biblioteca usada para validar formato de email
# email-validator verifica se o email segue o padrão correto
from email_validator import validate_email, EmailNotValidError


def validar_email(email):
    """
    Função responsável por verificar se o email informado
    possui um formato válido.

    Exemplo de email válido:
    usuario@email.com

    Se o email estiver correto → retorna True
    Se estiver inválido → retorna False
    """

    try:
        # Tenta validar o formato do email
        validate_email(email)

        # Se não ocorrer erro, o email é válido
        return True

    except EmailNotValidError:
        # Caso o formato esteja errado, retorna False
        return False