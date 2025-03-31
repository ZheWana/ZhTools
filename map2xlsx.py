import re
import sys
import openpyxl
import os

size_start = False

def read_map_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def parse_map_content(content):
    object_pattern = re.compile(r'(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\S+\.o)')
    object_matches = object_pattern.findall(content)

    object_data = []
    for i,match in enumerate(object_matches):
        object_data.append([int(match[0]), int(match[1]), int(match[2]), int(match[3]), int(match[4]), int(match[5]), match[6], f"=SUM(A{i+2}:F{i+2})"])

    return object_data


def create_excel(object_data, output_path):
    workbook = openpyxl.Workbook()

    object_sheet = workbook.active
    object_sheet.title = 'Object Data'
    object_sheet.append(['Code','(inc. data)', 'RO Data', 'RW Data', 'ZI Data', 'Debug', 'Object Name', 'Total'])
    for row in object_data:
        if "Object Totals" in row:
            break
        object_sheet.append(row)

    workbook.save(output_path)


def find_map_files(path):
    map_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.map'):
                file_path = os.path.join(root, file)
                map_files.append(file_path)
    return map_files

def get_filename_without_extension(mapfile_path):
    # 使用os.path.basename获取文件名（包含后缀）
    filename_with_ext = os.path.basename(mapfile_path)
    # 使用os.path.splitext分割文件名和后缀，取文件名部分
    filename_without_ext = os.path.splitext(filename_with_ext)[0]
    return filename_without_ext

if __name__ == "__main__":

    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        if os.path.isfile(input_path) and input_path.endswith('.map'):
            map_files = [input_path]
        else:
            map_files = find_map_files(input_path)
    else:
        map_files = find_map_files('.')

    for mapFile in map_files:
        map_file_path = mapFile
        output_excel_path = get_filename_without_extension(mapFile) + "_map.xlsx"
        map_content = read_map_file(map_file_path)
        object_data = parse_map_content(map_content)
        create_excel(object_data, output_excel_path)
