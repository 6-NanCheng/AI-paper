本项目旨在构建一套集“文献抓取—智能筛选—数据存储—信息提取—成果展示”为一体的自动化文献管理系统。

其核心功能包括：

- 系统首先通过AI模型批量采集与特定主题相关的文献。 AI模型会对每篇文献进行关键字打分，进一步评估语义相关性，仅保留高关联度的文章。

- 高质量文献将被保存到zotero进行结构化存储和标签管理，确保文献信息完整有序。

- 系统通过调用AI大模型，从Zotero数据库中自动提取文献的关键信息并进行深入解读，并生成统一格式的Markdown文档。

- 利用Quarto渲染生成直观、阅读流畅的网页展示界面，为用户呈现极致的文献浏览体验。

```markdown
# 项目说明文档

本文档介绍项目的主要自动化任务及环境配置。所有任务均由 [Invoke](https://www.pyinvoke.org/) 管理，请先安装 `invoke`（命令：`pip install invoke`）。

---

## 环境配置

确保项目根目录下存在 `environment.yaml` 文件，其内容应类似如下（请替换占位符）：

```yaml
name: env.yml

Zotero_Storage: "C:/Path/To/Your/Zotero/Storage"   
Bai_Lian_API_KEY: "<your_bai_lian_api_key>"
Zotero_user_id: "<your_zotero_user_id>"
Zotero_API_KEY: "<your_zotero_api_key>"
Zotero_BASE_URL: "https://api.zotero.org"
```
配置项详细说明

name 创建和管理 Conda 环境时将使用的环境名称。

Zotero_Storage 指定 Zotero 存储目录的路径。确保路径有效并具有适当的访问权限。

Bai_Lian_API_KEY 用于调用 Bai_Lian API 的密钥。请替换为你自己的密钥。

Zotero_user_id 用于指定 Zotero 用户标识，便于访问对应的 Zotero 数据。

Zotero_API_KEY 用于鉴权 Zotero API 请求的密钥，请替换为正确的密钥值。

Zotero_BASE_URL Zotero API 的基础 URL。通常保持默认即可。
---

## 任务说明

`tasks.py` 中定义的自动化任务功能如下：

- **setup_env**  
  检查 `environment.yaml` 中的 `name` 字段，判断当前是否位于目标 Conda 环境中。若已在目标环境则直接返回；若环境存在但未激活，则提示你运行 `conda activate <env_name>`；若不存在，则使用命令 `conda env create -f environment.yaml` 自动创建环境。

- **run_paper**  
  运行 `paper.py` 脚本，处理与论文相关的操作。

- **run_zotero_update**  
  运行 `zotero_update.py` 脚本，用于更新 Zotero 数据或执行其它任务。

- **run_pdf2md**  
  运行 `pdf2md.py` 脚本，将 PDF 文件转换为 Markdown 格式，便于编辑和处理。

- **run_add2yml**  
  运行 `add2yml.py` 脚本，用于对 YAML 文件内容进行添加或更新。

- **run_quarto**  
  执行 `quarto render` 命令，渲染项目文档（前提：确保已安装并配置 Quarto）。

- **all**  
  按下列顺序依次执行：  
  1. `setup_env`  
  2. `run_zotero_update`  
  3. `run_pdf2md`  
  4. `run_add2yml`  
  5. `run_quarto`  
  执行完成后，终端会提示“所有任务执行完成！”。

---

## 如何运行任务

1. **打开终端**  
   - Windows 用户：使用命令提示符或 PowerShell。  

2. **进入项目目录**  
   切换到包含 `tasks.py` 的目录，例如：  
   ```bash
   cd /你的/项目/所在/目录
   ```

3. **执行任务**  
   根据需要运行以下命令：  
   - 创建/检查环境：  
     ```bash
     invoke setup_env
     ```
   - 运行处理论文脚本：  
     ```bash
     invoke run_paper
     ```
   - 或一次性执行所有任务：  
     ```bash
     invoke all
     ```

终端将显示详细的执行信息，请根据提示进行下一步操作。

---
