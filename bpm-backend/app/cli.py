import uvicorn
from app.core.config import settings


def start_server():
    """
    Inicia o servidor Uvicorn.
    As configurações de host, porta e modo de recarga são lidas do
    objeto de configurações.
    """
    uvicorn.run(
        "app.main:app",
        reload=settings.app_debug,
        host=settings.app_host,
        port=settings.app_port,
    )
