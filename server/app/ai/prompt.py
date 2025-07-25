# system prompt
SYSTEM_PROMPT = "你是一个政策研究专家"

def get_outline_prompt(title: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"根据以下政策探究结果，为'{title}'生成专项规划提纲"}
    ]

# def get_test_prompt() -> list[dict]:
#     return [
#         {"role": "user", "content": "你好"}
#     ]

def get_test_prompt() -> list[dict]:
    return [
        {"role": "user", "content": "你好"}
    ]