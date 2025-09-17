from fastapi import Depends, HTTPException, status
from typing import Union

from ..db import models
from ..security.deps import get_current_user


def check_scope_permission(
        #entity: Union[models.Area, models.Congregation, models.Department],
    entity: Union[models.Process],
    user: models.User,
) -> None:
    """
    Função que verifica se um usuário tem permissão de escopo sobre uma entidade.
    Levanta uma exceção HTTPException 403 se o acesso for negado.

    - `super_admin` tem acesso a tudo.
    - `area_admin` pode acessar sua própria área e as congregações/departamentos dentro dela.
    - `congreg_admin` só pode acessar sua própria congregação e os departamentos dentro dela.

    Args:
        entity: A instância do modelo SQLAlchemy (Process, ..) a ser verificada.
        user: O usuário autenticado.
    """
    if user.role.name == "super_admin":
        return

    """
    if user.role.name == "area_admin":
        if isinstance(entity, models.Area) and entity.id == user.area_id:
            return
        if isinstance(entity, models.Congregation) and entity.area_id == user.area_id:
            return
        if isinstance(entity, models.Department) and entity.congregation.area_id == user.area_id:
            return

    if user.role.name == "congreg_admin":
        if isinstance(entity, models.Congregation) and entity.id == user.congregation_id:
            return
        if isinstance(entity, models.Department) and entity.congregation_id == user.congregation_id:
            return
    """

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado a este recurso.")