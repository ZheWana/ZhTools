@echo off
rem 安装 pipreqs
pip install pipreqs
if %errorlevel% neq 0 (
    echo 安装 pipreqs 失败，请检查网络或权限。
    exit /b 1
)

rem 安装 Nuitka
pip install Nuitka==2.0.6
if %errorlevel% neq 0 (
    echo 安装 Nuitka 失败，请检查网络或权限。
    exit /b 1
)

rem 使用 pipreqs 生成 requirements.txt 文件
pipreqs . --force
if %errorlevel% neq 0 (
    echo 生成 requirements.txt 文件失败。
    exit /b 1
)

rem 安装 requirements.txt 中的依赖
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 安装依赖失败，请检查 requirements.txt 文件或网络。
    exit /b 1
)

rem 检查 build 目录是否存在，如果不存在则创建
if not exist build (
    mkdir build
    if %errorlevel% neq 0 (
        echo 创建 build 目录失败，请检查权限。
        exit /b 1
    )
)

rem 遍历当前目录下的所有 Python 文件并使用 nuitka 打包
for %%f in (*.py) do (
    echo //-----------------------------
    python -m nuitka --standalone --output-dir=build --onefile --remove-output --mingw64 "%%f" --jobs=16
    if %errorlevel% neq 0 (
        echo "%%f" 打包失败。
        continue
    )
    echo "%%f" 打包完成。
    echo //-----------------------------
)
echo 所有 Python 文件打包完成