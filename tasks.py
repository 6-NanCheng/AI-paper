import os
import sys
import yaml
from invoke import task

def get_env_name(yaml_file="environment.yaml"):
    if os.path.exists(yaml_file):
        with open(yaml_file, "r", encoding="utf-8") as f:
            try:
                env_data = yaml.safe_load(f)
                env_name = env_data.get("name")
                if env_name:
                    return env_name
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
    检查 conda 环境是否存在
    """
    from subprocess import check_output
    try:
        envs = check_output("conda env list", shell=True, encoding="utf-8")
        return any(env_name in line for line in envs.splitlines())
    except Exception as e:
        print("无法检查 conda 环境:", e)
        return False

@task
def setup_env(c):
    """
    检查并创建或更新 Conda 环境（Windows-friendly）
    """
    yaml_file = "environment.yaml"
    env_name = get_env_name(yaml_file)
    if not env_name:
        print("未能从 environment.yaml 获取环境名称。")
        sys.exit(1)

    print(f"目标 Conda 环境: {env_name}")

    # 判断是否已处于该环境中
    current_env = os.environ.get("CONDA_DEFAULT_ENV")
    if current_env == env_name:
        print("当前已在目标 Conda 环境中。")
        return

    if conda_env_exists(env_name):
        print(f"已存在环境 '{env_name}'，尝试激活...")
        print(f"请在命令行手动运行: conda activate {env_name}")
        print("继续前将中断执行，激活环境后请重新运行本命令。")
        sys.exit(0)
    else:
        print(f"环境 '{env_name}' 不存在，正在创建...")
        try:
            c.run(f"conda env create -f {yaml_file}")
            print(f"环境创建成功！请运行: conda activate {env_name}")
            sys.exit(0)
        except Exception as e:
            print("创建环境失败，请手动处理：", e)
            sys.exit(1)
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

@task(pre=[setup_env, run_zotero_update, run_pdf2md, run_add2yml, run_quarto])
def all(c):
    print("所有任务执行完成！")

