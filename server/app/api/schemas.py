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

