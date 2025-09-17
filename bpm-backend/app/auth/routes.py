from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.models import User, Role
from ..db.schemas import UserCreate, UserOut, Token
from ..security.security import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Validações de escopo
    role = db.get(Role, payload.role_id)
    if not role:
        raise HTTPException(status_code=400, detail="Role inválido.")

    #if role.name == "area_admin" and (not payload.area_id or not db.get(Area, payload.area_id)):
    #    raise HTTPException(status_code=400, detail="area_admin precisa de um area_id válido.")
    
    #if role.name == "congreg_admin" and (not payload.congregation_id or not db.get(Congregation, payload.congregation_id)):
    #    raise HTTPException(status_code=400, detail="congreg_admin precisa de um congregation_id válido.")

    user_data = payload.model_dump()
    user_data["hashed_password"] = hash_password(user_data.pop("password"))
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}