from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.public.router import public_router
from app.api.v1.router import v1_router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ── Middleware ──
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    # ── V1 Admin / Authenticated & University Routes (/api/v1/...) ──
    app.include_router(v1_router, prefix=settings.API_V1_PREFIX)

    # ── Public Endpoints (/api/v1/ams-public matching NestJS app.routes.ts) ──
    app.include_router(public_router, prefix="/api/v1/ams-public")
    app.include_router(public_router, prefix=settings.API_PUBLIC_PREFIX, include_in_schema=False)
    app.include_router(public_router, prefix="/api/public", include_in_schema=False)

    @app.get("/health", tags=["Health"])
    async def health():
        return {"status": "ok"}

    return app


app = create_app()