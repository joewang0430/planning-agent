from langgraph.graph import StateGraph
from pydantic import BaseModel
from typing import List
from ...api.schemas import KnowledgeBaseFile
from ...kb.utils import KnowledgeBase
from ...kb.query_chroma import Query
from ...ai.agent import KbAgent, OutlineAgent

kb = KnowledgeBase()
qry = Query()
kb_agent = KbAgent()
outline_agent = OutlineAgent()

AI_MAX_SELECT_NUM = 3
VEC_SELECT_NUM = 7

'''
outline knowledge base reference: 
- user maximum select 3;
- ai maximum select 3 based on title only; out of vector selection of 7, 
  but if not really relavant, ai can select less than 3 or 0

so the maximum reference knowledge base num is 6; minimun is 0.
'''

class OutlineState(BaseModel):
    title: str
    selectedKbList: List[KnowledgeBaseFile]
    # policy: str # TODO: consider change it later
    outline: str = ""


def node_select_kb(state: OutlineState): 
    '''
    returns: 
    all the kbs in selectedKbList, including user uploaded and ai selected.
    the returned data structure is like: 
        “09_城建环保/青岛市加快推动“专精特新”中小企业高质量发展行动方案（2022—2025年）.xml”
    '''
    title = state.title
    user_selected_bfs = state.selectedKbList

    # Overall: get the id of both user select + upload, and ai select
    # get the ai select kb in id format
    vec_relevant_ids = qry.query_relevant(title, VEC_SELECT_NUM)
    ai_selected_ids = kb_agent.select_kb(title, vec_relevant_ids, AI_MAX_SELECT_NUM)
    # convert [id] format of ai choice into [bf] format
    ai_selected_bfs = kb.id_to_bf_lst(ai_selected_ids)

    # TODO: test only, delete later
    print("--- 向量数据库检索到的相关ID (vec_relevant_ids): ---")
    print(vec_relevant_ids)
    print("----------------------------------------------------")
    
    print("--- AI从上述列表中筛选出的ID (ai_selected_ids): ---")
    print(ai_selected_ids)
    print("----------------------------------------------------")

    # integrate user choices and ai choices, delete overlaps
    # Pydantic models are not hashable, so can't use a set of objects directly.
    # We'll use a dictionary to ensure uniqueness based on a unique identifier (the ID).
    unique_bfs = {kb.bf_to_id(bf): bf for bf in user_selected_bfs}
    for bf in ai_selected_bfs:
        unique_bfs[kb.bf_to_id(bf)] = bf
    
    total_selected_bfs = list(unique_bfs.values())

    # Return a dictionary to update the state
    return {"selectedKbList": total_selected_bfs}


def node_generate_outline(state: OutlineState):
    """
    Reads content from the selected knowledge base files,
    constructs a RAG prompt, and generates the final outline.
    """
    title = state.title
    selected_bfs = state.selectedKbList

    # get contents of all selected kb, and use it to generate ai abstract
    selected_kb_contents = kb.get_all_kb_content(selected_bfs)
    selected_kb_abstract = kb_agent.abstract_kb_lst(title, selected_kb_contents)

    # use prompt and get outline result
    final_outline = outline_agent.generate_outline(title, selected_kb_abstract)

    return {"outline": final_outline}


# Construct the graph
wf = StateGraph(OutlineState)

wf.add_node("select_kb", node_select_kb)
wf.add_node("generate_outline", node_generate_outline)

wf.set_entry_point("select_kb")
wf.add_edge("select_kb", "generate_outline")
wf.add_edge("generate_outline", "__end__")

app = wf.compile()


    # code below is not needed: 
    # # extract selected db/file in bf format
    # user_selected_bfs_db = kb.bf_get_db(user_selected_bfs)
    # user_selected_bfs_file = kb.bf_get_file(user_selected_bfs)
    # # convert selected db, from bf format in id format, and integrate with ai choice
    # selected_db_ids = kb.bf_to_id_lst(user_selected_bfs)
    # final_unique_list = list(set(ai_selected_ids + selected_db_ids))






    

