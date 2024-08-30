from fastapi import FastAPI
from .routers import dummy_data, refresh_database

app = FastAPI()

app.include_router(dummy_data.router)
app.include_router(refresh_database.router)
