import os
import json
import numpy as np
from tqdm import tqdm
from dotenv import load_dotenv
from openai import OpenAI
import xml.etree.ElementTree as ET

load_dotenv()

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
UPLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "vector_data"))
os.makedirs(UPLOADS_DIR, exist_ok=True)

API_KEY = os.getenv("EBD_API_KEY")
BASE_URL = os.getenv("EBD_BASE_URL")
MODEL_NAME = os.getenv("EBD_MODEL_NAME")
BATCH_SIZE = 10  # text-embedding-v4最大行数
MAX_LEN = 8182   # text-embedding-v4最大字符数

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# 1. 收集所有文本和元数据
file_infos = []
texts = []

for category in os.listdir(DATA_DIR):
    category_path = os.path.join(DATA_DIR, category)
    if not os.path.isdir(category_path):
        continue
    for fname in os.listdir(category_path):
        if not fname.endswith(".xml"):
            continue
        file_path = os.path.join(category_path, fname)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                xml_content = f.read()
            try:
                root = ET.fromstring(xml_content)
                import re
                # 只保留<Title>内容，忽略<Title_first>和<Title_second>
                def remove_space_between_chinese(s):
                    # 去除所有汉字之间的空格
                    return re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])', '', s)

                def extract_text(node):
                    # 忽略所有以 <Title_ 开头的节点及其内容
                    if node.tag.startswith("Title_"):
                        return ""
                    texts_list = []
                    # 当前节点文本
                    if node.text:
                        # 先去除汉字间空格
                        texts_list.append(remove_space_between_chinese(node.text))
                    # 递归子节点
                    for child in node:
                        child_text = extract_text(child)
                        if child_text:
                            texts_list.append(child_text)
                    # 尾部文本
                    if node.tail:
                        texts_list.append(remove_space_between_chinese(node.tail))
                    return " ".join(texts_list)
                text = extract_text(root).replace("\n", " ").strip()
                # 去除多余空格，只保留单个空格分隔
                text = ' '.join(text.split())
            except Exception as e:
                print(f"XML解析失败: {file_path}, {e}")
                text = xml_content.replace("\n", " ")
            # 截断超长文本
            if len(text) > MAX_LEN:
                text = text[:MAX_LEN]
            # print(f"\n解析内容: {text}") # uncmt iff testing
            if text.strip():
                texts.append(text)
                file_infos.append({
                    "category": category,
                    "name": fname,
                    "path": file_path
                })
        except Exception as e:
            print(f"处理文件出错: {file_path}，原因: {e}")



# 检查并打印空字符串（或全空白字符串）文本的文件
empty_text_files = []
for idx, text in enumerate(texts):
    if len(text.strip()) == 0:
        info = file_infos[idx]
        empty_text_files.append((info['name'], info['path']))
if empty_text_files:
    print("以下文件处理后文本为空字符串：")
    for name, path in empty_text_files:
        print(f"{name}: {path}")
else:
    print("所有文本均为非空字符串。")

# 检查并打印截断后仍大于8192字符的文件
overlong_files = []
for idx, text in enumerate(texts):
    if len(text) > 8192:
        info = file_infos[idx]
        overlong_files.append((info['name'], len(text), info['path']))
if overlong_files:
    print("以下文件截断后仍大于8192字符：")
    for name, length, path in overlong_files:
        print(f"{name} ({length} chars): {path}")
else:
    print("所有文本均不超过8192字符。")

print(f"共收集到 {len(texts)} 条文本，准备分批向量化...")

# 2. 分批调用 embedding 接口
all_embeddings = []
for i in tqdm(range(0, len(texts), BATCH_SIZE), desc="Batch embedding"):
    batch_texts = texts[i:i+BATCH_SIZE]
    batch_infos = file_infos[i:i+BATCH_SIZE]
    valid_texts = []
    valid_infos = []
    for t, info in zip(batch_texts, batch_infos):
        if isinstance(t, str) and 1 <= len(t) <= 8192:
            valid_texts.append(t)
            valid_infos.append(info)
        else:
            print(f"跳过不合法文本: {info['name']} ({len(t) if isinstance(t, str) else 'N/A'} chars) {info['path']}")
    if not valid_texts:
        continue
    try:
        completion = client.embeddings.create(
            model=MODEL_NAME,
            input=valid_texts,
            encoding_format="float"
        )
        # 兼容不同返回格式
        if hasattr(completion, "data"):
            batch_embeddings = [item.embedding for item in completion.data]
        else:
            batch_embeddings = [item["embedding"] for item in completion["data"]]
        all_embeddings.extend(batch_embeddings)
    except Exception as e:
        print("embedding请求异常，当前batch文件如下：")
        for info in valid_infos:
            print(f"  {info['name']} | {info['path']}")
        print(f"异常信息: {e}")
        raise

# 3. 保存向量
np.save(os.path.join(UPLOADS_DIR, "kb_vectors.npy"), np.array(all_embeddings, dtype=np.float32))
print(f"已保存 {len(all_embeddings)} 条知识库向量到 {UPLOADS_DIR}（text-embedding-v4，batch处理）")

# 4. 最后保存 file_infos
with open(os.path.join(UPLOADS_DIR, "kb_meta.json"), "w", encoding="utf-8") as f:
    json.dump(file_infos, f, ensure_ascii=False, indent=2)
print(f"已保存元数据到 {os.path.join(UPLOADS_DIR, 'kb_meta.json')}")



