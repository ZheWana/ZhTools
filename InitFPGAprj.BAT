@echo off
set /p projectName="Input the name of the FPGA project:"
md %projectName%
cd %projectName%
md prj
md user
cd user
md data
md sim
md src

cd src
type nul > top.v