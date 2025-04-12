@echo off
rem 安装 pipreqs
pip install pipreqs

rem 使用 pipreqs 生成 requirements.txt 文件
pipreqs . --force

rem 安装 requirements.txt 中的依赖
pip install -r requirements.txt

rem 遍历当前目录下的所有 Python 文件并使用 nuitka 打包
for %%f in (*.py) do (
    python -m nuitka --standalone --onefile --remove-output --mingw64 "%%f" --jobs=16
    echo "%%f" 打包完成。
)
echo 所有 Python 文件打包完成。    