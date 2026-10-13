from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.dependencies import get_current_user
from app.core.permissions import Role, require_roles
from app.models.user import User

router = APIRouter()


def _require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    return require_roles(Role.ADMIN, Role.SUPER_ADMIN)(current_user)


ROLES_DATA = [
    {"id": 1, "name": "super_admin", "description": "Super Administrator with full access", "status": True, "permissions": []},
    {"id": 2, "name": "admin", "description": "Administrator with system access", "status": True, "permissions": []},
    {"id": 3, "name": "faculty", "description": "Faculty member", "status": True, "permissions": []},
    {"id": 4, "name": "student", "description": "University Student", "status": True, "permissions": []},
    {"id": 5, "name": "staff", "description": "University Staff", "status": True, "permissions": []},
]


@router.get("/setup")
async def setup_roles(_actor: User = Depends(_require_admin)):
    return [{"id": r["id"], "name": r["name"]} for r in ROLES_DATA]


@router.get("")
async def list_roles(_actor: User = Depends(_require_admin)):
    return ROLES_DATA


@router.get("/{role_id}")
async def get_role(role_id: int, _actor: User = Depends(_require_admin)):
    for r in ROLES_DATA:
        if r["id"] == role_id:
            return r
    return {"id": role_id, "name": "custom", "permissions": []}


@router.patch("/{role_id}/permissions")
async def update_role_permissions(
    role_id: int,
    payload: dict,
    _actor: User = Depends(_require_admin),
):
    for r in ROLES_DATA:
        if r["id"] == role_id:
            r["permissions"] = payload.get("permission_ids", [])
            return r
    return {"id": role_id, "name": "custom", "permissions": payload.get("permission_ids", [])}

