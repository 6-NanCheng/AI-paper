import os
import json
import yaml
from pathlib import Path
from openai import OpenAI

# ========== 步骤 1：读取配置 ==========
with open("env.yml", "r", encoding="utf-8") as file:
    env_config = yaml.safe_load(file)

Bai_Lian_API_KEY = env_config.get("Bai_Lian_API_KEY")
Zotero_Storage = env_config.get("Zotero_Storage")

if not Bai_Lian_API_KEY:
    raise ValueError("API Key 未正确读取，请检查 env.yml 文件！")

if not os.path.exists(Zotero_Storage):
    raise FileNotFoundError(f"Zotero_Storage 路径 {Zotero_Storage} 不存在！")

# ========== 步骤 2：设置客户端 ==========
client = OpenAI(
    api_key=Bai_Lian_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ========== 步骤 3：定义 prompt 模板 ==========
PROMPT_TEMPLATE = """请按照以下步骤对文献进行深入解读和分析，确保结果逻辑清晰、内容全面：
# 此处替换为文章标题

## 基本信息提取

提取作者、发表年份、期刊名称等关键信息。

## 研究背景与目的

总结文献的研究背景，说明研究所解决的问题或提出的假设。
明确指出作者的研究目的和研究动机。

## 研究方法

描述作者采用的研究方法（如实验、调查、建模、定量/定性分析等）。
解释数据来源、采集方式以及实验设计或分析框架。
分析所选方法的优势和可能存在的局限性。

## 主要发现与结果

概述文章的核心发现和关键数据。
对图表、统计数据和实验结果进行总结和分析。
强调研究结果对原始问题的解答和新发现。

## 讨论与结论

分析作者如何讨论结果及其对研究领域的影响。
总结文章的结论，并指出研究局限性、未解决的问题或作者提出的未来研究方向。

## 创新点与贡献

指出文献在理论、方法或实践方面的创新与独特贡献。
讨论该研究如何推动领域的发展，及其实际应用意义。

## 个人评价与启示

提出对文献整体质量、方法合理性和结果可信度的评价。
指出文献中的不足或存在争议之处。
给出自己对相关领域未来研究的建议和启示。

请确保在解读过程中：
语言表达准确、逻辑清晰；
分析内容既关注整体框架也注意细节；
引用和解释关键概念和数据时要做到充分且有条理。

注意：在输出列表的时候，需要再列表头与列表项之间加入两个空行（换行符），否则Quarto渲染时候会出错。
"""

# ========== 核心函数：pdf2md ==========
def pdf2md():
    # 读取 json 文件
    with open("zotero_update_summary.json", "r", encoding="utf-8") as f:
        summary = json.load(f)

    # 创建 md 输出目录
    md_output_dir = os.path.join(os.getcwd(), "md")
    os.makedirs(md_output_dir, exist_ok=True)

    # 处理新增项
    for entry in summary.get("新增", []):
        for folder_name in entry:
            folder_path = os.path.join(Zotero_Storage, folder_name)
            if not os.path.exists(folder_path):
                print(f" 文件夹不存在：{folder_path}")
                continue

            # 查找 PDF 文件
            pdf_files = [
                os.path.join(folder_path, f)
                for f in os.listdir(folder_path)
                if f.lower().endswith(".pdf")
            ]
            if not pdf_files:
                print(f" 未找到 PDF 文件：{folder_path}")
                continue

            pdf_path = pdf_files[0]
            print(f"\n 开始处理：{folder_name}")

            # 上传 PDF 文件
            try:
                file_obj = client.files.create(file=Path(pdf_path), purpose="file-extract")
                file_id = file_obj.id
                print(f" file-id：{file_id}")
            except Exception as e:
                print(f" 上传失败：{pdf_path}，错误：{e}")
                continue

            # 发送解析请求
            print(" 正在发送请求解析文档...")
            try:
                completion = client.chat.completions.create(
                    model="qwen-long",
                    messages=[
                        {"role": "system", "content": f"fileid://{file_id}"},
                        {'role': 'user', 'content': PROMPT_TEMPLATE},
                    ],
                    temperature=0.2,
                )
                full_content = completion.choices[0].message.content
            except Exception as e:
                print(f" 解析失败：{folder_name}，错误：{e}")
                continue

            # 保存为 Markdown
            md_path = os.path.join(md_output_dir, f"{folder_name}.md")
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(full_content)

            print(f" 解析成功并保存为 Markdown：{md_path}")

# ========== 启动 ==========
if __name__ == "__main__":
    pdf2md()
