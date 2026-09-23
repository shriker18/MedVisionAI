from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import analysis, health, history
from app.services.database import init_db


app = FastAPI(
    title="MedVision API",
    description="Multimodal medical image analysis and clinical information support prototype.",
    version="1.0.0",
)

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    health.router,
    prefix="/health",
    tags=["Health"],
)

app.include_router(
    analysis.router,
    prefix="/analysis",
    tags=["Analysis"],
)

app.include_router(
    history.router,
    prefix="/history",
    tags=["History"],
)