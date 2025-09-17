from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
#from app.db import models, schemas
from ..db.database import get_db
from ..db.models import User, Process
from ..db.schemas import ProcessCreate, ProcessOut, ProcessUpdate
from ..security.deps import get_current_user, require_role
from ..utils.permissions import check_scope_permission

router = APIRouter(prefix="/processes", tags=["Processes"])

@router.post("/", response_model=ProcessOut, dependencies=[Depends(require_role("super_admin"))])
def create_process(payload: ProcessCreate, db: Session = Depends(get_db)):
    if db.query(Process).filter(Process.name == payload.name).first():
        raise HTTPException(status_code=400, detail="Processo já existe")
    process = Process(**payload.model_dump())
    db.add(process)
    db.commit()
    db.refresh(process)
    return process

@router.get("/", response_model=list[ProcessOut])
def list_processes(db: Session = Depends(get_db)):
    return db.query(Process).all()

@router.put("/{process_id}", response_model=ProcessOut, dependencies=[Depends(require_role("super_admin"))])
def update_process(
    process_id: int,
    payload: ProcessUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    process = db.get(Process, process_id)
    if not process:
        raise HTTPException(status_code=404, detail="Processo não encontrada")

    check_scope_permission(entity=process, user=current_user)

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(process, key, value)

    db.add(process)
    db.commit()
    db.refresh(process)
    return process