本项目旨在构建一套集“文献抓取—智能筛选—数据存储—信息提取—成果展示”为一体的自动化文献管理系统。

其核心功能包括：

- 系统首先通过AI模型批量采集与特定主题相关的文献。 AI模型会对每篇文献进行关键字打分，进一步评估语义相关性，仅保留高关联度的文章。

- 高质量文献将被保存到zotero进行结构化存储和标签管理，确保文献信息完整有序。

- 系统通过调用AI大模型，从Zotero数据库中自动提取文献的关键信息并进行深入解读，并生成统一格式的Markdown文档。

- 利用Quarto渲染生成直观、阅读流畅的网页展示界面，为用户呈现极致的文献浏览体验。


---

# 项目说明文档

---

## 1. 环境准备

请按以下顺序确保系统满足要求：

### 1.1 安装 Python 与 pip

- **要求**：安装 Python 3.x 与 pip。  
- **获取方式**：[Python 官网](https://www.python.org/downloads/)  
- **验证方法**：
  ```bash
  python --version
  pip --version
  ```

### 1.2 安装 Conda 环境管理工具

- **要求**：安装 Anaconda 或 Miniconda，用于创建和管理独立的开发环境。  
- **获取方式**：  
  - [Anaconda 官网](https://www.anaconda.com/products/individual)  
  - [Miniconda 官网](https://docs.conda.io/en/latest/miniconda.html)

### 1.3 安装 Invoke 与其它依赖库

在 Python 与 Conda 安装完成后，运行以下命令安装项目依赖：
```bash
pip install invoke pyyaml
```

### 1.4 安装 Quarto（可选）

- **要求**：若需执行文档渲染任务，必须安装 Quarto。  
- **获取方式**：[Quarto 官网](https://quarto.org/)  
- **验证方法**：
  ```bash
  quarto render
  ```

---

## 2. 配置文件说明

项目使用两个配置文件，各有不同作用：

### 2.1 env.yml（密钥与 API 参数配置）

- **作用**：存放密钥、API 参数等敏感信息。  
- **示例配置**：
  ```yaml
  # env.yml 配置示例
  Zotero_Storage: "C:/Path/To/Your/Zotero/Storage"
  Bai_Lian_API_KEY: "<your_bai_lian_api_key>"
  Zotero_user_id: "<your_zotero_user_id>"
  Zotero_API_KEY: "<your_zotero_api_key>"
  Zotero_BASE_URL: "https://api.zotero.org"
  ```

### 2.2 environment.yaml（Conda 环境配置）

- **作用**：定义项目开发和运行所需的 Conda 环境。  
- **示例配置**：
  ```yaml
  # environment.yaml 配置示例
  name: my_project_env
  channels:
    - defaults
  dependencies:
    - python=3.x
    - pip
    - pyyaml
    - invoke
    # 根据需要添加其它依赖
  ```

在执行自动化任务时，`setup-env` 会根据 environment.yaml 的配置检测当前环境，若不匹配或不存在，则自动创建新环境。

---

## 3. 自动化任务说明

所有任务均定义在 `tasks.py` 中，关键任务及其作用如下：

### 3.1 setup-env

- **作用**：检查当前 Conda 环境是否符合 environment.yaml 中的配置。  
  - 若已激活目标环境，提示环境正确；  
  - 若环境存在但未激活，提示执行 `conda activate <env_name>`；  
  - 若环境不存在，执行 `conda env create -f environment.yaml` 自动创建。

### 3.2 run-paper

- **作用**：执行 `paper.py` 脚本，进行论文检索与筛选。如果项目中无论文处理需求，此任务可跳过。

### 3.3 run-zotero-update

- **作用**：执行 `zotero-update.py` 脚本，主要任务：
  - 更新 Zotero 数据，并实时维护文献状态（保存至 **state.json**）；  
  - 输出更新记录至 **zotero_update_summary.json**。

### 3.4 run-pdf2md

- **作用**：执行 `pdf2md.py` 脚本，该任务关键在于利用 **zotero_update_summary.json** 中的数据：
  - 脚本会从 **zotero_update_summary.json** 中读取更新记录，获取需解析的 PDF 文件信息；  
  - 将这些 PDF 文件提交给 AI 模块进行解析，并生成 Markdown 格式的解读报告；  
  - 输出的 Markdown 文件供后续编辑、整合或渲染使用。

### 3.5 run-add2yml

- **作用**：执行 `add2yml.py` 脚本，将生成的解读报告数据添加到 YAML 文件中，便于后续处理或记录。

### 3.6 run-quarto

- **作用**：调用 `quarto render` 命令，渲染生成的解读报告（前提是已正确安装 Quarto）。

### 3.7 all

- **作用**：按以下顺序依次执行所有任务：
  1. setup-env  
  2. run-zotero-update  
  3. run-pdf2md  
  4. run-add2yml  
  5. run-quarto  
- 执行完成后，终端将显示“所有任务执行完成！”的提示。

*任务执行命令格式统一为：*
```bash
invoke <任务名>
```

---

## 4. 详细运行步骤

按照以下步骤操作，确保项目任务顺利执行：

### 4.1 打开终端

- Windows 用户：使用命令提示符或 PowerShell。  
- macOS / Linux 用户：使用 Terminal。

### 4.2 切换到项目根目录

确保 `tasks.py`、`env.yml` 和 `environment.yaml` 均位于该目录中。  
示例命令：
```bash
cd /你的/项目/所在/目录
```

### 4.3 执行任务

依次运行以下命令：

1. **检查或创建 Conda 环境**  
   运行：
   ```bash
   invoke setup-env
   ```
   - 若未激活已创建环境，请按照提示使用 `conda activate <env_name>` 命令激活。

2. **更新 Zotero 数据**  
   运行：
   ```bash
   invoke run-zotero-update
   ```
   - 执行后，确保生成两个文件：**state.json** 与 **zotero_update_summary.json**。

3. **解析 PDF 并生成 Markdown 报告**  
   运行：
   ```bash
   invoke run-pdf2md
   ```
   - 该任务读取 **zotero_update_summary.json** 中的更新记录，从中提取所需的 PDF 文件信息，并提交 AI 模块解析。  
   - 生成的 Markdown 报告用于后续处理和参考。

4. **将解读报告数据添加到 YAML 文件中**  
   运行：
   ```bash
   invoke run-add2yml
   ```

5. **渲染解读报告（可选）**  
   若需要将 Markdown 报告转换为最终格式，运行：
   ```bash
   invoke run-quarto
   ```
   - 请确认 Quarto 已正确安装。

6. **整体执行所有任务**  
   如需一步完成所有流程，运行：
   ```bash
   invoke all
   ```
   - 此命令按顺序执行以上各任务，并在流程结束时显示成功提示。

---

本文件去除多余描述，保留所有关键信息，确保每一步操作详尽明了。按照此文档执行后，即可顺利运行项目所有自动化任务。


