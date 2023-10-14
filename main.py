from fastapi import FastAPI
from app.enpoint.base_router import router_login, router_user, router_question


app = FastAPI()


app.include_router(router_login)
app.include_router(router_user)
app.include_router(router_question)