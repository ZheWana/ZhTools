# 此脚本的主要功能是批量处理指定目录下的 MP3 文件，具体包含以下操作：
# 1. 引导用户输入包含 MP3 文件的目录路径。
# 2. 遍历指定目录及其子目录，找出所有的 MP3 文件。
# 3. 对于每个 MP3 文件，检查其文件名格式是否为 "歌手 - 歌曲标题"：
#    - 若格式正确，提取出歌手和歌曲标题信息。
#    - 若格式不正确，输出提示信息并跳过该文件。
# 4. 优先从 MP3 文件的 TBPM 标签获取每分钟节拍数（bpm）信息，若该标签不存在，再从文件名中查找不区分大小写的 "xxxbpm" 信息：
#    - 若从 TBPM 标签获取，将其值乘以 2 后按照新的分组规则（每 10 步一组，168 - 178 为 170 范围等）进行分组，得到相应的 bpm 形式作为歌曲类型信息，并写入 MP3 文件的 ID3 标签。
#    - 若从文件名获取，直接按照新的分组规则进行分组，得到相应的 bpm 形式作为歌曲类型信息，并写入 MP3 文件的 ID3 标签。
#    - 若未找到，输出提示信息并跳过该文件，不进行后续处理。
# 5. 处理 MP3 文件的 ID3 标签：
#    - 若文件已有 ID3 标签，直接对其进行修改。
#    - 若文件没有 ID3 标签，创建一个新的 ID3 标签。
#    - 若文件损坏或不是有效的 MP3 文件，输出错误提示并跳过该文件。
# 6. 修改 ID3 标签中的元数据：
#    - 将解析得到的歌曲标题信息写入 TIT2 帧。
#    - 将解析得到的歌手信息写入 TPE1 帧。
#    - 将提取并转换后的歌曲类型信息写入 TCON 帧。
#    - 清空唱片集信息（TALB 帧）。
# 7. 按照相应规则计算得到的 bpm 进行分组：
#    - 为每个组别创建对应的文件夹（如果文件夹不存在）。
#    - 将文件移动到对应的分组文件夹中。
# 8. 在整个处理过程中，使用 print 语句输出关键信息，如开始处理目录、找到文件、解析信息、修改元数据、创建文件夹、移动文件以及出现的错误等，避免输出冗余信息，确保输出清晰有条理。

import os
import re
import shutil
from mutagen.id3 import ID3, TIT2, TCON, TPE1, TALB
from mutagen.mp3 import MP3, HeaderNotFoundError


def get_bpm_group(adjusted_bpm):
    if adjusted_bpm % 10 >= 8:
        return (adjusted_bpm // 10 + 1) * 10
    return (adjusted_bpm // 10) * 10


def modify_mp3_metadata(directory):
    print(f"开始处理目录: {directory}")
    for file in os.listdir(directory):
        if file.endswith(".mp3"):
            file_path = os.path.join(directory, file)
            print(f"找到 MP3 文件: {file_path}")
            try:
                # 去掉文件扩展名
                file_name = os.path.splitext(file)[0]
                # 解析歌手和歌曲标题
                parts = file_name.split(" - ", 1)
                if len(parts) == 2:
                    artist, title = parts
                    print(f"  解析得到歌手: {artist}, 歌曲标题: {title}")
                else:
                    print(f"  文件名 {file} 格式不正确，跳过。")
                    continue

                try:
                    audio = ID3(file_path)
                except Exception:
                    try:
                        # 如果文件没有 ID3 标签，创建一个新的
                        audio = MP3(file_path, ID3=ID3)
                        audio.add_tags()
                    except HeaderNotFoundError:
                        print(
                            f"  文件 {file_path} 可能损坏或不是有效的 MP3 文件，跳过。"
                        )
                        continue

                # 优先从 TBPM 标签获取 bpm 信息
                bpm = None
                bpm_multiplier = 1
                if "TBPM" in audio:
                    try:
                        bpm = float(audio["TBPM"].text[0])
                        bpm_multiplier = 2
                    except ValueError:
                        print(
                            f"  文件 {file_path} 的 TBPM 标签值无法转换为浮点数，跳过。"
                        )
                        continue
                else:
                    # 尝试从文件名中提取不区分大小写的 xxbpm 信息
                    bpm_match = re.search(r"(\d+(\.\d+)?)[Bb][Pp][Mm]", file_name)
                    if bpm_match:
                        bpm = float(bpm_match.group(1))

                if bpm is None:
                    print(f"  文件 {file} 未找到 bpm 信息，跳过。")
                    continue

                # 按照新规则进行分组
                adjusted_bpm = bpm_multiplier * bpm
                bpm_group = get_bpm_group(adjusted_bpm)
                song_type = f"{bpm_group:.0f}bpm"

                # 设置歌曲标题
                audio["TIT2"] = TIT2(encoding=3, text=title)
                # 设置歌手
                audio["TPE1"] = TPE1(encoding=3, text=artist)
                # 设置歌曲类型
                audio["TCON"] = TCON(encoding=3, text=song_type)
                # 清空唱片集信息
                if "TALB" in audio:
                    del audio["TALB"]

                audio.save()
                print(
                    f"  已成功修改文件: {file_path}，歌曲类型信息设置为: {song_type}，唱片集信息已清空"
                )

                # 创建分组文件夹
                group_folder = os.path.join(directory, song_type)
                if not os.path.exists(group_folder):
                    os.makedirs(group_folder)
                    print(f"  创建分组文件夹: {group_folder}")
                # 移动文件到分组文件夹
                new_file_path = os.path.join(group_folder, file)
                shutil.move(file_path, new_file_path)
                print(f"  已将文件 {file} 移动到 {group_folder}")
            except Exception as e:
                print(f"  处理文件 {file_path} 时出错: {e}")


if __name__ == "__main__":
    print("此脚本用于批量修改 MP3 文件的元数据，并按 bpm 进行分组。")
    print(
        "它会解析文件名，提取歌手、歌曲标题和 bpm 信息，将其写入 MP3 文件的 ID3 标签。"
    )
    print("然后按照规则对 bpm 进行分组，将文件移动到对应文件夹，同时清空唱片集信息。")
    directory = input("请输入包含 MP3 文件的目录路径: ")
    modify_mp3_metadata(directory)
