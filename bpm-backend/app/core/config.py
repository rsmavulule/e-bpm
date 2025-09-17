from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Gerencia as configurações da aplicação lendo de variáveis de ambiente
    e de arquivos .env.
    """
    # O pydantic-settings irá ler automaticamente de um arquivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Configurações da aplicação com valores padrão
    app_name: str = "BPM Backend"
    app_env: str = "dev"
    app_debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # Configurações de segurança com valores padrão
    jwt_secret: str = "change-me"
    jwt_alg: str = "HS256"
    jwt_expire_min: int = 60

    # Configuração obrigatória: deve estar presente no ambiente ou no .env
    database_url: str

settings = Settings()