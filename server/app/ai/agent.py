from langgraph.graph import StateGraph
from openai import OpenAI
from typing import TypedDict
import os
from dotenv import load_dotenv

load_dotenv()

# config kimi api client
client = OpenAI(
    api_key=os.getenv("MOONSHOT_API_KEY"), 
    base_url="https://api.moonshot.cn/v1",
)

# define state struct for langgraph
class PlanningState(TypedDict):
    title: str
    # policy_research: str 
    outline: str 
    content: str 

def generate_outline(state: PlanningState) -> PlanningState:
    '''生成提纲'''
    title = state["title"]
    
    messages = [
        {"role": "system", "content": "你是一个政策研究专家"},
        {"role": "user", "content": f"根据以下政策探究结果，为'{title}'生成专项规划提纲"}
    ]

    completion = client.chat.completions.create(
        model="moonshot-v1-128k",
        messages=messages,
    )

    outline = completion.choices[0].message.content
    state["outline"] = outline
    return state

# test if api works
def test_api():
    messages = [
        {"role": "user", "content": "你好"}
    ]
    completion = client.chat.completions.create(
        model="moonshot-v1-128k",
        messages=messages,
    )
    answer = completion.choices[0].message.content
    
    return answer

# test
if __name__ == "__main__":
    answer = test_api()
    print(answer)