# 此脚本的主要功能是批量修改指定目录下 MP3 文件的元数据信息。
# 具体来说，它会对每个 MP3 文件进行以下操作：
# 1. 解析文件名，文件名需符合 "歌手 - 歌曲标题" 的格式。
#    若格式正确，会提取出歌手和歌曲标题信息。
#    若格式不正确，则跳过该文件，并给出相应提示。
# 2. 从文件名中查找不区分大小写的 "xxxbpm" 信息。
#    若找到，将其转换为小写形式作为歌曲类型信息。
#    若未找到，默认歌曲类型信息为 "180bpm"。
# 3. 处理 MP3 文件的 ID3 标签：
#    - 若文件已有 ID3 标签，直接对其进行修改。
#    - 若文件没有 ID3 标签，会创建一个新的 ID3 标签。
#    - 若文件损坏或不是有效的 MP3 文件，会跳过该文件并给出提示。
# 4. 修改 ID3 标签中的元数据：
#    - 将解析得到的歌曲标题信息写入 TIT2 帧。
#    - 将解析得到的歌手信息写入 TPE1 帧。
#    - 将提取或默认的歌曲类型信息写入 TCON 帧。
# 5. 保存修改后的 ID3 标签，并输出修改成功的提示信息。
# 6. 对于处理过程中出现的异常，会输出相应的错误提示信息。

import os
import re
from mutagen.id3 import ID3, TIT2, TCON, TPE1
from mutagen.mp3 import MP3, HeaderNotFoundError


def modify_mp3_metadata(directory):
    print(f"开始处理目录: {directory}")
    for root, dirs, files in os.walk(directory):
        print(f"正在处理目录: {root}")
        for file in files:
            if file.endswith('.mp3'):
                file_path = os.path.join(root, file)
                print(f"找到 MP3 文件: {file_path}")
                try:
                    # 去掉文件扩展名
                    file_name = os.path.splitext(file)[0]
                    # 解析歌手和歌曲标题
                    parts = file_name.split(' - ', 1)
                    if len(parts) == 2:
                        artist, title = parts
                        print(f"解析得到歌手: {artist}, 歌曲标题: {title}")
                    else:
                        print(f"文件名 {file} 格式不正确，跳过。")
                        continue

                    # 尝试从文件名中提取不区分大小写的 xxbpm 信息
                    bpm_match = re.search(r'(\d+)[Bb][Pp][Mm]', file_name)
                    if bpm_match:
                        song_type = bpm_match.group(0).lower()
                    else:
                        song_type = '180bpm'

                    try:
                        audio = ID3(file_path)
                    except Exception:
                        try:
                            # 如果文件没有 ID3 标签，创建一个新的
                            audio = MP3(file_path, ID3=ID3)
                            audio.add_tags()
                        except HeaderNotFoundError:
                            print(f"文件 {file_path} 可能损坏或不是有效的 MP3 文件，跳过。")
                            continue

                    # 设置歌曲标题
                    audio['TIT2'] = TIT2(encoding=3, text=title)
                    # 设置歌手
                    audio['TPE1'] = TPE1(encoding=3, text=artist)
                    # 设置歌曲类型
                    audio['TCON'] = TCON(encoding=3, text=song_type)
                    audio.save()
                    print(f"已成功修改文件: {file_path}，歌曲类型信息设置为: {song_type}")
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")


if __name__ == "__main__":
    print("此脚本用于批量修改 MP3 文件的元数据。")
    print("它会解析文件名，提取歌手、歌曲标题和 bpm 信息，将其写入 MP3 文件的 ID3 标签。")
    directory = input("请输入包含 MP3 文件的目录路径: ")
    modify_mp3_metadata(directory)
    