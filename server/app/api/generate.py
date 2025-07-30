from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from ..ai.agent import ClassificationAgent, OutlineAgent
from typing import List, Optional
from .schemas import (
    ClassifyTitleRequest,
    ClassifyTitleReturn,
    GenerateOutlineRequest,
    GenerateOutlineReturn,
)
from ..ai.graph.outline import app as outline_graph_app
import traceback


generate_router = APIRouter()


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
        # The initial state requires 'title' and 'selectedKbList'.
        # The 'policy' and 'outline' fields will be populated by the graph.
        initial_state = {
            "title": req.title,
            "selectedKbList": [kb.model_dump() for kb in req.selectedKbList],
            # policy and outline are not needed for input
        }

        final_state = await outline_graph_app.ainvoke(initial_state)
        result_outline = final_state.get("outline", "生成大纲失败，未找到结果。")

        return GenerateOutlineReturn(
            success=True,
            title=req.title,
            outline=result_outline
        )
    
    except Exception as e:
        print(f"(from router_generate_outline, generate.py) 生成大纲异常: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}, (from router_generate_outline, generate.py)")


# @generate_router.post("/api/outline")
# async def router_generate_outline(req: GenerateOutlineRequest):
#     try: 
#         # # convert user selection into ids
#         # selected_bfs = req.selectedKbList
#         # selected_ids = kb.bf_to_id_lst(selected_bfs)

#         # result = agent.test_api()
        
#         result = outline_agent.generate_outline(req.title)
#         return GenerateOutlineReturn(
#             success=True,
#             title=req.title,
#             outline=result
#         )
#     except Exception as e:
#         print("(from router_generate_outline, generate.py)生成大纲异常：", e)
#         raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}, (from router_generate_outline, generate.py)")