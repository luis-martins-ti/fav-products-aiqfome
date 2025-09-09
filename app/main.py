from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import router as api_router
from app.db.database import engine, Base
from loguru import logger
from contextlib import asynccontextmanager

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Aplicação iniciada")
    yield
    logger.info("🛑 Aplicação finalizada")


app = FastAPI(
    title="AiQFome Fav Products API",
    description="API de Gestão de Produtos Favoritos",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router)
