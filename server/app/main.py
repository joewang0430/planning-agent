# main entrance of the 专项规划Agent project

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Planning Agent API", version="1.0.0")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 前端 Next.js 默认端口，根据需要配置
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# test
@app.get("/ping")
async def root():
    return {"message": "PONG! Planning Agent API is running!"}
