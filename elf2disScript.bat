@REM 功能：使用fromelf通过elf文件生成反汇编文件
@REM 若有参数则将参数作为fromelf执行参数（将elf文件拖入bat文件）
@REM 没有参数则搜索当前目录下的第一个后缀为elf的文件；
@REM 没有的话则什么也不做。

@REM 注意：fromelf应该在你的环境变量中
@echo off
set scriptPath=%~dp0
set targetPath=%1
if [%targetPath%] == [] (
    if exist *.elf ( 
        for %%f in (*.elf) do (
            fromelf --text -a -c --output=./tarDisFromELF.txt %%f
            exit
        )
    )
) else (
    fromelf --text -a -c --output=./tarDisFromELF.txt %targetPath%
)