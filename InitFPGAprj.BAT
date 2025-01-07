@echo off
set /p projectName="Input the name of the FPGA project:"
md %projectName%
cd %projectName%

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