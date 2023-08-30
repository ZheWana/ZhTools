# 功能：
# 生成VScode的C语言配置文件的settings.json
# 
# 注意：
# 功能涉及到文件内容读写，不排除读写过程出现bug导致文件内容丢失，所使用前请先备份文件

import re
import os

# 保存配置项
encoding = ""
preDefines = []
includePath = []

# 询问工作区编码
temp = input("Please set encoding for workspace(u for utf-8, g for gb2312, others will directly fill into the setting)")
if temp == "u" or temp == "":
    encoding = "\"files.encoding\": \"utf8\","
elif temp == "g":
    encoding = "\"files.encoding\": \"gb2312\","
else:
    encoding = "\"files.encoding\": \"" + str(temp) + "\","

# 查找后缀为uvprojx或uvproj的文件
mdkFilePath = ""
tarList = []

for root, dirs, files in os.walk(".\\"):
    for f in files:
        if f.endswith(".uvprojx") or f.endswith(".uvproj"):
            tarList.append(os.path.join(root, f))

# 若有多个，让用户选一个
if len(tarList) == 0:
    print("No MDK project, can`t generate defines.")
else:
    num = 0
    if len(tarList) > 1:
        print("There are", len(tarList), "project files:")
        for i in range(len(tarList)):
            print(i, ":", tarList[i])
        num = input("Please input a integer to select one:")

    try:
        if int(num) > len(tarList):
            num = 0
            print("Wrong input, default to use 0.")
    except:
        print("Wrong input, default to use 0.")

    mdkFilePath = tarList[int(num)]

    # 查找工程文件中的目标，将目标和宏定义列表作为键值对生成字典
    tarList = {}
    with open(mdkFilePath, "r") as f:
        tar = ""

        line = f.readline();
        while line:
            target_matches = re.match(r'<TargetName>(.*)</TargetName>', line.strip())
            define_matches = re.match(r'<Define>(.*)</Define>', line.strip())

            if tar == "" and target_matches:
                tar = target_matches.group(1).strip()

            if define_matches is not None:
                if tar != "":
                    if(tar not in tarList):
                        tarList[tar] = re.split(",| ", define_matches.group(1).strip())
                    tar = ""

            line = f.readline()

    # 若有多个目标，询问用户使用哪个
    num = 0
    if len(tarList) > 1:
        print("There are", len(tarList), "targets:")
        for i in range(len(tarList)):
            print(i, ":", list(tarList.keys())[i])
        num = input("Please input a integer to select one:")

    try:
        if int(num) > len(tarList):
            num = 0
            print("Wrong input, default to use 0.")
    except:
        print("Wrong input, default to use 0.")

# 生成宏定义
try:
    tarList = tarList[list(tarList.keys())[int(num)]]
except:
    tarList = []
preDefines.append("\"C_Cpp.default.defines\": [\n")
for define in tarList:
    preDefines.append("    \"" + define + "\",\n")
preDefines.append("],\n")

# 默认脚本所在的目录为工作区根目录，将所有含有.h文件的目录加入列表
tarList = []
for root, dirs, files in os.walk(".\\"):
    for f in files:
        if f.endswith(".h"):
            tarList.append(root.replace("\\", "/").replace("./", "${workspaceFolder}/"))
            break

# 生成包含路径
includePath.append("\"C_Cpp.default.includePath\": [\n")
for path in tarList:
    includePath.append("    \"" + path + "\",\n")
includePath.append("    \"${workspaceFolder}/**\"\n")
includePath.append("],\n")

# 创建并将编码、预定义宏、包含路径写入文件中
if not os.path.exists("./.vscode"):
    os.makedirs("./.vscode")
with open("./.vscode/settings.json", "w+") as f:
    tab = "    "
    f.write("{\n")
    f.write(tab + encoding + "\n")
    f.writelines([tab + line for line in preDefines])
    f.writelines([tab + line for line in includePath])
    f.write("}\n")
print("Generating Done.")

