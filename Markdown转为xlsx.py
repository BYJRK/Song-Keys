from pathlib import Path
import re
import xlsxwriter
import os
from dataclasses import dataclass


keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
filename = '歌曲调位总结.md'
xlsxname = '歌曲调位总结.xlsx'
key_pattern = '## ([ABCDEFG]#?)'
lang_pattern = '### (国语歌曲|外语歌曲|纯音乐)'
song_pattern = r'\d+\. (?P<name>[^（【『]+)(?:（(?P<info>.+)）)?(?:『(?P<spell>.+)』)?(?:【(?P<keys>.+)】)?'
info_pattern = r'(?:(?P<source>《.+》[^，]*))?，?(?P<singer>[^，]+)?，?(?:“(?P<lyric>.+)”)?'


@dataclass
class Song:
    name: str
    spell: str
    source: str
    singer: str
    lyric: str
    key: str
    lang: str
    transpose: str


def load_song_list(filename):
    file = Path(filename)
    song_list = []
    with file.open('r', encoding='utf8') as f:
        current_key = None
        current_lang = None
        re_song = re.compile(song_pattern)
        re_lang = re.compile(lang_pattern)
        re_key = re.compile(key_pattern)
        re_info = re.compile(info_pattern)
        # 逐行分析
        for line in f:
            match = re_key.match(line)
            # 如果匹配到调位标题
            if match:
                current_key = match.group(1)
                continue
            # 如果匹配到种类标题
            match = re_lang.match(line)
            if match:
                current_lang = match.group(1)
                continue
            # 如果匹配到歌曲
            match = re_song.match(line)
            if match:
                name = match.group('name')
                key = current_key
                lang = current_lang
                info = match.group('info')
                spell = match.group('spell')
                if not info:
                    source = None
                    singer = None
                    lyric = None
                else:
                    match2 = re_info.match(info)
                    source = match2.group('source')
                    singer = match2.group('singer')
                    lyric = match2.group('lyric')
                transpose = match.group('keys')
                song = Song(name, spell, source, singer, lyric, key, lang, transpose)
                song_list.append(song)
    return song_list


def display_key_info(song_list, show_pie=False):
    """展示歌曲列表调位的详细分布信息"""
    total = len(song_list)
    total_chinese = len([s for s in song_list if s.lang == "国语歌曲"])
    total_foreign = len([s for s in song_list if s.lang == "外语歌曲"])
    total_instrum = len([s for s in song_list if s.lang == "纯音乐"])
    print('Key   Total(percent)      Chinese        Foreign       Instrumental')
    print('-------------------------------------------------------------------')
    for key in keys:
        song_in_key = [song for song in song_list if song.key == key]
        song_chinese = [song for song in song_in_key if song.lang == '国语歌曲']
        song_foreign = [song for song in song_in_key if song.lang == '外语歌曲']
        song_instrum = [song for song in song_in_key if song.lang == '纯音乐']
        print(f'{key:<3}   {len(song_in_key):>4} ({len(song_in_key)/total*100:>5.2f}%)   ', end='')
        print(f'{len(song_chinese):>4} ({len(song_chinese)/total_chinese*100:>5.2f}%)   ', end='')
        print(f'{len(song_foreign):>4} ({len(song_foreign)/total_foreign*100:>5.2f}%)   ', end='')
        print(f'{len(song_instrum):>4} ({len(song_instrum)/total_instrum*100:>5.2f}%)')
    print('-------------------------------------------------------------------')
    print(f'Total {total:^14}       {total_chinese:^7}       {total_foreign:^7}       {total_instrum:^12}')


def write_xlsx(song_list):
    """将歌曲列表输出到外部 xlsx 文档"""
    book = xlsxwriter.Workbook(xlsxname)
    sheet = book.add_worksheet('歌曲列表')

    # 列宽
    sheet.set_column('A:A', 18) # 歌曲名
    sheet.set_column('B:B', 12) # 读音
    sheet.set_column('C:C', 6)  # 调位
    sheet.set_column('D:D', 9)  # 语言
    sheet.set_column('E:E', 20) # 出处
    sheet.set_column('F:F', 15) # 歌手
    sheet.set_column('G:G', 20) # 歌词

    # 首行
    sheet.write(0, 0, '歌曲名')
    sheet.write(0, 1, '读音')
    sheet.write(0, 2, '调位')
    sheet.write(0, 3, '语言')
    sheet.write(0, 4, '出处')
    sheet.write(0, 5, '歌手')
    sheet.write(0, 6, '歌词')

    # 列表项
    for line, song in enumerate(song_list):
        sheet.write(line + 1, 0, song.name)
        if song.spell:
            sheet.write(line + 1, 1, song.spell)
        sheet.write(line + 1, 2, song.key)
        sheet.write(line + 1, 3, song.lang)
        if song.source:
            sheet.write(line + 1, 4, song.source)
        if song.singer:
            sheet.write(line + 1, 5, song.singer)
        if song.lyric:
            sheet.write(line + 1, 6, song.lyric)
    book.close()


if __name__ == "__main__":
    song_list = load_song_list(filename)
    display_key_info(song_list)
    write_xlsx(song_list)
    os.startfile(xlsxname)
