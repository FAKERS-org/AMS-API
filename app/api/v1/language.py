from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import BaseModel

from app.core.dependencies import get_current_user
from app.core.permissions import Role, require_roles
from app.models.user import User

router = APIRouter()


def _require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    return require_roles(Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF)(current_user)


class LanguageModel(BaseModel):
    id: int
    code: str
    name: str
    native_name: str | None = None
    direction: str = "ltr"
    is_default: bool = False
    is_active: bool = True


LANGUAGES: list[dict] = [
    {
        "id": 1,
        "code": "en",
        "name": "English",
        "native_name": "English",
        "direction": "ltr",
        "is_default": True,
        "is_active": True,
    },
    {
        "id": 2,
        "code": "km",
        "name": "Khmer",
        "native_name": "ភាសាខ្មែរ",
        "direction": "ltr",
        "is_default": False,
        "is_active": True,
    },
]


@router.get("/setup-table")
async def setup_table(_actor: User = Depends(_require_admin)):
    return [
        {"value": "code", "label": "Code", "type": "text"},
        {"value": "name", "label": "Name", "type": "text"},
        {"value": "native_name", "label": "Native Name", "type": "text"},
        {"value": "direction", "label": "Direction", "type": "text"},
        {"value": "is_default", "label": "Default", "type": "boolean"},
        {"value": "is_active", "label": "Active", "type": "boolean"},
        {"value": "actions", "label": "Actions", "type": "actions"},
    ]


@router.get("/setup")
async def setup(_actor: User = Depends(_require_admin)):
    return {
        "name": "Language",
        "fields": [
            {"name": "code", "value": "code", "label": "Language Code", "type": "text", "is_required": True},
            {"name": "name", "value": "name", "label": "Language Name", "type": "text", "is_required": True},
            {"name": "native_name", "value": "native_name", "label": "Native Name", "type": "text"},
            {
                "name": "direction",
                "value": "direction",
                "label": "Text Direction",
                "type": "select",
                "options": [{"label": "Left to Right", "value": "ltr"}, {"label": "Right to Left", "value": "rtl"}],
            },
            {"name": "is_default", "value": "is_default", "label": "Default Language", "type": "switch"},
            {"name": "is_active", "value": "is_active", "label": "Active", "type": "switch"},
        ],
    }


@router.get("")
async def list_languages(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    _actor: User = Depends(_require_admin),
):
    filtered = LANGUAGES
    if search:
        s = search.lower()
        filtered = [l for l in filtered if s in l["name"].lower() or s in l["code"].lower()]
    total = len(filtered)
    start = (page - 1) * limit
    paged = filtered[start : start + limit]
    return {
        "data": paged,
        "meta": {
            "currentPage": page,
            "perPage": limit,
            "totalPages": max(1, (total + limit - 1) // limit),
            "totalItems": total,
        },
    }


@router.get("/{language_id}/view")
async def view_language(language_id: int, _actor: User = Depends(_require_admin)):
    for l in LANGUAGES:
        if l["id"] == language_id:
            return l
    return LANGUAGES[0]


@router.get("/{language_id}")
async def get_language(language_id: int, _actor: User = Depends(_require_admin)):
    for l in LANGUAGES:
        if l["id"] == language_id:
            return l
    return LANGUAGES[0]


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_language(payload: dict, _actor: User = Depends(_require_admin)):
    new_id = max([l["id"] for l in LANGUAGES], default=0) + 1
    item = {
        "id": new_id,
        "code": payload.get("code", f"lang{new_id}"),
        "name": payload.get("name", "New Language"),
        "native_name": payload.get("native_name", ""),
        "direction": payload.get("direction", "ltr"),
        "is_default": payload.get("is_default", False),
        "is_active": payload.get("is_active", True),
    }
    LANGUAGES.append(item)
    return item


@router.put("/{language_id}")
async def update_language(language_id: int, payload: dict, _actor: User = Depends(_require_admin)):
    for l in LANGUAGES:
        if l["id"] == language_id:
            l.update({k: v for k, v in payload.items() if v is not None})
            return l
    return LANGUAGES[0]


@router.delete("/{language_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_language(language_id: int, _actor: User = Depends(_require_admin)):
    global LANGUAGES
    LANGUAGES = [l for l in LANGUAGES if l["id"] != language_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)

