# 功能：
# 将所在的文件夹及其子文件夹中的所有.c和.h文件进行编码检测，并把所有非utf-8编码的文件转化为utf-8编码的文件
# 
# 注意：
# 功能涉及到文件内容读写，不排除读写过程出现bug导致文件内容丢失，所使用前请先备份文件

import os
import sys
import chardet
import tkinter
import random
import keyboard

print_color = {
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'purple': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'tail': '\033[0m'
}


def convert_file_to_utf8(filename):
    if os.path.getsize(filename) != 0:
        content = open(filename, 'rb').read()
        res = chardet.detect(content)

        if res['encoding'] != 'utf-8' and res['encoding'] != 'ascii':
            try:
                # convert to utf-8
                code = 'utf-8'
                new_content = content.decode(res['encoding']).encode(code)
                file = open(filename, 'wb').write(content.decode(res['encoding']).encode('utf-8'))
            except UnicodeDecodeError:
                print('----->' + filename + ': ' + 'decode error')
                return
            except TypeError:
                print('----->' + 'type error')
                return
            print(filename + ': ' + 'convert ' + res['encoding'] + ' to utf-8 ok.')
        else:
            # # uncomment to random convert
            # if random.randint(0, 10) <= 5:
            #     code = 'gbk'
            #     print(filename + ': ' + 'random to gbk')
            #     new_content = content.decode(res['encoding']).encode(code)
            #     file = open(filename, 'wb').write(content.decode(res['encoding']).encode(code))
            # else:
                print(filename + ': ' + 'do not need to convert')
    else:
        print('----->' + filename + ' is blank')
        return


g = os.walk(os.getcwd())
filename = ''
flag = False
for i in range(0,3):
    print("IMPORTANT: You'd better back up your folders before continuing.")
print("Press Enter to convert all *.c and *.h files in this folder to UTF-8 encoding.")
keyboard.wait('enter')
print("Start to convert. Please be patient......")
for path, dir_list, file_list in g:
    for file_name in file_list:
        if file_name.endswith(('.c', '.h')):
            if not flag:
                flag = True
            os.path.join(path, file_name)
            convert_file_to_utf8(os.path.join(path, file_name))
if not flag:
    print("No file in the corresponding format, nothing to convert!")
os.system('pause')