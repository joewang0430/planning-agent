from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from ..ai import agent

generate_router = APIRouter()

# STRUCT: generate outline
# TOSTRUCT
class GenerateOutlineRequest(BaseModel):
    title: str
class GenerateOutlineReturn(BaseModel):
    success: bool
    title: str
    outline: str


@generate_router.post("/api/outline")
async def router_generate_outline(req: GenerateOutlineRequest):
    try: 
        result = agent.test_api()
        return GenerateOutlineReturn(
            success=True,
            title=req.title,
            outline=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}, (from router_generate_outline, generate.py)")