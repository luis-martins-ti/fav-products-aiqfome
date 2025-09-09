from fastapi import APIRouter
from app.api import client
from app.auth import routes as auth_routes

router = APIRouter()

router.include_router(auth_routes.router)
router.include_router(client.router)

