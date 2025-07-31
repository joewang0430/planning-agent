from pydantic import BaseModel
from typing import List, Optional

# For /api/classify_title
class ClassifyTitleRequest(BaseModel):
    title: str
    
class ClassifyTitleReturn(BaseModel):
    valid: bool

# For /api/outline
class KnowledgeBaseFile(BaseModel):
    name: str
    type: str 
    category: Optional[str] = None

class GenerateOutlineRequest(BaseModel):
    title: str
    selectedKbList: List[KnowledgeBaseFile]

class GenerateOutlineReturn(BaseModel):
    success: bool
    title: str
    outline: str
    policy: str
    kb_list: List[KnowledgeBaseFile]

# For /api/content
class GenerateContentRequest(BaseModel):
    title: str
    outline: str
    context: str

class GenerateContentReturn(BaseModel):
    success: bool = True
    title: str
    content: dict | str # accept dict for content_outline, or str for error message

# For /api/rewrite/outline
class RewriteOutlineRequest(BaseModel):
    title: str
    context: str

class RewriteOutlineReturn(BaseModel):
    success: bool
    title: str
    outline: str

# For rewriting a subtitle
class RewriteSubtitleRequest(BaseModel):
    plan_title: str
    full_outline: list
    parent_title: str
    current_subtitle: str
    context: str
    user_requirement: Optional[str] = ""

class RewriteSubtitleReturn(BaseModel):
    success: bool = True
    new_title: str

# For rewriting a section
class RewriteSectionRequest(BaseModel):
    plan_title: str
    full_outline: list
    current_section: dict
    policy_context: str
    user_requirement: Optional[str] = ""

class RewriteSectionReturn(BaseModel):
    success: bool = True
    new_section: dict