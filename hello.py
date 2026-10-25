r"""
第一个 Python 脚本 —— D1 用。

运行方式（在 PowerShell 里）：
    cd C:\Users\Administrator\Projects\py-tools
    python hello.py

这一份不用你改，先跑通，看到输出就算 D1 完成。
"""

import sys
import platform

# 1. 最简单的输出
print("Hello, Python!")

# 2. 变量与 f-string（Python 里拼接文字的标准写法）
name = "未来的测开工程师"
days = 7
print(f"{name}，你给自己定的是 {days} 天做出第一个工具。")

# 3. 读环境信息 —— 这就是"程序能感知运行环境"的最小例子
print(f"Python 版本: {sys.version.split()[0]}")
print(f"操作系统: {platform.system()} {platform.release()}")
print(f"解释器路径: {sys.executable}")

# 4. 一个循环 + 一点计算，感受一下"代码替你干活"
total = 0
for i in range(1, 11):
    total += i
print(f"1 加到 10 的结果是: {total}")

# 5. 字典：后面写工具时最常用的数据结构（配置、接口返回都是它）
tools = {
    "爬虫": "抓数据",
    "pytest": "写自动化用例",
    "PyInstaller": "打包成 exe",
}
print("\n你的工具箱规划：")
for tool, purpose in tools.items():
    print(f"  - {tool}: {purpose}")

print("\nD1 完成。下一步：装 VS Code，然后开始抓数据。")
