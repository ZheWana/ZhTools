@echo off
set /p projectPath="Input the path of the FPGA project:"
if "%projectPath%"=="" (
    set projectPath=.
)
set /p projectName="Input the name of the FPGA project:"
md "%projectPath%\%projectName%"
cd "%projectPath%\%projectName%"

echo prj/** > .gitignore
md prj
md user
cd user
md data
md sim
md src

cd src
type nul > top.v

cd .. 
cd sim
type nul > sim.v