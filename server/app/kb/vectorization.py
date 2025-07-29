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
APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.makedirs(UPLOADS_DIR, exist_ok=True)

API_KEY = os.getenv("EBD_API_KEY")
BASE_URL = os.getenv("EBD_BASE_URL")
MODEL_NAME = os.getenv("EBD_MODEL_NAME")
BATCH_SIZE = 10  # text-embedding-v4 max line num
MAX_LEN = 8182   # text-embedding-v4 max character num

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# 1. Collect all the text and metadata
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
                # Only maintain <Title>，ignore <Title_first> and <Title_second>
                def remove_space_between_chinese(s):
                    # remove the Spaces between Chinese characters
                    return re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])', '', s)

                def extract_text(node):
                    # Ignore all nodes starting with <Title_ and their contents
                    if node.tag.startswith("Title_"):
                        return ""
                    texts_list = []
                    # Current node text
                    if node.text:
                        # remove the Spaces between Chinese characters, this is severely important!
                        texts_list.append(remove_space_between_chinese(node.text))
                    # Recursive child nodes
                    for child in node:
                        child_text = extract_text(child)
                        if child_text:
                            texts_list.append(child_text)
                    # tail text
                    if node.tail:
                        texts_list.append(remove_space_between_chinese(node.tail))
                    return " ".join(texts_list)
                text = extract_text(root).replace("\n", " ").strip()
                # Remove the extra Spaces and keep only a single space for separation
                text = ' '.join(text.split())
            except Exception as e:
                print(f"XML解析失败: {file_path}, {e}")
                text = xml_content.replace("\n", " ")
            # Truncate extremely long text
            if len(text) > MAX_LEN:
                text = text[:MAX_LEN]
            # print(f"\n解析内容: {text}") # uncmt iff testing
            if text.strip():
                texts.append(text)
                relative_path = os.path.relpath(file_path, APP_ROOT)
                file_infos.append({
                    "category": category,
                    "name": fname,
                    "path": f"/{relative_path}",
                    "text": text
                })
        except Exception as e:
            print(f"处理文件出错: {file_path}，原因: {e}")


# TODO: delete it 
# A file that checks and prints the text of an empty string (or a completely blank string)
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

# TODO: delete it 
# Check and print files that still exceed MAX_LEN characters after truncation
overlong_files = []
for idx, text in enumerate(texts):
    if len(text) > MAX_LEN:
        info = file_infos[idx]
        overlong_files.append((info['name'], len(text), info['path']))
if overlong_files:
    print("以下文件截断后仍大于8192字符：")
    for name, length, path in overlong_files:
        print(f"{name} ({length} chars): {path}")
else:
    print("所有文本均不超过8192字符。")

print(f"共收集到 {len(texts)} 条文本，准备分批向量化...")

# 2. Call the embedding interface in batches
all_embeddings = []
for i in tqdm(range(0, len(texts), BATCH_SIZE), desc="Batch embedding"):
    batch_texts = texts[i:i+BATCH_SIZE]
    batch_infos = file_infos[i:i+BATCH_SIZE]
    valid_texts = []
    valid_infos = []
    for t, info in zip(batch_texts, batch_infos):
        if isinstance(t, str) and 1 <= len(t) <= MAX_LEN:
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
        # Compatible with different return formats
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

# 3. Save vector
np.save(os.path.join(UPLOADS_DIR, "kb_vectors.npy"), np.array(all_embeddings, dtype=np.float32))
print(f"已保存 {len(all_embeddings)} 条知识库向量到 {UPLOADS_DIR}（text-embedding-v4，batch处理）")

# 4. Finally save file_infos
with open(os.path.join(UPLOADS_DIR, "kb_meta.json"), "w", encoding="utf-8") as f:
    json.dump(file_infos, f, ensure_ascii=False, indent=2)
print(f"已保存元数据到 {os.path.join(UPLOADS_DIR, 'kb_meta.json')}")



