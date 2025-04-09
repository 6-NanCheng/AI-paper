import requests
import json
import os
import yaml

# 读取配置文件
def load_config():
    with open('env.yml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# 从配置文件中读取参数（使用 dict.get 提供默认值）
config = load_config()
ZOTERO_USER_ID = config.get('Zotero_user_id')
ZOTERO_API_KEY = config.get('Zotero_API_KEY')
ZOTERO_BASE_URL = config.get('Zotero_BASE_URL', 'https://api.zotero.org')  # 如果不存在则使用默认值

headers = {"Authorization": f"Bearer {ZOTERO_API_KEY}"}

# 1. 获取 Zotero 中的所有集合
def fetch_collections():
    url = f"{ZOTERO_BASE_URL}/users/{ZOTERO_USER_ID}/collections"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching collections: {e}")
        return []

# 2. 获取某个集合中的 PDF 文件
def fetch_pdf_items(collection_id):
    url = f"{ZOTERO_BASE_URL}/users/{ZOTERO_USER_ID}/collections/{collection_id}/items"
    params = {
        "format": "json",
        "include": "data",
        "limit": 100,
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        items = response.json()
        pdf_items = [
            item for item in items
            if item["data"].get("itemType") == "attachment" and 
               item["data"].get("contentType", "").startswith("application/pdf")
        ]
        return pdf_items
    except Exception as e:
        print(f"Error fetching PDF items for collection {collection_id}: {e}")
        return []

# 3. 获取当前状态（已有 PDF 文件）并返回
def fetch_current_state():
    if os.path.exists("zotero_state.json"):
        with open("zotero_state.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception as e:
                print("Error reading state file, starting with an empty state:", e)
                return {}
    return {}

# 4. 保存当前状态并打印实时状态（只打印关键结果）
def save_current_state(state):
    print(" 当前实时状态：")
    print(json.dumps(state, ensure_ascii=False, indent=4))
    with open("zotero_state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=4)
    print(" 当前状态已保存为 zotero_state.json")

# 5. 对比更新：只统计并打印新增的 PDF 项
def check_updates():
    collections = fetch_collections()
    previous_state = fetch_current_state()
    new_state = {}
    update_summary = {"新增": []}

    for collection in collections:
        collection_id = collection["key"]
        collection_name = collection["data"].get("name", "Unnamed Collection")
        pdf_items = fetch_pdf_items(collection_id)
        for pdf in pdf_items:
            item_key = pdf["data"].get("key")
            new_state[item_key] = {"collection": collection_name}
            # 如果该 PDF 不在之前状态中，则视为新增项
            if item_key not in previous_state:
                update_summary["新增"].append({item_key: {"collection": collection_name}})
                
    print(" 更新信息统计：")
    print(f"新增：{len(update_summary['新增'])}")
    if update_summary["新增"]:
        print("详细新增项目：")
        for item in update_summary["新增"]:
            print(item)
    
    # 保存新的实时状态
    save_current_state(new_state)
    return update_summary

# 主函数：运行更新检查并保存更新信息
if __name__ == "__main__":
    update_summary = check_updates()
    with open("zotero_update_summary.json", "w", encoding="utf-8") as f:
        json.dump(update_summary, f, ensure_ascii=False, indent=4)
    print(" 更新信息已保存为 zotero_update_summary.json")
