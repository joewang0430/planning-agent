import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List
from ..api.schemas import KnowledgeBaseFile
import chromadb
from .import_to_chromadb import CHROMA_PERSIST_DIR, COLLECTION_NAME
import docx


load_dotenv()

API_KEY = os.getenv("EBD_API_KEY")
BASE_URL = os.getenv("EBD_BASE_URL")
MODEL_NAME = os.getenv("EBD_MODEL_NAME")

MAX_KB_NUM = 6  # max 6 kb each generation
USER_MAX_KB_NUM = 5 # max 5 kb for user to select

KB_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../kb/data"))
KB_UPLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../kb/uploads"))

MAX_CHAR_NUM = 950

class KnowledgeBase:
    @staticmethod
    def get_kb_list():
        kb_list = []
        for category in os.listdir(KB_DATA_DIR):
            category_path = os.path.join(KB_DATA_DIR, category)
            if os.path.isdir(category_path):
                files = []
                for fname in os.listdir(category_path):
                    if fname.endswith(".xml"):
                        files.append({"name": fname, "type": "db"})
                kb_list.append({"category": category, "files": files})
        return kb_list
    
    @staticmethod
    def bf_to_id(bf:KnowledgeBaseFile) -> str:
        """
        Converts a KnowledgeBaseFile object to a string ID if its type is 'db'.
        Format: "category/name"
        Returns an empty string if the type is not 'db'.
        """
        if bf.type == "db":
            return f"{bf.category}/{bf.name}"
        return ""
    
    @staticmethod
    def bf_to_id_lst(bf_lst: List[KnowledgeBaseFile]) -> List[str]:
        """
        Converts a list of KnowledgeBaseFile objects to a list of string IDs,
        only including items where type is 'db'.
        Format: "category/name"
        """
        return [f"{bf.category}/{bf.name}" for bf in bf_lst if bf.type == "db"]
    
    @staticmethod
    def bf_get_file(bf_lst: List[KnowledgeBaseFile]) -> List[KnowledgeBaseFile]:
        """
        Extracts items with type 'file' from a list of KnowledgeBaseFile objects.
        """
        return [bf for bf in bf_lst if bf.type == "file"]

    @staticmethod
    def bf_get_db(bf_lst: List[KnowledgeBaseFile]) -> List[KnowledgeBaseFile]:
        """
        Extracts items with type 'db' from a list of KnowledgeBaseFile objects.
        """
        return [bf for bf in bf_lst if bf.type == "db"]
    
    @staticmethod
    def get_ai_kb_num(selected_kb):
        '''
        this function says: how many kb should ai gonna find
        '''
        # calculate the number of selected knowledge bases (including user uploads)
        used_num = len(selected_kb)
        remain_num = MAX_KB_NUM - used_num
        return remain_num
    
    @staticmethod
    def exclude_kb_list(lst, selected_kb):
        '''
        this function is used for re-getting all the kbs but except user-selected
        '''
        # build the selected collection {(category, name)} for items with type 'db'
        selected_set = set(
            (kb["category"], kb["name"]) for kb in selected_kb if kb.get("type") == "db"
        )
        new_lst = []
        for cat in lst:
            # Filter out the selected files
            new_files = [
                f for f in cat["files"]
                if (cat["category"], f["name"]) not in selected_set
            ]
            # Only the categories with remaining files are retained
            if new_files:
                new_lst.append({
                    "category": cat["category"],
                    "files": new_files
                })
        return new_lst
    
    @staticmethod
    def id_to_bf(id_str: str) -> KnowledgeBaseFile:
        """
        Converts a string ID back to a KnowledgeBaseFile object.
        ID Format: "category/name"
        """
        parts = id_str.split('/', 1)
        category = parts[0]
        name = parts[1]
        return KnowledgeBaseFile(name=name, type="db", category=category)

    @staticmethod
    def id_to_bf_lst(id_lst: List[str]) -> List[KnowledgeBaseFile]:
        """
        Converts a list of string IDs back to a list of KnowledgeBaseFile objects.
        """
        return [KnowledgeBase.id_to_bf(id_str) for id_str in id_lst]
    
    @staticmethod
    def get_all_kb_content(bf_lst: List[KnowledgeBaseFile]) -> List[str]:
        """
        Retrieves the content for a list of KnowledgeBaseFile objects.
        - For 'db' type, it fetches content from ChromaDB by ID.
        - For 'file' type, it reads the content from the local file system.
        - All content is truncated to MAX_CHAR_NUM characters.
        """
        contents = []
        
        # Initialize ChromaDB client
        try:
            db_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
            collection = db_client.get_collection(name=COLLECTION_NAME)
        except Exception as e:
            print(f"Error initializing ChromaDB: {e}")
            # Return empty content for all if DB fails
            return [""] * len(bf_lst)

        for bf in bf_lst:
            content = ""
            try:
                if bf.type == 'db':
                    doc_id = KnowledgeBase.bf_to_id(bf)
                    if doc_id:
                        # Fetch from ChromaDB
                        result = collection.get(ids=[doc_id], include=["documents"])
                        if result and result.get('documents'):
                            content = result['documents'][0]
                        else:
                            print(f"Warning: Document with ID '{doc_id}' not found in ChromaDB.")
                
                elif bf.type == 'file':
                    # User upload files has no category
                    file_path = os.path.join(KB_UPLOADS_DIR, bf.name)
                    if os.path.exists(file_path):
                        # --- File classify starts ---
                        if bf.name.endswith('.docx'):
                            # If it is a.docx file, read it using python-docx
                            try: 
                                doc = docx.Document(file_path)
                                full_text = [para.text for para in doc.paragraphs]
                                content = '\n'.join(full_text)
                            except Exception as e:
                                print(f"Error reading .docx file '{bf.name}': {e}")
                                content = ""
                        else:
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                            except UnicodeDecodeError:
                                print(f"Warning: Could not decode file '{bf.name}' as utf-8.")
                                content = f"Non-text file content for {bf.name} is not displayed."
                        # --- File classify ends ---
                    else:
                        print(f"Warning: File not found at '{file_path}'.")

            except Exception as e:
                print(f"Error processing '{bf.name}': {e}")
                content = "" # Ensure content is empty on error

            # Truncate content if it exceeds the maximum length
            if len(content) > MAX_CHAR_NUM:
                content = content[:MAX_CHAR_NUM]
            
            contents.append(content)
            
        return contents

# test functionality
if __name__ == "__main__":
    all_kb_list = [
        {
            "category": "组织机构",
            "files": [
                {"name": "A.xml", "type": "db"},
                {"name": "B.xml", "type": "db"},
            ]
        },
        {
            "category": "国土能源",
            "files": [
                {"name": "C.xml", "type": "db"},
                {"name": "D.xml", "type": "db"},
            ]
        }
    ]
    # mock selected kb
    selected_kb = [
        # This item has type 'db', so it should be excluded from the list.
        {"name": "A.xml", "type": "db", "category": "组织机构"},
        # This item also has type 'db', so it should also be excluded.
        {"name": "C.xml", "type": "db", "category": "国土能源"},
    ]
    # test exclude_kb_list
    print("Testing exclude_kb_list function...")
    filtered_kb_list = KnowledgeBase.exclude_kb_list(all_kb_list, selected_kb)
    print("Filtered list:")
    print(filtered_kb_list)
    # ...
    print("\nExpected output:")
    print("[{'category': '组织机构', 'files': [{'name': 'B.xml', 'type': 'db'}]}, {'category': '国土能源', 'files': [{'name': 'D.xml', 'type': 'db'}]}]")
