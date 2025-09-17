from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.models import User
from .security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

ROLE_ORDER = {
    "user": 0,
    "congreg_admin": 1,
    "area_admin": 2,
    "super_admin": 3,
}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    email = payload["sub"]
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado/ativo")
    return user

def require_role(min_role: str):
    def checker(user: User = Depends(get_current_user)) -> User:
        if ROLE_ORDER.get(user.role.name, -1) < ROLE_ORDER.get(min_role, 99):
            raise HTTPException(status_code=403, detail="Acesso negado")
        return user
    return checker