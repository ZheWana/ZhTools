# 功能：输入寄存器需要存储数值的最大值，获取对应寄存器的位数。
import os

max_value = int(input("Input max value: "))
reg_width = 0
while True:
    if 2**reg_width - 1 >= max_value:
        print(f"Register width: {reg_width}, with max value: {2**reg_width - 1}")
        break
    else:
        reg_width += 1

os.system('pause')
