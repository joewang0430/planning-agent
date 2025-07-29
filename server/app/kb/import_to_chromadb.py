import os
import json
import numpy as np
import chromadb
import shutil
from tqdm import tqdm

# os.path.dirname(__file__) is the depo where script exists
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the directory for storing vectors and metadata
VECTOR_DATA_DIR = os.path.join(CURRENT_DIR, "vector_data")

# Define the directory for persistent storage of ChromaDB
CHROMA_PERSIST_DIR = os.path.join(VECTOR_DATA_DIR, "chroma_db")

# Define the complete paths of vector and metadata files
VECTORS_FILE = os.path.join(VECTOR_DATA_DIR, "kb_vectors.npy")
META_FILE = os.path.join(VECTOR_DATA_DIR, "kb_meta.json")

# Define the collection name
COLLECTION_NAME = "planning_agent_kb"

# Define the batch size
BATCH_SIZE = 100

def import_to_chroma():
    """
    Import the generated vectors and metadata into ChromaDB.
    """
    print("--- 开始导入数据到 ChromaDB ---")

    # Check whether the source file exists
    if not os.path.exists(VECTORS_FILE) or not os.path.exists(META_FILE):
        print(f"[错误] 向量文件 '{VECTORS_FILE}' 或元数据文件 '{META_FILE}' 不存在。")
        print("请先运行 vectorization.py 脚本生成这些文件。")
        return

    # Clean up the old database directory (make sure it is newly imported)
    if os.path.exists(CHROMA_PERSIST_DIR):
        print(f"发现旧的数据库目录 '{CHROMA_PERSIST_DIR}'，正在删除...")
        try:
            shutil.rmtree(CHROMA_PERSIST_DIR)
            print("旧目录已成功删除。")
        except OSError as e:
            print(f"[错误] 删除旧目录失败: {e}")
            return
    
    # load data
    print("正在加载向量和元数据文件...")
    try:
        vectors = np.load(VECTORS_FILE)
        with open(META_FILE, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    except Exception as e:
        print(f"[错误] 加载文件失败: {e}")
        return

    # data check
    if len(vectors) != len(metadata):
        print(f"[错误] 数据不匹配！向量数量 ({len(vectors)}) 与元数据记录数量 ({len(metadata)}) 不一致。")
        return
    
    print(f"加载成功！共 {len(vectors)} 条记录待导入。")

    # Initialize the ChromaDB client and create the collection
    print(f"正在初始化持久化 ChromaDB 客户端，存储路径: '{CHROMA_PERSIST_DIR}'...")
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)

    print(f"正在创建或获取集合: '{COLLECTION_NAME}'...")
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    print(f"集合 '{COLLECTION_NAME}' 已准备就绪。当前集合中文档数: {collection.count()}")

    # Prepare the data and import it in batches
    # ChromaDB requires that the ID be of string type
    ids = [f"doc_{i}" for i in range(len(metadata))]
    # ChromaDB requires embeddings is list of lists
    embeddings_list = vectors.tolist()

    print(f"准备分批导入数据，每批 {BATCH_SIZE} 条...")
    for i in tqdm(range(0, len(ids), BATCH_SIZE), desc="Importing to ChromaDB"):
        batch_ids = ids[i:i+BATCH_SIZE]
        batch_embeddings = embeddings_list[i:i+BATCH_SIZE]
        batch_metadata = metadata[i:i+BATCH_SIZE]
        # Extract the original content of each item, assuming the metadata 
        # has a 'text' field; otherwise, it is an empty string
        batch_documents = [m.get("text", "") for m in batch_metadata]
        try:
            collection.add(
                ids=batch_ids,
                embeddings=batch_embeddings,
                metadatas=batch_metadata,
                documents=batch_documents
            )
        except Exception as e:
            print(f"\n[错误] 在导入批次 {i//BATCH_SIZE + 1} 时发生错误: {e}")
            # TODO: decide palse or continue later
            return

    # final varificaiton
    final_count = collection.count()
    print(f"\n--- 导入完成 ---")
    print(f"集合 '{COLLECTION_NAME}' 中最终的文档数量: {final_count}")

    if final_count == len(ids):
        print("[成功] 所有数据已成功导入！")
    else:
        print(f"[警告] 数据可能未完全导入，预期 {len(ids)} 条，实际 {final_count} 条。")

if __name__ == "__main__":
    import_to_chroma()
