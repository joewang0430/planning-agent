import os
import chromadb
from dotenv import load_dotenv
from app.ai.agent import EmbeddingAgent

load_dotenv()

# API config (must be same with vectorization.py)
API_KEY = os.getenv("EBD_API_KEY")
BASE_URL = os.getenv("EBD_BASE_URL")
MODEL_NAME = os.getenv("EBD_MODEL_NAME")

# ChromaDB config (must be same with import_to_chromadb.py)
VECTOR_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "vector_data"))
CHROMA_PERSIST_DIR = os.path.join(VECTOR_DATA_DIR, "chroma_db")
COLLECTION_NAME = "planning_agent_kb"

class Query:
    def __init__(self):
        """
        Initialize the query class and connect to ChromaDB.
        """
        print("--- 初始化 ChromaDB 连接 ---")
        if not os.path.exists(CHROMA_PERSIST_DIR):
            raise FileNotFoundError(f"数据库目录 '{CHROMA_PERSIST_DIR}' 不存在。请先运行 import_to_chromadb.py。")
        
        try:
            self.embedding_agent = EmbeddingAgent()
            db_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
            self.collection = db_client.get_collection(name=COLLECTION_NAME)
            print(f"成功连接到集合 '{COLLECTION_NAME}'，其中包含 {self.collection.count()} 条记录。")
        except Exception as e:
            print(f"[错误] 连接或获取集合失败: {e}")
            raise

    def query_relevant(self, query_text: str, n_results: int = 5):
        """
        Query ChromaDB using the given text and return a list of ids with the most similar results.
        """
        print(f"\n--- 开始为查询 '{query_text}' 执行相似度查询 ---")

        # Generate the embedding of the query text
        print("正在生成查询 embedding...")
        query_embedding = self.embedding_agent.get_embedding(query_text)
        if query_embedding is None:
            print("[错误] 调用 embedding API 失败。")
            return []
        print("Embedding 生成成功。")

        # execute query
        print(f"正在数据库中查询 {n_results} 个最相似的结果...")
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=[]  # Only get the ID, no other information is needed
            )
        except Exception as e:
            print(f"[错误] 执行查询时出错: {e}")
            return []

        # Extract and return the ID
        if not results or not results.get('ids') or not results['ids'][0]:
            print("未找到相关结果。")
            return []
        
        doc_ids = results['ids'][0]
        print(f"查询成功，找到 {len(doc_ids)} 个相关文档 ID。")
        return doc_ids


# test
if __name__ == "__main__":
    try:
        query_agent = Query()
        query = "杭州市城市轨道交通网络‘十五五’发展专项规划（2021-2025年）"
        relevant_ids = query_agent.query_relevant(query_text=query, n_results=5)
        
        if relevant_ids:
            print("\n--- 查询返回的文档 ID 列表 ---")
            print(relevant_ids)
        else:
            print("\n--- 未返回任何文档 ID ---")

    except Exception as e:
        print(f"\n[主程序错误] {e}")
