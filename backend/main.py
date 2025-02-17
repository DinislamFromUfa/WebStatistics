from fastapi import FastAPI

from .userrouter import router

app = FastAPI()

app.include_router(router)


