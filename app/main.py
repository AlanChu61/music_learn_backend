from fastapi import FastAPI
from .routers import refresh_database, users, courses, submissions

app = FastAPI()

app.include_router(refresh_database.router)
app.include_router(users.router)
# app.include_router(courses.router)
# app.include_router(submissions.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Music Learning Platform!"}
