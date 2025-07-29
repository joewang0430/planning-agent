import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from utils import KnowledgeBase

load_dotenv()

# API config (must be same with vectorization.py)
API_KEY = os.getenv("EBD_API_KEY")
BASE_URL = os.getenv("EBD_BASE_URL")
MODEL_NAME = os.getenv("EBD_MODEL_NAME")

# ChromaDB config (must be same with import_to_chromadb.py)
VECTOR_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "vector_data"))
CHROMA_PERSIST_DIR = os.path.join(VECTOR_DATA_DIR, "chroma_db")
COLLECTION_NAME = "planning_agent_kb"

def query_chroma_db(query_text: str, n_results: int = 5):
    """
    使用给定的文本查询 ChromaDB，并返回最相似的结果。
    """
    print("--- 开始执行 ChromaDB 相似度查询 ---")

    # check if repo exists
    if not os.path.exists(CHROMA_PERSIST_DIR):
        print(f"[错误] 数据库目录 '{CHROMA_PERSIST_DIR}' 不存在。")
        print("请先运行 import_to_chromadb.py 脚本创建数据库。")
        return

    # connect to persistent ChromaDB
    print(f"正在从 '{CHROMA_PERSIST_DIR}' 加载数据库...")
    try:
        db_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        collection = db_client.get_collection(name=COLLECTION_NAME)
        print(f"成功连接到集合 '{COLLECTION_NAME}'，其中包含 {collection.count()} 条记录。")
    except Exception as e:
        print(f"[错误] 连接或获取集合失败: {e}")
        return

     # generate embedding for query text
    print(f"\n正在为查询文本生成 embedding: '{query_text}'")
    query_embedding = KnowledgeBase.get_embedding(query_text)
    if query_embedding is None:
        print("[错误] 调用 embedding API 失败。")
        return
    print("Embedding 生成成功。")

    # implement query
    print(f"正在数据库中查询 {n_results} 个最相似的结果...")
    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["metadatas", "documents", "distances"] # ensure return documents
        )
    except Exception as e:
        print(f"[错误] 执行查询时出错: {e}")
        return

    # print solution
    print("\n--- 查询结果 ---")
    if not results or not results.get('ids') or not results['ids'][0]:
        print("未找到相关结果。")
        return

    for i, doc_id in enumerate(results['ids'][0]):
        distance = results['distances'][0][i]
        metadata = results['metadatas'][0][i]
        # documents returned from ChromaDB might be None，although already included
        document = (results['documents'][0][i] if results.get('documents') and results['documents'][0] else "N/A") or "N/A"
        
        print(f"\n--- Top {i+1} ---")
        print(f"  ID:       {doc_id}")
        print(f"  距离:     {distance:.4f} (越小越相似)")
        print(f"  文件名:   {metadata.get('name', 'N/A')}")
        print(f"  类别:     {metadata.get('category', 'N/A')}")
        # only print partial doc content for simplicity
        print(f"  内容预览: {document[:200]}...")

if __name__ == "__main__":
    query = "杭州市城市轨道交通网络‘十五五’发展专项规划（2021-2025年）"
    query_chroma_db(query_text=query)
