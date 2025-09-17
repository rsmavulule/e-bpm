from contextlib import asynccontextmanager
from fastapi import FastAPI
from .db.database import Base, engine
from .auth.routes import router as auth_router
from .api.processes import router as processes_router
from .api.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Executa tarefas na inicialização e no encerramento do servidor.
    """
    # A criação de tabelas agora é gerenciada pelo Alembic.
    print("INFO:     Servidor iniciado.")
    yield
    print("INFO:     Servidor encerrado.")

app = FastAPI(title="BPM Backend", lifespan=lifespan)

# Routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(processes_router)

@app.get("/")
def root():
    return {"msg": "BPM Backend up"}