# system prompt
SYSTEM_PROMPT = "你是一个政策研究专家"

def get_outline_prompt(title: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": (
            f"请为“{title}”生成一个专项规划提纲，要求如下：\n"
            "1. 以结构化 JSON 格式输出，不要输出任何解释或说明。\n"
            "2. 一级标题为章节标题（如“一、形式需求”），每个一级标题下有若干二级标题（如“（一）发展基础。”），二级标题放在 children 字段的数组里。\n"
            "3. 示例格式：\n"
            '[\n'
            '  {\n'
            '    "title": "一、形式需求",\n'
            '    "children": [\n'
            '      { "title": "（一）发展基础。" },\n'
            '      { "title": "（二）机遇与挑战。" }\n'
            '    ]\n'
            '  },\n'
            '  {\n'
            '    "title": "二、总体要求",\n'
            '    "children": [\n'
            '      { "title": "（一）指导思想。" },\n'
            '      { "title": "（二）发展原则。" },\n'
            '      { "title": "（三）发展布局。" },\n'
            '      { "title": "（四）发展目标。" }\n'
            '    ]\n'
            '  }\n'
            ']\n'
            "4. 只输出有效的 JSON 数据，不要有任何多余的文字。\n"
        )}
    ]

# def get_test_prompt() -> list[dict]:
#     return [
#         {"role": "user", "content": "你好"}
#     ]

def get_test_prompt() -> list[dict]:
    return [
        {"role": "user", "content": "你好"}
    ]