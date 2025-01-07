# 将MarkDown文档中分散在系统各处的图片汇总到md同级的assets目录下，以便对图片做管理或者对文档进行迁移
# 参数：md文件路径或者含有需要操作的所有md文件的文件夹

from genericpath import isdir, isfile
import os
import re


def copy_img_and_change_dir(md_file_path):
    base_dir = os.path.dirname(md_file_path)
    assets_dir = os.path.join(base_dir, "assets")

    # 如果assets目录不存在，则创建它
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)

    with open(md_file_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    img_paths = re.findall(r"!\[[^\)]*\]\((.*)\)", md_content)

    for img_path in img_paths:

        # 处理相对路径
        if not os.path.isabs(img_path):
            abs_path = os.path.join(base_dir, img_path)
        else:
            abs_path = img_path

        # 忽略网络图片
        if "http" in img_path:
            continue

        # 获取图片文件名
        img_filename = os.path.basename(abs_path)
        new_img_path = os.path.join(assets_dir, img_filename)

        # 复制图片到assets文件夹
        print(f'Copying {abs_path}...')
        os.system(f'cp "{abs_path}" "{new_img_path}" > NUL')

        # 替换Markdown内容中的图片路径
        md_content = md_content.replace(img_path, f"assets/{img_filename}")

    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(md_content)


if __name__ == "__main__":
    md_file_path = input("Please input file path:")
    md_files = []
    if os.path.isdir(md_file_path):
        for root, dirs, files in os.walk(md_file_path):
            for file in files:
                if file.endswith(".md"):
                    md_files.append(os.path.join(root, file))
    elif os.path.isfile(md_file_path):
        md_files.append(md_file_path)

    [copy_img_and_change_dir(md_file) for md_file in md_files]
