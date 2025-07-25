from langgraph.graph import StateGraph
from openai import OpenAI
from typing import TypedDict
import os
from dotenv import load_dotenv
from .prompt import get_outline_prompt, get_test_prompt

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
    messages = get_outline_prompt(title)

    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=messages,
    )

    outline = completion.choices[0].message.content
    state["outline"] = outline
    return state

# test if api works
def test_api():
    messages = get_test_prompt()
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