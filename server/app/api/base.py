from fastapi import APIRouter, UploadFile, File
from fastapi import Request
from fastapi.responses import JSONResponse
import shutil
import os
from ..kb.utils import KnowledgeBase

base_router = APIRouter()

KB_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../kb/data"))
KB_UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../kb/uploads"))


# upload kb file
# if file with same name uploaded twice, later one will overcome the first
@base_router.post("/kb/upload")
async def upload_kb_file(file: UploadFile = File(...)):
    os.makedirs(KB_UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(KB_UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"success": True, "filename": file.filename}


# delete uploaded kb file
@base_router.post("/kb/delete")
async def delete_kb_file(request: Request):
    data = await request.json()
    filename = data.get("filename")
    file_path = os.path.join(KB_UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"success": True, "filename": filename}
    else:
        return JSONResponse(status_code=404, content={"success": False, "error": "File not found", "filename": filename})


# generate JSON of kb list, for front-end rendering
@base_router.get("/kb/list")
def router_get_kb_list():
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
    return KnowledgeBase.get_kb_list()