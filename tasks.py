import os
import sys
import yaml
import re
from subprocess import check_output
from invoke import task

def get_env_name(yaml_file="environment.yaml"):
    """
    通过 PyYAML 从 environment.yaml 文件中获取环境名称。
    若文件不存在或未找到 'name' 键，则输出警告或退出程序。
    """
    if os.path.exists(yaml_file):
        with open(yaml_file, "r", encoding="utf-8") as f:
            try:
                env_data = yaml.safe_load(f)
                env_name = env_data.get("name")
                if env_name:
                    return env_name.strip()
                else:
                    print("Warning: environment.yaml 中未找到 'name' 键。")
            except Exception as e:
                print("Error parsing environment.yaml:", e)
                sys.exit(1)
    else:
        print("Warning: environment.yaml 文件不存在。")
    return None

def conda_env_exists(env_name):
    """
    检查 Conda 环境是否存在。

    通过调用 "conda env list" 获取已注册的环境信息，
    如果输出中显示环境名称为完整路径，则提取最后一部分进行匹配，
    同时匹配不区分大小写。
    """
    try:
        envs_output = check_output("conda env list", shell=True, encoding="utf-8")
        target = env_name.lower()
        for line in envs_output.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # 去除当前激活环境标记 '*'
            line = line.replace("*", "").strip()
            match = re.match(r"^(\S+)", line)
            if match:
                candidate = match.group(1).strip()
                # 如果 candidate 是一个路径（包含路径分隔符），则提取 basename
                if os.path.sep in candidate:
                    candidate = os.path.basename(candidate)
                if candidate.lower() == target:
                    return True
        return False
    except Exception as e:
        print("无法检查 conda 环境:", e)
        return False

@task
def setup_env(c):
    """
    检查并创建或更新 Conda 环境。

      1. 从 environment.yaml 中读取目标环境名称；
      2. 如果当前已处于目标环境中，则直接退出；
      3. 如果目标环境已经存在，则提示用户手动激活；
      4. 如果目标环境不存在，则使用 environment.yaml 自动创建环境。
    """
    yaml_file = "environment.yaml"
    env_name = get_env_name(yaml_file)
    if not env_name:
        print("未能从 environment.yaml 获取环境名称。")
        sys.exit(1)

    print(f"目标 Conda 环境: {env_name}")

    # 检查当前是否已在目标环境中（忽略大小写）
    current_env = os.environ.get("CONDA_DEFAULT_ENV")
    if current_env and current_env.lower() == env_name.lower():
        print("当前已在目标 Conda 环境中。")
        return

    if conda_env_exists(env_name):
        print(f"环境 '{env_name}' 已存在。")
        print(f"请在命令行中运行: conda activate {env_name}")
        print("激活后再重新运行此命令。")
        sys.exit(0)
    else:
        print(f"环境 '{env_name}' 不存在，正在创建...")
        try:
            result = c.run(f"conda env create -f {yaml_file}", warn=True)
            if result.failed:
                print("创建环境失败，请手动处理。")
                sys.exit(1)
            else:
                print(f"环境创建成功！请运行: conda activate {env_name}")
                sys.exit(0)
        except Exception as e:
            print("创建环境失败，请手动处理：", e)
            sys.exit(1)

if __name__ == "__main__":
    from invoke import Program
    program = Program(namespace=globals())
    program.run()



@task
def run_paper(c):
    print("正在运行 paper.py...")
    c.run("python paper.py")    

@task
def run_zotero_update(c):
    print("正在运行 zotero_update.py...")
    c.run("python zotero_update.py")

@task
def run_pdf2md(c):
    print("正在运行 pdf2md.py...")
    c.run("python pdf2md.py")

@task
def run_add2yml(c):
    print("正在运行 add2yml.py...")
    c.run("python add2yml.py")

@task
def run_quarto(c):
    print("正在执行 quarto render...")
    c.run("quarto render")

@task(pre=[setup-env, run_zotero_update, run_pdf2md, run_add2yml, run_quarto])
def all(c):
    print("所有任务执行完成！")

