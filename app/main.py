from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.api.v1.router import v1_router
from app.api.public.router import public_router

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

    app.include_router(v1_router, prefix=settings.API_V1_PREFIX)
    app.include_router(public_router, prefix=settings.API_PUBLIC_PREFIX)

    @app.get("/health", tags=["Health"])
    async def health():
        return {"status": "ok"}

    return app


app = create_app()