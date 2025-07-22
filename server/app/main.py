# main entrance of the Planning Agent Project server.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Planning Agent API", version="1.0.0")

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# test
@app.get("/ping")
async def root():
    return {"message": "PONG! Planning Agent API is running!"}
