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
