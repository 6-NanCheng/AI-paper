本项目旨在构建一套集“文献抓取—智能筛选—数据存储—信息提取—成果展示”为一体的自动化文献管理系统。

其核心功能包括：

- 系统首先通过AI模型批量采集与特定主题相关的文献。 AI模型会对每篇文献进行关键字打分，进一步评估语义相关性，仅保留高关联度的文章。

- 高质量文献将被保存到zotero进行结构化存储和标签管理，确保文献信息完整有序。

- 系统通过调用AI大模型，从Zotero数据库中自动提取文献的关键信息并进行深入解读，并生成统一格式的Markdown文档。

- 利用Quarto渲染生成直观、阅读流畅的网页展示界面，为用户呈现极致的文献浏览体验。

# 项目说明文档

本文档介绍了本项目的主要自动化任务，所有任务均通过 [Invoke](https://www.pyinvoke.org/) 工具管理。**请确保在运行前已安装 `invoke`。**

pip install invoke

## 任务说明

### setup_env
- **功能**：从 `environment.yaml` 中读取 `name` 字段，获取目标 Conda 环境名称，并检查当前环境状态。
- **操作流程**：
  - 如果已处于目标环境中，则直接返回；
  - 如果目标环境已存在，则提示用户手动激活该环境；
  - 如果目标环境不存在，则自动使用 `conda env create -f environment.yaml` 命令创建新的环境。

### run_paper
- **功能**：运行 `paper.py` 脚本，处理与论文相关的操作。

### run_zotero_update
- **功能**：运行 `zotero_update.py` 脚本，用于更新 Zotero 数据或其他相关任务。

### run_pdf2md
- **功能**：运行 `pdf2md.py` 脚本，将 PDF 文件转换为 Markdown 格式。

### run_add2yml
- **功能**：运行 `add2yml.py` 脚本，处理 YAML 文件的内容添加或更新。

### run_quarto
- **功能**：调用 `quarto render` 命令，对项目相关文档进行渲染。
- **注意**：确保已正确安装 Quarto。

### all
- **功能**：依次执行以下任务：
  1. `setup_env`
  2. `run_zotero_update`
  3. `run_pdf2md`
  4. `run_add2yml`
  5. `run_quarto`
- **提示**：所有任务执行完毕后，会输出“所有任务执行完成！”的提示信息。

## 使用方法

在终端中，通过 `invoke` 命令执行对应任务。例如：
```bash
invoke setup_env
invoke run_paper
invoke all

