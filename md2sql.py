import re
import json
import sqlite3

keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
filename = '歌曲调号总结.md'
xlsxname = '歌曲调号总结.xlsx'
key_pattern = '## ([ABCDEFG]#?)'
lang_pattern = '### (国语歌曲|外语歌曲|纯音乐)'
song_pattern = (
    r'\d+\. (?P<name>[^（【『]+)(?:（(?P<info>.+)）)?(?:『(?P<spell>.+)』)?(?:【(?P<keys>.+)】)?'
)
info_pattern = r'(?:(?P<source>《.+》[^，]*))?，?(?P<singer>[^，]+)?，?(?:“(?P<lyric>.+)”)?'


def load_song_list(filename):
    song_list = []
    with open(filename, 'r', encoding='utf8') as f:
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
            if not match:
                continue
            name = match.group('name')
            key = current_key
            lang = current_lang
            info = match.group('info')
            ruby = match.group('spell')
            if not info:
                source = None
                artist = None
                lyric = None
            else:
                match2 = re_info.match(info)
                source = match2.group('source')
                artist = match2.group('singer')
                lyric = match2.group('lyric')
            mod = match.group('keys')

            song_list.append(
                {
                    'title': name.strip(),
                    'key': key,
                    'mod': mod,
                    'lang': lang,
                    'ruby': ruby,
                    'src': source,
                    'artist': artist,
                    'lyric': lyric,
                }
            )

    return song_list


def song_list_to_sql(song_list):
    con = sqlite3.connect('songs.db')
    c = con.cursor()

    c.execute(
        """
    CREATE TABLE songs (
        title text,
        key text,
        mod text,
        lang text,
        ruby text,
        src text,
        artist text,
        lyric text
    )
    """
    )

    for song in song_list:
        c.execute(
            """
        INSERT INTO songs VALUES (?,?,?,?,?,?,?,?)
        """,
            (
                song['title'],
                song['key'],
                song['mod'],
                song['lang'],
                song['ruby'],
                song['src'],
                song['artist'],
                song['lyric'],
            ),
        )

    con.commit()
    con.close()


if __name__ == "__main__":
    song_list = load_song_list(filename)
    song_list_to_sql(song_list)
