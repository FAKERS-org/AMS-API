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


PERMISSIONS_DATA = [
    {"id": 1, "name": "manage_users", "description": "Can manage users", "status": True},
    {"id": 2, "name": "manage_university", "description": "Can manage university courses, students, and faculties", "status": True},
    {"id": 3, "name": "manage_content", "description": "Can manage events, awards, and projects", "status": True},
    {"id": 4, "name": "view_analytics", "description": "Can view dashboard analytics", "status": True},
]


@router.get("")
async def list_permissions(_actor: User = Depends(_require_admin)):
    return PERMISSIONS_DATA


@router.get("/{permission_id}")
async def get_permission(permission_id: int, _actor: User = Depends(_require_admin)):
    for p in PERMISSIONS_DATA:
        if p["id"] == permission_id:
            return p
    return {"id": permission_id, "name": "custom_permission", "status": True}


@router.patch("/role-permission/{permission_id}/toggle")
async def toggle_role_permission(permission_id: int, _actor: User = Depends(_require_admin)):
    return {"status": True}

