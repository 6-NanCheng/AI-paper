本项目旨在构建一套集“文献抓取—智能筛选—数据存储—信息提取—成果展示”为一体的自动化文献管理系统。

其核心功能包括：

- 系统首先通过AI模型批量采集与特定主题相关的文献。 AI模型会对每篇文献进行关键字打分，进一步评估语义相关性，仅保留高关联度的文章。

- 高质量文献将被保存到zotero进行结构化存储和标签管理，确保文献信息完整有序。

- 系统通过调用AI大模型，从Zotero数据库中自动提取文献的关键信息并进行深入解读，并生成统一格式的Markdown文档。

- 利用Quarto渲染生成直观、阅读流畅的网页展示界面，为用户呈现极致的文献浏览体验。


# 项目说明文档

本文档详细介绍了本项目中的自动化任务、环境配置要求以及如何使用这些任务。项目所有任务均由 [Invoke](https://www.pyinvoke.org/) 管理，适用于环境搭建、脚本运行和文档渲染。本文档旨在帮助初学者快速上手，全面了解各任务的流程和注意事项。

> **先决条件：安装 Invoke**  
> 在终端中运行以下命令以安装：
> ```bash
> pip install invoke pyyaml
> 
> ```

---

## 安装前的准备工作

在使用项目中的自动化任务前，请确保进行以下系统准备：

1. **Python 与 pip**  
   - **要求**：Python 3.x 及 pip 已正确安装。  
   - **获取方法**：请访问 [Python 官网](https://www.python.org/downloads/) 下载和安装最新版本。  
   - **验证**：在终端执行 `python --version` 和 `pip --version` 确认安装成功。

2. **Conda 环境管理工具**  
   - **要求**：Anaconda 或 Miniconda 已安装。  
   - **用途**：项目的环境任务会根据 `environment.yaml` 文件创建/检查 Conda 环境。  
   - **获取方法**：请访问 [Anaconda官网](https://www.anaconda.com/products/individual) 或 [Miniconda 官网](https://docs.conda.io/en/latest/miniconda.html)。

3. **Quarto**  
   - **要求**：若需要执行文档渲染任务，Quarto 必须预先安装。  
   - **获取方法**：请访问 [Quarto 官网](https://quarto.org/) 下载安装包，并按照官方安装说明进行配置。  
   - **验证**：在终端中执行 `quarto render` 以确认 Quarto 工作正常。

---

## 环境配置说明

项目所需的重要配置信息保存在项目根目录中的 `environment.yaml` 文件中。此文件不仅定义了 Conda 环境的名称，也包含与 Zotero 及 Bai_Lian API 相关的配置参数。  

### 示例配置

以下是 `env.yaml` 的示例内容，请根据个人实际情况进行修改：

```yaml

# 环境配置示例
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

- **setup-env**  
  检查 `environment.yaml` 中的 `name` 字段，判断当前是否位于目标 Conda 环境中。若已在目标环境则直接返回；若环境存在但未激活，则提示你运行 `conda activate <env_name>`；若不存在，则使用命令 `conda env create -f environment.yaml` 自动创建环境。

- **run-paper**  
  运行 `paper.py` 脚本，处理与论文相关的操作。

- **run-zotero-update**  
  运行 `zotero-update.py` 脚本，用于更新 Zotero 数据或执行其它任务。

- **run-pdf2md**  
  运行 `pdf2md.py` 脚本，将 PDF 文件转换为 Markdown 格式，便于编辑和处理。

- **run-add2yml**  
  运行 `add2yml.py` 脚本，用于对 YAML 文件内容进行添加或更新。

- **run-quarto**  
  执行 `quarto render` 命令，渲染项目文档（前提：确保已安装并配置 Quarto）。

- **all**  
  按下列顺序依次执行：  
  1. `setup-env`  
  2. `run-zotero-update`  
  3. `run-pdf2md`  
  4. `run-add2yml`  
  5. `run-quarto`  
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
     invoke setup-env
     ```
   - 运行处理论文脚本：  
     ```bash
     invoke run-paper
     ```
   - 或一次性执行所有任务：  
     ```bash
     invoke all
     ```

终端将显示详细的执行信息，请根据提示进行下一步操作。

---
