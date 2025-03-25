# 功能：
# 在命令行生成verilog状态机代码
# 使用格式：4 S1 S2 S3 S4 12 23 34 41
# 含义：4个状态，分别为S1、S2、S3、S4，状态转移为1-2、2-3、3-4、4-1
# 
# 注意：
# 功能涉及到文件内容读写，不排除读写过程出现bug导致文件内容丢失，所使用前请先备份文件
import sys
import math
from tkinter import Tk # in Python 2, use "Tkinter" instead 

def add_to_clipboard(text):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.update() # now it stays on the clipboard after the window is closed
    r.destroy()

if(len(sys.argv) == 1):
    print("Usage:Number_Of_State StateName1 StateName2 ... StateTransfer1(such as 12 means 1 -> 2) StateTransfer2 ...")
else:
    try:
        num = int(sys.argv[1])
    except:    
        print("Usage:Number_Of_State StateName1 StateName2 ... StateTransfer1(such as 12 means 1 -> 2) StateTransfer2 ...")
        print("Error: Number_Of_State should be an integer")
        exit(0)

    transfer_position = num + 2
    data_width = math.sqrt(num)
    data_width = int(data_width) if data_width.is_integer() else int(data_width) + 1

    state_name = []
    for i in range(num):
        try:
            if sys.argv[i + 2].isdigit():
                if transfer_position == num + 2:
                    transfer_position = i + 2
                raise ValueError
            state_name.append(sys.argv[i + 2])
        except:
            state_name.append("S" + str(i))

    transfer_list = sys.argv[transfer_position:]
    # Check if the transfer list is full of digit
    for transfer in transfer_list:
        if not transfer.isdigit():
            print("Usage:Number_Of_State StateName1 StateName2 ... StateTransfer1(such as 12 means 1 -> 2) StateTransfer2 ...")
            print("Error: StateTransfer should be an integer")
            exit(0)

    code = ""
    # Generate state name parameter for verilog state machine
    for i in range(num):
        code += "parameter " + state_name[i] + " = " + str(data_width) + "'d" + str(i) + ";\n"
    code += "\n"

    # Generate cur_state and next_state variable
    code += "reg [" + str(data_width - 1) + ": 0] cur_state" + " = " + state_name[0] + ";\n"
    code += "reg [" + str(data_width - 1) + ": 0] next_state" + " = " + state_name[0] + ";\n"
    code += "\n"

    # Generate state transfer block
    code += "always @(posedge clk or negedge rst_n) begin\n"
    code += "\tif (!rst_n) begin\n"
    code += "\t\tcur_state <= " + state_name[0] + ";\n"
    code += "\tend else begin\n"
    code += "\t\tcur_state <= next_state;\n"
    code += "\tend\n"
    code += "end\n\n"

    # Generate state transfer condition
    for transfer in transfer_list:
        variable_name = "transcondition_" + state_name[int(transfer[0]) - 1] + "_to_" + state_name[int(transfer[1]) - 1]
        code += "wire "+ variable_name + ";\n"

    code += "always @(*) begin\n"
    code += "\tcase (cur_state)\n"
    for i,name in enumerate(state_name):
        code += "\t\t" + name + " : begin\n\t\t\t"
        for transfer in transfer_list:
            if i == int(transfer[0]) - 1:
                variable_name = "transcondition_" + state_name[int(transfer[0]) - 1] + "_to_" + state_name[int(transfer[1]) - 1]
                code += "if (cur_state == "+ state_name[int(transfer[0]) - 1] + " && " + variable_name +") begin\n"
                code += "\t\t\t\tnext_state = " + state_name[int(transfer[1]) - 1] + ";\n"
                code += "\t\t\tend else "
        code += "begin\n"
        code += "\t\t\t\tnext_state = cur_state;\n"
        code += "\t\t\tend\n"
        code += "\t\tend\n"

    code += "\t\tdefault: next_state = cur_state;\n" # preventing latch
    code += "\tendcase\n"
    code += "end\n\n"

    # Generate state behavior
    code += "always @(posedge clk or negedge rst_n) begin\n"
    code += "\tif (!rst_n) begin\n"
    code += "\t\t// Reset Signals\n\n"
    code += "\tend else begin\n"
    code += "\t\tcase (cur_state)\n"
    for state in state_name:
        code += "\t\t\t" + state + " : begin\n"
        code += "\t\t\t\t// Handle signals\n\n"
        code += "\t\t\tend\n"
    code += "\t\t\tdefault : begin\n"
    code += "\t\t\tend\n"
    code += "\t\tendcase\n"
    code += "\tend\n"
    code += "end\n\n"

    # Generate transcondition assigning
    for transfer in transfer_list:
        variable_name = "transcondition_" + state_name[int(transfer[0]) - 1] + "_to_" + state_name[int(transfer[1]) - 1]
        code += "assign " + variable_name + " = ( 1 );\n"
    add_to_clipboard(code)
    print(code)
    print("You can Paste it into your Verilog code now")