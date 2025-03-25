# 功能：
# 生成VScode的C语言配置文件的settings.json：
# 1.询问工作区编码
# 2.若工作区内含有多个Keil工程，询问使用的工程，没有的话将预定义宏留空
# 3.若所选工程内含有多个目标，询问使用的目标
# 4.询问用户可能使用的编译器路径以及具体的可执行文件
#
# 注意：
# 脚本使用覆盖式生成，使用前请先备份原settings.json文件避免数据丢失

import re
import os

# 保存配置项
encoding = ""
compilerPath = ""
preDefines = []
includePath = []
currentPath = ""


# 将列表内容展示给用户并返回用户的选项
def getUserChoice(items: list, discription: str):
    print("-" * 20 + "\nThere are", len(items), discription, ":")
    for i, item in enumerate(items):
        print(i, ":", item)
    num = input("Please input a integer to select one:")

    if num != "":
        try:
            if int(num) > len(items):
                print("Wrong input, default to use 0.")
                return 0
            else:
                return int(num)
        except:
            print("Wrong input, default to use 0.")
            return 0

    return num


def isCompilerPath(path: str):
    CompilerPathKeyWords = ["gcc", "g++", "arm", "iar", "devkit"]
    lowerPath = path.lower()
    for word in CompilerPathKeyWords:
        if word in lowerPath:
            return True

    return False


# 询问脚本运行路径
temp = input("Please enter the script running path(press Enter for the script path):")
if temp == "":
    currentPath = ".\\"
else:
    if temp.startswith('"') and temp.endswith('"'):
        temp = temp[1:-1]
    currentPath = temp

print(currentPath)

# 询问工作区编码
temp = input(
    "Please set encoding for workspace(u for utf-8, g for gb2312, others will directly fill into the setting)"
)
if temp == "u" or temp == "":
    encoding = '"files.encoding": "utf8",'
elif temp == "g":
    encoding = '"files.encoding": "gb2312",'
else:
    encoding = '"files.encoding": "' + str(temp) + '",'

# 查找后缀为uvprojx或uvproj的文件
mdkFilePath = ""
tarList = []

for root, dirs, files in os.walk(currentPath):
    for f in files:
        if f.endswith(".uvprojx") or f.endswith(".uvproj"):
            tarList.append(os.path.join(root, f))

# 若有多个，让用户选一个
num = ""
if len(tarList) == 0:
    print("No MDK project, can`t generate defines.")
else:
    if len(tarList) > 1:
        num = getUserChoice(tarList, "projects")

    num = 0 if num == "" else num

    mdkFilePath = tarList[num]

    # 查找工程文件中的目标，将目标和宏定义列表作为键值对生成字典
    tarList = {}
    with open(mdkFilePath, "r") as f:
        tar = ""

        for line in f:
            target_matches = re.match(r"<TargetName>(.*)</TargetName>", line.strip())
            define_matches = re.match(r"<Define>(.*)</Define>", line.strip())

            if tar == "" and target_matches:
                tar = target_matches.group(1).strip()

            if define_matches is not None:
                if tar != "":
                    if tar not in tarList:
                        tarList[tar] = re.split(",| ", define_matches.group(1).strip())
                    tar = ""

    # 若有多个目标，询问用户使用哪个
    num = getUserChoice(tarList, "targets")

# 生成宏定义
tarList = [] if num == "" else tarList[list(tarList.keys())[num]]
preDefines.append('"C_Cpp.default.defines": [\n')
for define in tarList:
    preDefines.append('    "' + define + '",\n')
preDefines.append("],\n")

# 默认脚本所在的目录为工作区根目录，将所有含有.h文件的目录加入列表
tarList = []
for root, dirs, files in os.walk(".\\"):
    for f in files:
        if f.endswith(".h"):
            tarList.append(root.replace("\\", "/").replace("./", "${workspaceFolder}/"))
            break

# 生成包含路径
includePath.append('"C_Cpp.default.includePath": [\n')
for path in tarList:
    includePath.append('    "' + path + '",\n')
includePath.append('    "${workspaceFolder}/**"\n')
includePath.append("],\n")

# 查找环境变量中可能的编译器路径(含有bin的路径)，让用户选择
tarList = list(
    filter(
        isCompilerPath,
        os.environ.get("Path").split(";"),
    )
)
num = getUserChoice(
    tarList,
    "Pathes might be your compiler path(You need to choose where compiler is located)",
)
if num != "":
    # 筛选出所选路径中所有的可执行文件
    for root, dirs, files in os.walk(tarList[num]):
        tarList = list(
            filter(
                lambda x: ("gcc" in x or "armcc" in x or "armclang" in x)
                and x.endswith(".exe"),
                files,
            )
        )
        num = getUserChoice(
            tarList, "programes(You have to choose one as your compiler)"
        )
        if num != "":
            compilerPath = os.path.join(root, tarList[num])
        break
if compilerPath != "":
    compilerPath = (
        '"C_Cpp.default.compilerPath": "' + compilerPath.replace("\\", "/") + '",'
    )

ccppExSettings = '"C_Cpp.errorSquiggles": "disabled",\n\
    "C_Cpp.codeAnalysis.clangTidy.checks.disabled": [\n\
    \t"clang-analyzer-*"\n\
    ]\n'

# 创建settings.json并将编码、预定义宏、包含路径写入文件中
if not os.path.exists("./.vscode"):
    os.makedirs("./.vscode")
with open("./.vscode/settings.json", "w+") as f:
    tab = "    "
    f.write("{\n")
    f.write(tab + encoding + "\n")
    f.write(tab + compilerPath + "\n")
    f.writelines([tab + line for line in preDefines])
    f.writelines([tab + line for line in includePath])
    f.writelines(tab + ccppExSettings)
    f.write("}\n")
print("Generating Done.")

os.system("pause")
