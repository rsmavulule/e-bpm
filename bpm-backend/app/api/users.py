from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.models import User
from ..db.schemas import UserOut, UserUpdate
from ..security.deps import get_current_user, require_role
from ..security.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user

@router.get("/", response_model=list[UserOut], dependencies=[Depends(require_role("super_admin"))])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.put("/{user_id}", response_model=UserOut, dependencies=[Depends(require_role("super_admin"))])
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db)
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    update_data = payload.model_dump(exclude_unset=True)

    if "password" in update_data:
        user.hashed_password = hash_password(update_data["password"])
        del update_data["password"]

    for key, value in update_data.items():
        setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user