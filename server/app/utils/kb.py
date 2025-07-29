import os

MAX_KB_NUM = 6  # max 6 knowledgebase each generation
USER_MAX_KB_NUM = 5 # max 5 knowledgebase for user to select

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
                        files.append({"name": fname, "type": "file"})
                kb_list.append({"category": category, "files": files})
        return kb_list
    
    @staticmethod
    def get_ai_kb_num(selected_kb):
        def get_ai_kb_num(selected_kb):
            # calculate the number of selected knowledge bases (including user uploads)
            used_num = len(selected_kb)
            remain_num = MAX_KB_NUM - used_num
            return remain_num
    
    @staticmethod
    def exclude_kb_list(lst, selected_kb):
        # build the selected collection {(category, name)}
        selected_set = set(
            (kb["category"], kb["name"]) for kb in selected_kb
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
    

# test functionality
if __name__ == "__main__":
    all_kb_list = [
        {
            "category": "组织机构",
            "files": [
                {"name": "A.xml", "type": "file"},
                {"name": "B.xml", "type": "file"},
            ]
        },
        {
            "category": "国土能源",
            "files": [
                {"name": "C.xml", "type": "file"},
            ]
        }
    ]
    # mocke selected kb
    selected_kb = [
        {"name": "A.xml", "type": "file", "category": "组织机构"},
        {"name": "C.xml", "type": "file", "category": "国土能源"},
    ]
    # test exclude_kb_list
    filtered_kb_list = KnowledgeBase.exclude_kb_list(all_kb_list, selected_kb)
    print(filtered_kb_list)
    # expected：[{'category': '组织机构', 'files': [{'name': 'B.xml', 'type': 'file'}]}]