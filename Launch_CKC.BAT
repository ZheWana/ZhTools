@REM "使用环境：Clion+Keil+CubeMX联合开发"
@REM "脚本默认根路径：Clion项目根目录下(与MDK-ARM目录平级)"
@REM "脚本功能：将工程文件夹拖入脚本文件中，自动打开Keil、Clion以及CubeMX"

@echo off

@REM 指定Clion可执行文件路径
set "ClionExecPath=E:\SoftWare\JetBrains\CLion 2022.1\bin\clion64.exe"
set "current_dir=%1\"

if [%current_dir%] == [] set "current_dir=%~dp0"

echo "About to open project under :%current_dir%"

if exist "%current_dir%*.ioc"  (

    @REM 打开CubeMX
    for %%f in (%current_dir%*.ioc) do start %%f

    @REM @REM @REM 打开Keil
    for /r "%current_dir%MDK-ARM" %%i in (*.uvproj *.uvprojx) do start %%i

    @REM @REM @REM 打开Clion
    start /B "" "%ClionExecPath%" %current_dir%
)

exit
