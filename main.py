# Importa o framework FastAPI
from fastapi import FastAPI, Request

# Permite servir arquivos estáticos (CSS, JS, imagens)
from fastapi.staticfiles import StaticFiles

# Sistema de templates HTML usado pelo FastAPI
from fastapi.templating import Jinja2Templates

# Permite redirecionar o usuário para outra rota
from fastapi.responses import RedirectResponse


# Importa a conexão com o banco
from app.database.database import engine, SessionLocal

# Importa o modelo de usuário
from app.models.user_model import Base, Usuario

# Importa as rotas de autenticação (login e cadastro)
from app.routers.auth_router import router

# Função que verifica o token JWT
from app.security.jwt_handler import verificar_token


# --------------------------------------------------
# Criação da aplicação FastAPI
# --------------------------------------------------

app = FastAPI()


# --------------------------------------------------
# Cria as tabelas no banco automaticamente
# caso ainda não existam
# --------------------------------------------------

Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# Registra as rotas do sistema de autenticação
# --------------------------------------------------

app.include_router(router)


# --------------------------------------------------
# Configuração da pasta de arquivos estáticos
# Exemplo: CSS, JavaScript, imagens
# --------------------------------------------------

app.mount("/static", StaticFiles(directory="static"), name="static")


# --------------------------------------------------
# Configuração da pasta de templates HTML
# --------------------------------------------------

templates = Jinja2Templates(directory="templates")


# --------------------------------------------------
# Página inicial (Login)
# --------------------------------------------------

@app.get("/")
def login_page(request: Request):

    # Renderiza o template login.html
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


# --------------------------------------------------
# Página de cadastro de usuário
# --------------------------------------------------

@app.get("/cadastro")
def cadastro_page(request: Request):

    return templates.TemplateResponse(
        "cadastro.html",
        {"request": request}
    )


# --------------------------------------------------
# Dashboard do sistema
# Página acessível apenas se o usuário estiver logado
# --------------------------------------------------

@app.get("/dashboard")
def dashboard_page(request: Request):

    session = SessionLocal()

    token = request.cookies.get("access_token")

    if not token:
        return RedirectResponse("/")

    email = verificar_token(token)

    if not email:
        return RedirectResponse("/")

    usuario = session.query(Usuario).filter_by(email=email).first()

    # lista de usuários do banco
    usuarios = session.query(Usuario).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "usuario": usuario,
            "usuarios": usuarios
        }
    )