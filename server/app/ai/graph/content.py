# later can add more nodes as business expands

from langgraph.graph import StateGraph
from pydantic import BaseModel
from ...ai.agent import ContentAgent


content_agent = ContentAgent()


class ContentState(BaseModel):
    title: str
    outline: str
    context: str
    content: str = ""


def node_generate_content(state: ContentState):
    title = state.title
    outline = state.outline
    context = state.context

    content = content_agent.generate_content(title, outline, context)

    return {"content": content}

# Construct the graph
wf = StateGraph(ContentState)

wf.add_node("generate_content", node_generate_content)
wf.set_entry_point("generate_content")
wf.add_edge("generate_content", "__end__")

app = wf.compile()