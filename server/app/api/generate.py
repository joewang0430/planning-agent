from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from ..ai.agent import ClassificationAgent, OutlineAgent


generate_router = APIRouter()


# STRUCT: classify title
class ClassifyTitleRequest(BaseModel):
    title: str
class ClassifyTitleReturn(BaseModel):
    valid: bool

# STRUCT: generate outline
# TOSTRUCT
class GenerateOutlineRequest(BaseModel):
    title: str
class GenerateOutlineReturn(BaseModel):
    success: bool
    title: str
    outline: str


classify_agent = ClassificationAgent()
outline_agent = OutlineAgent()


@generate_router.post("/api/classify_title")
async def router_classify_title(req: ClassifyTitleRequest):
    try:
        result = classify_agent.classify_title(req.title)
        return ClassifyTitleReturn(valid=(result.strip().lower() == "true"))    #return { valid: True/False }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"标题检测失败: {str(e)}  (from router_generate_outline, generate.py)")
    

@generate_router.post("/api/outline")
async def router_generate_outline(req: GenerateOutlineRequest):
    try: 
        # result = agent.test_api()
        result = outline_agent.generate_outline(req.title)
        return GenerateOutlineReturn(
            success=True,
            title=req.title,
            outline=result
        )
    except Exception as e:
        print("(from router_generate_outline, generate.py)生成大纲异常：", e)
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}, (from router_generate_outline, generate.py)")