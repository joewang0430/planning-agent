from fastapi import APIRouter
import os

base_router = APIRouter()

KB_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../kb/data"))

@base_router.get("/kb/list")
def get_kb_list():
    # print("get_kb_list 路由被调用") 
    """
    Fintch scans the knowledge base directory and 
    returns all knowledge base files by folder classification
    return format:
    [
      {
        "category": "分类名",
        "files": [
          { "name": "文件名.xml", "type": "file" }
        ]
      },
      ...
    ]
    """
    kb_list = []
    # traverse category repos
    for category in os.listdir(KB_DATA_DIR):
        category_path = os.path.join(KB_DATA_DIR, category)
        if os.path.isdir(category_path):
            files = []
            for fname in os.listdir(category_path):
                if fname.endswith(".xml"):
                    files.append({"name": fname, "type": "file"})
            kb_list.append({"category": category, "files": files})
    return kb_list