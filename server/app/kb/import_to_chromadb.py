import os
import json
import numpy as np
import chromadb
import shutil
from tqdm import tqdm

# --- 配置 ---
# 获取当前脚本所在的目录
# __file__ 是当前脚本的路径
# os.path.dirname(__file__) 是脚本所在的目录
# os.path.abspath() 将其转换为绝对路径
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 定义存放向量和元数据的目录
VECTOR_DATA_DIR = os.path.join(CURRENT_DIR, "vector_data")

# 定义 ChromaDB 持久化存储的目录
CHROMA_PERSIST_DIR = os.path.join(VECTOR_DATA_DIR, "chroma_db")

# 定义向量和元数据文件的完整路径
VECTORS_FILE = os.path.join(VECTOR_DATA_DIR, "kb_vectors.npy")
META_FILE = os.path.join(VECTOR_DATA_DIR, "kb_meta.json")

# 定义集合名称
COLLECTION_NAME = "planning_agent_kb"

# 定义批处理大小
BATCH_SIZE = 100

def import_to_chroma():
    """
    将生成的向量和元数据导入到 ChromaDB 中。
    """
    print("--- 开始导入数据到 ChromaDB ---")

    # --- 1. 检查源文件是否存在 ---
    if not os.path.exists(VECTORS_FILE) or not os.path.exists(META_FILE):
        print(f"[错误] 向量文件 '{VECTORS_FILE}' 或元数据文件 '{META_FILE}' 不存在。")
        print("请先运行 vectorization.py 脚本生成这些文件。")
        return

    # --- 2. 清理旧的数据库目录 (确保全新导入) ---
    if os.path.exists(CHROMA_PERSIST_DIR):
        print(f"发现旧的数据库目录 '{CHROMA_PERSIST_DIR}'，正在删除...")
        try:
            shutil.rmtree(CHROMA_PERSIST_DIR)
            print("旧目录已成功删除。")
        except OSError as e:
            print(f"[错误] 删除旧目录失败: {e}")
            return
    
    # --- 3. 加载数据 ---
    print("正在加载向量和元数据文件...")
    try:
        vectors = np.load(VECTORS_FILE)
        with open(META_FILE, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    except Exception as e:
        print(f"[错误] 加载文件失败: {e}")
        return

    # --- 4. 数据校验 ---
    if len(vectors) != len(metadata):
        print(f"[错误] 数据不匹配！向量数量 ({len(vectors)}) 与元数据记录数量 ({len(metadata)}) 不一致。")
        return
    
    print(f"加载成功！共 {len(vectors)} 条记录待导入。")

    # --- 5. 初始化 ChromaDB 客户端并创建集合 ---
    print(f"正在初始化持久化 ChromaDB 客户端，存储路径: '{CHROMA_PERSIST_DIR}'...")
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)

    print(f"正在创建或获取集合: '{COLLECTION_NAME}'...")
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    print(f"集合 '{COLLECTION_NAME}' 已准备就绪。当前集合中文档数: {collection.count()}")

    # --- 6. 准备数据并分批导入 ---
    # ChromaDB 要求 ID 是字符串类型
    ids = [f"doc_{i}" for i in range(len(metadata))]
    # ChromaDB 要求 embeddings 是 list of lists
    embeddings_list = vectors.tolist()

    print(f"准备分批导入数据，每批 {BATCH_SIZE} 条...")
    for i in tqdm(range(0, len(ids), BATCH_SIZE), desc="Importing to ChromaDB"):
        batch_ids = ids[i:i+BATCH_SIZE]
        batch_embeddings = embeddings_list[i:i+BATCH_SIZE]
        batch_metadata = metadata[i:i+BATCH_SIZE]
        
        try:
            collection.add(
                ids=batch_ids,
                embeddings=batch_embeddings,
                metadatas=batch_metadata
            )
        except Exception as e:
            print(f"\n[错误] 在导入批次 {i//BATCH_SIZE + 1} 时发生错误: {e}")
            # 可以选择在这里停止或继续
            return

    # --- 7. 最终验证 ---
    final_count = collection.count()
    print(f"\n--- 导入完成 ---")
    print(f"集合 '{COLLECTION_NAME}' 中最终的文档数量: {final_count}")

    if final_count == len(ids):
        print("[成功] 所有数据已成功导入！")
    else:
        print(f"[警告] 数据可能未完全导入，预期 {len(ids)} 条，实际 {final_count} 条。")

if __name__ == "__main__":
    import_to_chroma()
