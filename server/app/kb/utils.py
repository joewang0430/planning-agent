import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List
from ..api.schemas import KnowledgeBaseFile

load_dotenv()

API_KEY = os.getenv("EBD_API_KEY")
BASE_URL = os.getenv("EBD_BASE_URL")
MODEL_NAME = os.getenv("EBD_MODEL_NAME")

MAX_KB_NUM = 6  # max 6 kb each generation
USER_MAX_KB_NUM = 5 # max 5 kb for user to select

KB_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../kb/data"))

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
    
    @staticmethod # TODO: change it later
    def get_content_from_bf(bf: KnowledgeBaseFile) -> str:
        """
        Reads and returns the content of a knowledge base file.
        """
        return ""

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
    print("\nExpected output:")
    print("[{'category': '组织机构', 'files': [{'name': 'B.xml', 'type': 'file'}]}, {'category': '国土能源', 'files': [{'name': 'C.xml', 'type': 'file'}, {'name': 'D.xml', 'type': 'file'}]}]")