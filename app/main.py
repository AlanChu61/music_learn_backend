from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, courses, submissions, refresh_database

app = FastAPI()

# 設置 CORS 規則
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有 HTTP 標頭
)
app.include_router(users.router)
# app.include_router(courses.router)
app.include_router(submissions.router)
app.include_router(refresh_database.router)


# WebSocket 连接
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(f"Message received: {data}")
        await websocket.send_text(f"Message text was: {data}")


# HTTP 根路由
@app.get("/")
def root():
    return {"message": "Welcome to the Music Learning Platform!"}
