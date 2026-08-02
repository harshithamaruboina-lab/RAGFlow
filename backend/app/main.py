from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging


def create_app() -> FastAPI:

    configure_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        description="RAGFlow API — Multi-Modal Knowledge Graph Synthesis for Enterprise Compliance",
    )


    # CORS FIX FOR FRONTEND
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5174",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    register_exception_handlers(app)


    app.include_router(
        api_router,
        prefix=settings.API_V1_PREFIX
    )


    @app.get("/")
    def root():
        return {
            "message": "RAGFlow API is running"
        }


    return app



app = create_app()