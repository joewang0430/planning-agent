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
        id_list_str = "\n".join(id_list)
        return [
            {
                "role": "system",
                "content": (
                    "你是一个精准的政策研究助手。你的任务是根据用户提供的专项规划标题，从一个候选知识库ID列表中，筛选出与标题内容最相关的ID。"
                    "你返回的结果必须是一个JSON对象，格式为：{\"selected_ids\": [\"id1.xml\", \"id2.xml\", ...]}。"
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
                    f"2. 返回的结果必须是一个JSON对象，其 'selected_ids' 键对应一个字符串数组。例如：{{\"selected_ids\": [\"id1.xml\", \"id2.xml\"]}}。\n"
                    f"3. 除了这个JSON对象，不要包含任何解释、注释或其他多余的文字。"
                )
            }
        ]
    
    @staticmethod
    def get_abstract_prompt(title: str, content_lst: list[str]) -> list[dict]:
        """
        Generates a prompt for summarizing a list of knowledge base contents.
        """
        num_contents = len(content_lst)
        target_word_count = num_contents * 100
        
        # Combine all content pieces into a single block for the prompt
        combined_content = "\n\n---\n\n".join(content_lst)

        return [
            {
                "role": "system",
                "content": (
                    "你是一位顶级的政策研究专家和内容提炼大师。你的任务是为一个特定的专项规划标题，将多个分散的知识库内容片段，提炼成一份连贯、精炼、高度相关的核心内容摘要。"
                )
            },
            {
                "role": "user",
                "content": (
                    f"我正在为以下专项规划标题撰写专项规划：\n"
                    f"“{title}”\n\n"
                    f"请仔细阅读并理解下面的 {num_contents} 份知识库内容，然后为我生成一份综合性的内容摘要。\n"
                    f"知识库内容片段如下：\n"
                    f"```\n"
                    f"{combined_content}\n"
                    f"```\n\n"
                    f"请遵循以下规则：\n"
                    f"1. **核心目标**：你的摘要必须紧密围绕标题“{title}”，只保留与该标题最直接相关的信息。\n"
                    f"2. **内容整合**：不要简单地罗列或拼接原文，你需要理解、重组和提炼所有片段中的关键信息，形成一个有逻辑、有条理的整体。\n"
                    f"3. **长度控制**：生成的摘要字数应在 **{target_word_count}** 字左右。但是，这是一个指导性目标，内容质量永远是第一位的。如果原始材料本身信息量较少，你可以生成更短的摘要，甚至在极端情况下，如果内容非常精炼，可以直接整合原文。请不要为了凑字数而添加无关信息。\n"
                    f"4. **格式要求**：请直接输出摘要内容，不要包含任何解释、标题或多余的客套话。"
                )
            }
        ]
    
    @staticmethod
    def get_outline_prompt(title: str, kb_abstract: str = "") -> list[dict]:
        """
        Generates a prompt to create a structured outline.
        If kb_abstract is provided, it will be included as a reference.
        """
        # The basic requirements are applicable in both cases
        base_requirements = (
            "1. 以结构化 JSON 格式输出，不要输出任何解释或说明。\n"
            "2. 一级标题为章节标题（如“一、形式需求”），每个一级标题下有若干二级标题（如“（一）发展基础。”），二级标题放在 children 字段的数组里。最少也要列三个一级标题\n"   # this can be changed later
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
        )

        # Dynamically construct user instructions based on whether kb_abstract is empty
        if not kb_abstract or not kb_abstract.strip():
            # Situation 1: kb_abstract is empty and returns the simple prompt
            user_content = (
                f"请为“{title}”生成一个专项规划提纲，要求如下：\n"
                f"{base_requirements}"
            )
        else:
            # Situation 2: kb_abstract is not empty; add reference information
            user_content = (
                f"请为“{title}”生成一个专项规划提纲。\n\n"
                f"这是整理的知识库摘要，供你参考：\n"
                f"```\n"
                f"{kb_abstract}\n"
                f"```\n\n"
                f"请结合参考资料，并围绕标题生成提纲，要求如下：\n"
                f"{base_requirements}"
            )

        return [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ]
    
    @staticmethod
    def get_content_prompt(title: str, outline: str, context: str = "") -> list[dict]:
        """
        Generates a prompt to write detailed content for each second-level title in an outline.
        If context is provided, it will be included as a reference.
        """
        # The basic instructions define the core tasks and output formats
        base_requirements = (
            "1. **核心任务**：请为下面这个大纲的**每一个二级标题**，撰写详细、专业的阐述内容。\n"
            "2. **输出格式**：你的输出必须是一个单一的、结构化的JSON对象。此JSON对象应包含一个名为 `content_outline` 的键，其值的结构与我提供的大纲完全一致，但在每个二级标题的对象中，增加一个名为 `content` 的键，值为你生成的详细内容字符串。\n"
            "3. **示例格式**：\n"
            '   {\n'
            '     "content_outline": [\n'
            '       {\n'
            '         "title": "一、发展基础与面临形势",\n'
            '         "children": [\n'
            '           { "title": "（一）发展基础", "content": "这里是为“发展基础”生成的详细内容..." },\n'
            '           { "title": "（二）面临形势", "content": "这里是为“面临形势”生成的详细内容..." }\n'
            '         ]\n'
            '       }\n'
            '     ]\n'
            '   }\n'
            "4. **严格要求**：除了这个JSON对象，绝对不要包含任何解释、注释、代码块标记（如```json ... ```）或其他多余的文字。"
        )

        # Dynamically construct user instructions based on whether the context is empty or not
        if not context or not context.strip():
            # empty
            user_content = (
                f"我正在撰写关于“{title}”的专项规划。\n\n"
                f"这是规划的大纲结构：\n"
                f"```json\n"
                f"{outline}\n"
                f"```\n\n"
                f"请严格遵循以下要求：\n"
                f"{base_requirements}"
            )
        else:
            # not empty
            user_content = (
                f"我正在撰写关于“{title}”的专项规划。\n\n"
                f"这是规划的大纲结构：\n"
                f"```json\n"
                f"{outline}\n"
                f"```\n\n"
                f"这是供你参考的知识库摘要：\n"
                f"```\n"
                f"{context}\n"
                f"```\n\n"
                f"请在参考上述资料的基础上，严格遵循以下要求：\n"
                f"{base_requirements}"
            )

        return [
            {"role": "system", "content": "你是一位顶级的政策研究和公文撰写专家，擅长将结构化的要点扩展为内容详实、逻辑严谨的段落。"},
            {"role": "user", "content": user_content}
        ]

    @staticmethod
    def get_rewrite_subtitle_prompt(
        plan_title: str,
        full_outline: list,
        parent_title: str,
        current_subtitle: str,
        context: str,
        user_requirement: str = ""
    ) -> list[dict]:
        """
        Generates a prompt to rewrite a single second-level title, with full outline context.
        """
        import json
        # If the user has no input requirements, a default instruction will be provided
        requirement_prompt = f"用户的具体要求是：『{user_requirement}』。" if user_requirement and user_requirement.strip() else "请基于整体大纲结构和参考资料，优化这个标题，使其更精准、更专业。"
        
        # If there is no knowledge base summary, no relevant prompt will be displayed
        context_prompt = f"背景参考资料如下：\n```\n{context}\n```\n" if context and context.strip() else ""

        user_content = (
            f"我正在撰写一份名为《{plan_title}》的专项规划。这是当前规划的完整大纲结构，供你理解上下文：\n"
            f"```json\n{json.dumps(full_outline, ensure_ascii=False, indent=2)}\n```\n\n"
            f"{context_prompt}\n"
            f"**核心任务**：请聚焦于大纲中的『{parent_title}』这一章，找到并重写其下的二级标题：『{current_subtitle}』。\n"
            f"{requirement_prompt}\n\n"
            f"**严格要求**：请只返回重写后的新标题字符串，不要包含任何JSON格式、引号、解释或其他多余文字。"
        )

        return [
            {"role": "system", "content": "你是一位精通公文措辞的专家，擅长在理解整体结构的基础上，对局部细节进行优化和精炼。"},
            {"role": "user", "content": user_content}
        ]

    @staticmethod
    def get_rewrite_section_prompt(
        plan_title: str,
        full_outline: list,
        current_section: dict,
        policy_context: str,
        user_requirement: str = ""
    ) -> list[dict]:
        """
        Generates a prompt to rewrite an entire section, with full outline context.
        """
        import json
        requirement_prompt = f"用户的额外要求是：『{user_requirement}』。" if user_requirement and user_requirement.strip() else "请基于参考政策和整体大纲的上下文，优化当前章节的逻辑结构和标题。"
        
        context_prompt = f"请参考以下政策要点：\n【政策参考】\n{policy_context}\n【参考结束】\n\n" if policy_context and policy_context.strip() else ""

        user_content = (
            f"我正在撰写一份名为《{plan_title}》的专项规划。\n"
            f"{context_prompt}"
            f"这是当前规划的完整大纲结构，供你理解整体上下文：\n"
            f"```json\n{json.dumps(full_outline, ensure_ascii=False, indent=2)}\n```\n\n"
            f"**核心任务**：请聚焦于上述大纲中的以下章节，并对其进行重写：\n"
            f"```json\n{json.dumps(current_section, ensure_ascii=False, indent=2)}\n```\n"
            f"重写需要覆盖该章节的一级标题及其下属的所有二级标题，重写后二级标题的数量和内容都可以发生变化。\n"
            f"{requirement_prompt}\n\n"
            f"**输出格式要求**：你的回答必须是一个单一、完整的JSON对象，该对象代表重写后的新章节。格式如下：\n"
            '{\n'
            '  "title": "新的一级标题",\n'
            '  "children": [\n'
            '    { "title": "新的二级标题A" },\n'
            '    { "title": "新的二级标题B" }\n'
            '  ]\n'
            '}\n'
            "除了这个JSON对象，不要返回任何其他内容。"
        )

        return [
            {"role": "system", "content": "你是一位顶级的政策研究和规划专家，擅长在把握全局的前提下，对局部章节进行深度重构和优化。"},
            {"role": "user", "content": user_content}
        ]
    
    @staticmethod
    def get_rewrite_content_prompt(
        plan_title: str,
        section_title: str,
        subtitle_title: str,
        current_content: str,
        context: str,
        user_requirement: str = ""
    ) -> list[dict]:
        """
        Generates a prompt to rewrite a paragraph of content.
        """
        # If the user has no input requirements, a default instruction will be provided
        requirement_prompt = f"用户的具体要求是：『{user_requirement}』。" if user_requirement and user_requirement.strip() else "请基于参考资料和上下文，优化这段内容的措辞和逻辑，使其更专业、更流畅。"
        
        # If there is no knowledge base summary, no relevant prompt will be displayed
        context_prompt = f"请参考以下政策要点：\n【政策参考】\n{context}\n【参考结束】\n\n" if context and context.strip() else ""

        user_content = (
            f"我正在为一个名为《{plan_title}》的专项规划撰写内容。\n"
            f"{context_prompt}"
            f"**任务上下文**：\n"
            f"- 当前章节（一级标题）：『{section_title}』\n"
            f"- 当前小节（二级标题）：『{subtitle_title}』\n\n"
            f"**核心任务**：请重写以下这段属于『{subtitle_title}』小节的内容：\n"
            f"```text\n"
            f"{current_content}\n"
            f"```\n\n"
            f"**重写指令**：{requirement_prompt}\n\n"
            f"**严格要求**：请只返回重写后的新内容段落（纯文本字符串），不要包含任何标题、JSON格式、引号、解释或其他多余文字。"
        )

        return [
            {"role": "system", "content": "你是一位顶级的政策研究和公文撰写专家，擅长在理解上下文的基础上，对具体段落进行深度优化、改写和扩写。"},
            {"role": "user", "content": user_content}
        ]


    @staticmethod
    def get_test_prompt() -> list[dict]:
        return [
            {"role": "user", "content": "你好"}
        ]
