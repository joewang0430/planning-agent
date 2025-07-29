from langgraph.graph import StateGraph
from openai import OpenAI
from typing import TypedDict
import os
from dotenv import load_dotenv
from .prompt import Prompt

load_dotenv()
DEFAULT_MODEL_NAME = "moonshot-v1-8k"

EXAMPLE_TITLE_1 = "杭州市政府关于十五五的专项规划"
EXAMPLE_TITLE_2 = "杭州市城市轨道交通网络‘十五五’发展专项规划（2021-2025年）"

# config kimi api client, globally
# client = OpenAI(
#     api_key=os.getenv("API_KEY"), 
#     base_url=os.getenv("BASE_URL"), 
# )

# define state struct for langgraph
class PlanningState(TypedDict):
    title: str
    # policy_research: str 
    outline: str 
    content: str 


# class for embedding
class EmbeddingAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("EBD_API_KEY"), 
            base_url=os.getenv("EBD_BASE_URL"), 
        )
        self.model_name = os.getenv("EBD_MODEL_NAME")
    
    def get_embedding(self, text: str):
        """
        generate embedding for text
        """
        try:
            response = self.client.embeddings.create(
                model=self.model_name,
                input=[text],
                encoding_format="float"
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"[错误] 获取 embedding 失败: {e}")
            return None


# AI operates knowledge base
class KbAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("API_KEY"), 
            base_url=os.getenv("BASE_URL"), 
        )
        self.model_name = os.getenv("MODEL_NAME", DEFAULT_MODEL_NAME)
    
    def select_kb(self, title: str, lst: str, num: int):
        messages = Prompt.get_kb_selection_prompt(title, lst)
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )
        classification = completion.choices[0].message.content
        return classification


# check if the title is valid
class ClassificationAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("API_KEY"), 
            base_url=os.getenv("BASE_URL"), 
        )
        self.model_name = os.getenv("MODEL_NAME", DEFAULT_MODEL_NAME)

    def classify_title(self, title: str):
        messages = Prompt.get_classification_prompt(title)
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )
        classification = completion.choices[0].message.content
        return classification


# class solving outline
class OutlineAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("API_KEY"), 
            base_url=os.getenv("BASE_URL"), 
        )
        self.model_name = os.getenv("MODEL_NAME", DEFAULT_MODEL_NAME)

    def generate_outline(self, title: str):
        messages = Prompt.get_outline_prompt(title)
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )
        outline = completion.choices[0].message.content
        return outline


# test if api works
class TestAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("API_KEY"), 
            base_url=os.getenv("BASE_URL"), 
        )
        self.model_name = os.getenv("MODEL_NAME", DEFAULT_MODEL_NAME)
    
    def test_api(self):
        messages = Prompt.get_test_prompt()
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )
        answer = completion.choices[0].message.content
        
        return answer

# test
if __name__ == "__main__":
    tested_agent = ClassificationAgent()
    answer = tested_agent.classify_title("杭州市政府‘十五五’建设的专项规划（2025）")
    print(answer)