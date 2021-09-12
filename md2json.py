from pathlib import Path
import re
import xlsxwriter
import os
import json
import dataclasses
from dataclasses import dataclass

keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
filename = '歌曲调位总结.md'
xlsxname = '歌曲调位总结.xlsx'
key_pattern = '## ([ABCDEFG]#?)'
lang_pattern = '### (国语歌曲|外语歌曲|纯音乐)'
song_pattern = (
    r'\d+\. (?P<name>[^（【『]+)(?:（(?P<info>.+)）)?(?:『(?P<spell>.+)』)?(?:【(?P<keys>.+)】)?'
)
info_pattern = r'(?:(?P<source>《.+》[^，]*))?，?(?P<singer>[^，]+)?，?(?:“(?P<lyric>.+)”)?'


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

                song_list.append(
                    {
                        'title': name,
                        'key': key,
                        'mod': None if not transpose else transpose.split('→'),
                        'lang': lang,
                        'ruby': spell,
                        'src': source,
                        'artist': None if not singer else singer.split('&'),
                        'lyric': lyric,
                    }
                )

    return song_list


if __name__ == "__main__":
    song_list = load_song_list(filename)
    with open('songs.json', 'w', encoding='utf-8') as f:
        json.dump(song_list, f)
