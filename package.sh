# 1. 安装必须的工具
pip install setuptools wheel build twine

# 2. 打包
python -m build

# 3. 上传
twine upload dist/*