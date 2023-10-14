from fastapi import APIRouter
from app.enpoint.router_of_all_parts.user_router import router as router_user
from app.enpoint.router_of_all_parts.user_login import router as router_login
from app.enpoint.router_of_all_parts.question import router as router_question


api_router = APIRouter()

api_router.include_router(router_user, prefix="/users", tags=["users"])
api_router.include_router(router_login, prefix="/login", tags=["login"])
api_router.include_router(router_question, prefix="/question", tags=["question"])

