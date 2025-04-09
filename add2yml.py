import yaml
import json
import os

# 路径配置
YML_PATH = "_quarto.yml"
STATE_PATH = "zotero_state.json"
MD_FOLDER = "md"  # md 文件夹

# 读取 _quarto.yml
with open(YML_PATH, "r", encoding="utf-8") as f:
    yml_data = yaml.safe_load(f)

# 确保 book 部分及 chapters 存在
yml_data.setdefault("book", {}).setdefault("chapters", [])

# 读取 zotero_state.json
with open(STATE_PATH, "r", encoding="utf-8") as f:
    zotero_state = json.load(f)

# 建立 collection -> [md 文件相对路径] 映射
collection_map = {}
for md_filename in os.listdir(MD_FOLDER):
    if md_filename.endswith(".md"):
        stem = os.path.splitext(md_filename)[0]  # 去掉 .md 后缀
        if stem in zotero_state:
            collection = zotero_state[stem]["collection"]
            # 将相对路径构造为："md/xxx.md"
            md_path = f"{MD_FOLDER}/{md_filename}"
            collection_map.setdefault(collection, []).append(md_path)

# 更新 yml_data，插入 md 文件到对应的 part 下
for collection, md_files in collection_map.items():
    # 查找是否已有对应的 part
    part_exists = False
    for item in yml_data["book"]["chapters"]:
        if isinstance(item, dict) and item.get("part") == collection:
            part_exists = True
            # 如果已有 part，直接插入新章节（避免重复）
            for md_file in md_files:
                if md_file not in item["chapters"]:
                    item["chapters"].append(md_file)
            break

    # 如果没有对应的 part，则创建新的 part 和章节
    if not part_exists:
        new_part = {"part": collection, "chapters": md_files}
        yml_data["book"]["chapters"].append(new_part)

# 写回 _quarto.yml，确保新的内容仅添加到 book 部分的 chapters 下
with open(YML_PATH, "w", encoding="utf-8") as f:
    yaml.dump(yml_data, f, allow_unicode=True, sort_keys=False)

print("✅ _quarto.yml 文件已成功更新！")
