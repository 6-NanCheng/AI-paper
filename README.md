
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

在执行自动化任务时，`setup-env` 将根据 environment.yaml 的配置检测当前环境，若不匹配或不存在，则自动创建新环境。

---

## 3. 自动化任务说明

所有任务均定义在 `tasks.py` 中，关键任务及其作用如下：

### 3.1 setup-env

- **作用**：检查当前 Conda 环境是否符合 environment.yaml 中的配置。  
  - 环境已激活：提示环境正确。  
  - 环境存在但未激活：提示执行 `conda activate <env_name>`。  
  - 环境不存在：执行 `conda env create -f environment.yaml` 自动创建。

### 3.2 run-paper

- **作用**：执行 `paper.py` 脚本，用于论文检索与筛选（无相关需求可跳过）。

### 3.3 run-zotero-update

- **作用**：执行 `zotero-update.py` 脚本，主要任务：
  - 更新 Zotero 数据，并实时维护文献状态。  
    - 更新后的文献信息会保存至 **state.json**，该文件用于存储 Zotero 当前状态数据，例如已同步的文献条目和相关更新信息；  
  - 输出更新记录至 **zotero_update_summary.json**，该文件详细记录每次更新的摘要和变动信息，便于后续任务参考。

### 3.4 run-pdf2md

- **作用**：执行 `pdf2md.py` 脚本，该任务利用 **zotero_update_summary.json** 中的更新记录：
  - 读取文件中的更新记录，获取需解析的 PDF 文件信息；  
  - 将这些 PDF 文件提交给 AI 模块进行解析，生成 Markdown 格式的解读报告；  
  - 输出的 Markdown 报告用于后续整合与渲染。

### 3.5 run-add2yml

- **作用**：执行 `add2yml.py` 脚本，将生成的解读报告数据添加至 YAML 文件中，便于记录与后续处理。

### 3.6 run-quarto

- **作用**：调用 `quarto render` 命令，渲染生成的解读报告（前提是已正确安装 Quarto）。

### 3.7 all

- **作用**：按以下顺序依次执行所有任务：
  1. setup-env  
  2. run-zotero-update  
  3. run-pdf2md  
  4. run-add2yml  
  5. run-quarto  
- 执行完成后终端显示“所有任务执行完成！”的提示。

*任务执行命令格式统一为：*
```bash
invoke <任务名>
```

---

## 4. 详细运行步骤

按以下步骤操作，确保项目任务顺利执行：

### 4.1 打开终端

- Windows 用户：使用命令提示符或 PowerShell；  
- macOS/Linux 用户：使用 Terminal。

### 4.2 切换到项目根目录

确保 `tasks.py`、`env.yml` 和 `environment.yaml` 均在同一目录中。  
示例命令：
```bash
cd /你的/项目/所在/目录
```

### 4.3 执行各任务

1. **检查或创建 Conda 环境**  
   运行命令：
   ```bash
   invoke setup-env
   ```
   - 若未激活已创建环境，请根据提示执行 `conda activate <env_name>`。

2. **更新 Zotero 数据**  
   运行命令：
   ```bash
   invoke run-zotero-update
   ```
   - 执行后检查生成的两个文件：  
     - **state.json**：存储 Zotero 最新同步状态信息（如文献条目、更新时间等）；  
     - **zotero_update_summary.json**：记录更新摘要与变动详情，供后续任务使用。

3. **解析 PDF 并生成 Markdown 报告**  
   运行命令：
   ```bash
   invoke run-pdf2md
   ```
   - 脚本从 **zotero_update_summary.json** 中读取更新记录，获取需解析的 PDF 文件信息。  
   - AI 模块解析后生成 Markdown 格式的报告，供后续编辑和使用。

4. **将解读报告数据添加至 YAML 文件**  
   运行命令：
   ```bash
   invoke run-add2yml
   ```

5. **渲染解读报告（可选）**  
   若需转换 Markdown 报告为最终格式，运行命令：
   ```bash
   invoke run-quarto
   ```
   - 请确保 Quarto 已正确安装和配置。

6. **整体执行所有任务(除检索文件的所有步骤)**  
   一步完成整个流程，运行命令：
   ```bash
   invoke all
   ```
   - 系统将按顺序执行所有任务，并在任务结束时显示成功提示。

---

## 附：state.json 与 zotero_update_summary.json 说明

- **state.json**  
  - 用于记录 Zotero 数据的当前状态。  
  - 保存同步时刻的文献条目列表、标记信息等，确保后续更新时可以对比和判断变动。

- **zotero_update_summary.json**  
  - 用于记录每次运行 `zotero-update.py` 时的更新内容。  
  - 包含新增文献、其所在目录的关键数据，供 **run-pdf2md** 任务参考，确保仅解析最新更新的 PDF 文件信息。

---
