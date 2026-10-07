import enum
from functools import wraps
from typing import Callable

from fastapi import HTTPException, status


class Role(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    FACULTY = "faculty"
    STUDENT = "student"
    STAFF = "staff"

ROLE_HIERARCHY = {
    Role.STUDENT: 0,
    Role.STAFF: 1,
    Role.FACULTY: 2,
    Role.ADMIN: 3,
    Role.SUPER_ADMIN: 4,
}


def require_roles(*allowed: Role):
    
    def _checker(current_user):
        user_role = Role(current_user.role)
        if user_role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return _checker


def require_min_role(min_role: Role):
    
    def _checker(current_user):
        user_role = Role(current_user.role)
        if ROLE_HIERARCHY[user_role] < ROLE_HIERARCHY[min_role]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return _checker