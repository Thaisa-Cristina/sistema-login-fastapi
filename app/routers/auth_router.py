from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database.database import SessionLocal
from app.models.user_model import Usuario
from app.services.auth_service import gerar_hash, verificar_senha
from app.security.jwt_handler import criar_token
from app.utils.email_validator import validar_email


templates = Jinja2Templates(directory="templates")


router = APIRouter()

# cria sessão com banco
session = SessionLocal()


@router.post("/login")
def login(email: str = Form(...), senha: str = Form(...)):
    """
    Autentica usuário no sistema.
    """

    # busca usuário pelo email
    usuario = session.query(Usuario).filter_by(email=email).first()

    if not usuario:
        return {"erro": "Usuário não encontrado"}

    # verifica senha usando bcrypt
    if verificar_senha(senha, usuario.senha):

        # cria token JWT
        token = criar_token(usuario.email)

        # cria resposta redirecionando para dashboard
        response = RedirectResponse("/dashboard", status_code=303)

        # salva token no cookie do navegador
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True
        )

        return response

    return {"erro": "Senha incorreta"}


@router.post("/cadastro")
def cadastrar(nome: str = Form(...), email: str = Form(...), senha: str = Form(...)):
    """
    Cria novo usuário no sistema.
    """

    # valida formato do email
    if not validar_email(email):
        return {"erro": "Email inválido"}

    # verifica se email já existe
    usuario_existente = session.query(Usuario).filter_by(email=email).first()

    if usuario_existente:
        return {"erro": "Email já cadastrado"}

    # gera hash da senha
    senha_hash = gerar_hash(senha)

    # cria objeto usuário
    usuario = Usuario(
        nome=nome,
        email=email,
        senha=senha_hash
    )

    # salva no banco
    session.add(usuario)
    session.commit()

    # redireciona para login
    return RedirectResponse("/", status_code=303)


@router.get("/logout")
def logout():

    response = RedirectResponse("/", status_code=302)

    # remove o cookie do token
    response.delete_cookie("access_token")

    return response


@router.get("/deletar/{usuario_id}")
def deletar_usuario(usuario_id: int):

    session = SessionLocal()

    usuario = session.query(Usuario).filter_by(id=usuario_id).first()

    if usuario:
        session.delete(usuario)
        session.commit()

    return RedirectResponse("/dashboard", status_code=303)

# Página de edição
@router.get("/editar/{user_id}")
def editar_usuario_page(request: Request, user_id: int):

    db = SessionLocal()

    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()

    return templates.TemplateResponse(
        request,
        "editar.html",
        {
            "usuario": usuario
        }
    )


# Salvar edição
@router.post("/editar/{user_id}")
def editar_usuario(
    user_id: int,
    nome: str = Form(...),
    email: str = Form(...)
):

    db = SessionLocal()

    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()

    usuario.nome = nome
    usuario.email = email

    db.commit()

    return RedirectResponse("/dashboard", status_code=303)