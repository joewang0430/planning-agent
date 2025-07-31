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
    GenerateContentRequest,
    GenerateContentReturn,
    RewriteOutlineRequest,
    RewriteOutlineReturn,
    RewriteSubtitleRequest,
    RewriteSubtitleReturn,
    RewriteSectionRequest,
    RewriteSectionReturn,
)
from ..ai.graph.outline import app as outline_graph_app
from ..ai.graph.content import app as content_graph_app
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
        raise HTTPException(status_code=500, detail=f"标题检测失败: {str(e)}  (from router_classify_title, generate.py)")
    

@generate_router.post("/api/outline")
async def router_generate_outline(req: GenerateOutlineRequest):
    try:
        # The initial state requires 'title' and 'selectedKbList'.
        # The 'policy' and 'outline' fields will be populated by the graph.
        initial_state = {
            "title": req.title,
            "selectedKbList": [kb.model_dump() for kb in req.selectedKbList],
            "policy": "",
            # outline is not needed for input
        }

        final_state = await outline_graph_app.ainvoke(initial_state)
        result_outline = final_state.get("outline", "生成大纲失败，未找到结果。")
        result_policy = final_state.get("policy", "未能生成政策总结。")
        result_kb_list = final_state.get("selectedKbList", [])

        return GenerateOutlineReturn(
            success=True,
            title=req.title,
            outline=result_outline,
            policy=result_policy,
            kb_list=result_kb_list,
        )
    
    except Exception as e:
        print(f"(from router_generate_outline, generate.py) 生成大纲异常: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}, (from router_generate_outline, generate.py)")


@generate_router.post("/api/rewrite/outline")
async def router_rewrite_outline(req: RewriteOutlineRequest):
    try:
        new_outline = outline_agent.generate_outline(req.title, req.context)
        return RewriteOutlineReturn(
            success=True,
            title=req.title,
            outline=new_outline
        )
    except Exception as e:
        print(f"(from router_rewrite_outline, generate.py) 重写大纲异常: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"重写大纲失败: {str(e)}, (from router_rewrite_outline, generate.py)")


@generate_router.post("/api/content")
async def router_generate_content(req: GenerateContentRequest):
    try: 
        initial_state = {
            "title": req.title,
            "outline": req.outline,
            "context": req.context,
            # content is not needed for input (I guess)
        }

        final_state = await content_graph_app.ainvoke(initial_state)
        result_content = final_state.get("content", "生成内容失败，未找到结果。")

        return GenerateContentReturn(
                success=True,
                title=req.title,
                content=result_content,
        )
    
    except Exception as e:
        print(f"(from router_generate_content, generate.py) 生成内容异常: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"生成内容失败: {str(e)}, (from router_generate_content, generate.py)")
    

@generate_router.post("/api/rewrite/subtitle")
async def router_rewrite_subtitle(req: RewriteSubtitleRequest):
    try:
        new_title = outline_agent.rewrite_subtitle(
            plan_title=req.plan_title,
            full_outline=req.full_outline,
            parent_title=req.parent_title,
            current_subtitle=req.current_subtitle,
            context=req.context,
            user_requirement=req.user_requirement
        )
        return RewriteSubtitleReturn(new_title=new_title)
    except Exception as e:
        print(f"(from router_rewrite_subtitle, generate.py) 重写二级标题异常: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"重写二级标题失败: {str(e)}")


@generate_router.post("/api/rewrite/section")
async def router_rewrite_section(req: RewriteSectionRequest):
    try:
        new_section = outline_agent.rewrite_section(
            plan_title=req.plan_title,
            full_outline=req.full_outline,
            current_section=req.current_section,
            policy_context=req.policy_context,
            user_requirement=req.user_requirement
        )
        # 检查 agent 是否返回了错误字典
        if isinstance(new_section, dict) and 'error' in new_section:
             raise Exception(f"AI Agent Error: {new_section.get('raw_content', new_section.get('error'))}")

        return RewriteSectionReturn(new_section=new_section)
    except Exception as e:
        print(f"(from router_rewrite_section, generate.py) 重写章节异常: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"重写章节失败: {str(e)}")


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