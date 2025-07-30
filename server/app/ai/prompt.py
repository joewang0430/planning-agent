# system prompt
SYSTEM_PROMPT = "你是一个政策研究专家"

class Prompt: 
    @staticmethod
    def get_classification_prompt(title: str) -> list[dict]:
        return [
            {"role": "system", "content": "你是一个政策规划领域的智能助手，负责判断用户输入的标题是否为有效的专项规划标题。"},
            {"role": "user", "content": (
                f"请判断以下标题是否为有效的专项规划标题：\n"
                f"“{title}”\n"
                "如果标题内容明确、具体，且与政策、规划相关，则返回“true”；"
                "如果标题内容过于简单、无意义或与规划无关，则返回“false”。\n"
                "请只返回 true 或 false，不要输出其他内容。"
            )}
        ]
    
    @staticmethod
    def get_kb_selection_prompt(title: str, id_list: list[str], num: int = 3) -> list[dict]:
        # Convert the ID list to a formatted string for clear display in the prompt
        id_list_str = "\n".join(id_list)
        return [
            {
                "role": "system",
                "content": (
                    "你是一个精准的政策研究助手。你的任务是根据用户提供的专项规划标题，从一个候选知识库ID列表中，筛选出与标题内容最相关的ID。"
                    "你返回的结果必须是一个JSON数组，其中只包含你选中的ID字符串。"
                )
            },
            {
                "role": "user",
                "content": (
                    f"我正在研究以下专项规划标题：\n"
                    f"“{title}”\n\n"
                    f"请从下面这个候选知识库ID列表中，仔细评估每个ID中'/'后面的文件名与上述标题的关联度，并挑选出最多 {num} 个最相关的ID。\n"
                    f"候选知识库ID列表：\n"
                    f"```\n"
                    f"{id_list_str}\n"
                    f"```\n\n"
                    f"请遵循以下规则：\n"
                    f"1. 你的选择必须完全基于相关性。如果候选列表中没有足够相关的ID，你可以选择少于 {num} 个，极端情况下可以返回一个空列表[]。\n"
                    f"2. 返回的结果必须是一个JSON格式的字符串数组，例如：[\"id1.xml\", \"id2.xml\"]。\n"
                    f"3. 除了这个JSON数组，不要包含任何解释、注释或其他多余的文字。"
                )
            }
        ]
    
    @staticmethod
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

    @staticmethod
    def get_test_prompt() -> list[dict]:
        return [
            {"role": "user", "content": "你好"}
        ]