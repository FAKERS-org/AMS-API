from fastapi import APIRouter, Depends, Query, Response, status

from app.core.dependencies import get_current_user
from app.core.permissions import Role, require_roles
from app.models.user import User

router = APIRouter()


def _require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    return require_roles(Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF)(current_user)


RESEARCH_INTERESTS: list[dict] = [
    {
        "id": 1,
        "name": "Artificial Intelligence & Robotics",
        "description": "Exploration of neural networks, reinforcement learning, and autonomous robotic systems.",
        "faculties": [],
        "students": [],
    },
    {
        "id": 2,
        "name": "Cybersecurity & Cloud Systems",
        "description": "Network defense, zero-trust architectures, and cryptography.",
        "faculties": [],
        "students": [],
    },
    {
        "id": 3,
        "name": "Data Science & Machine Learning",
        "description": "Large-scale data analysis, deep learning, and predictive models.",
        "faculties": [],
        "students": [],
    },
]


@router.get("/setup-table")
async def setup_table(_actor: User = Depends(_require_admin)):
    return [
        {"value": "name", "label": "Name", "type": "text"},
        {"value": "description", "label": "Description", "type": "text"},
        {"value": "faculties", "label": "Faculties", "type": "multi-select"},
        {"value": "students", "label": "Students", "type": "multi-select"},
        {"value": "actions", "label": "Actions", "type": "actions"},
    ]


@router.get("/setup")
async def setup(_actor: User = Depends(_require_admin)):
    return {
        "name": "Research Interest",
        "fields": [
            {"name": "name", "value": "name", "type": "text", "label": "Name", "is_required": True},
            {"name": "description", "value": "description", "type": "textarea", "label": "Description"},
        ],
    }


@router.get("")
async def list_research_interests(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    _actor: User = Depends(_require_admin),
):
    filtered = RESEARCH_INTERESTS
    if search:
        s = search.lower()
        filtered = [r for r in filtered if s in r["name"].lower()]
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


@router.get("/{interest_id}/view")
async def view_research_interest(interest_id: int, _actor: User = Depends(_require_admin)):
    for r in RESEARCH_INTERESTS:
        if r["id"] == interest_id:
            return r
    return RESEARCH_INTERESTS[0]


@router.get("/{interest_id}")
async def get_research_interest(interest_id: int, _actor: User = Depends(_require_admin)):
    for r in RESEARCH_INTERESTS:
        if r["id"] == interest_id:
            return r
    return RESEARCH_INTERESTS[0]


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_research_interest(payload: dict, _actor: User = Depends(_require_admin)):
    new_id = max([r["id"] for r in RESEARCH_INTERESTS], default=0) + 1
    item = {
        "id": new_id,
        "name": payload.get("name", f"Research Interest {new_id}"),
        "description": payload.get("description", ""),
        "faculties": payload.get("faculties", []),
        "students": payload.get("students", []),
    }
    RESEARCH_INTERESTS.append(item)
    return item


@router.put("/{interest_id}")
async def update_research_interest(interest_id: int, payload: dict, _actor: User = Depends(_require_admin)):
    for r in RESEARCH_INTERESTS:
        if r["id"] == interest_id:
            r.update({k: v for k, v in payload.items() if v is not None})
            return r
    return RESEARCH_INTERESTS[0]


@router.delete("/{interest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_research_interest(interest_id: int, _actor: User = Depends(_require_admin)):
    global RESEARCH_INTERESTS
    RESEARCH_INTERESTS = [r for r in RESEARCH_INTERESTS if r["id"] != interest_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)

