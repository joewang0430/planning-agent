# main entrance of the Planning Agent Project server.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from .api import generate, base

load_dotenv()

app = FastAPI(title="Planning Agent API", version="1.0.0")

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(generate.generate_router)
app.include_router(base.base_router, prefix="/api")

# test
@app.get("/ping")
async def root():
    return {"message": "PONG! Planning Agent API is running!"}
    