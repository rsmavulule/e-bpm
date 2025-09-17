from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Date, ForeignKey, UniqueConstraint,
    Float
)
from typing import Optional
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base

# --------------------
# Segurança
# --------------------

class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(255))


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Vínculo para administradores de processos
    #process_id: Mapped[int | None] = mapped_column(ForeignKey("process.id"), nullable=True)

    #process: Mapped[Optional["Process"]] = relationship("Process")

    role: Mapped["Role"] = relationship("Role", lazy="joined")

# --------------------
# Hierarquia BPM
# --------------------
class Process(Base):
    __tablename__ = "processes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True) 
    description: Mapped[str | None] = mapped_column(String(255))
    bpmn_xml_json: Mapped[str] = mapped_column(Text)
