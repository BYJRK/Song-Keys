import sqlite3


KEYS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
LANGS = ['国语歌曲', '外语歌曲', '纯音乐']

con = sqlite3.connect('songs.db')
md = open('songs.md', 'w', encoding='utf-8')

for key in KEYS:
    md.write(f'## {key}\n\n')
    for lang in LANGS:
        md.write(f'### {lang}\n\n')
        songs = con.execute(
            'SELECT * FROM songs WHERE key = ? and lang = ?', (key, lang)
        ).fetchall()
        line_num = 1
        for song in songs:
            title, _, lang, artist, mod, ruby, src, lyric = song
            # 歌名（《出处》，歌手1[&歌手2]，“歌词”）『注音』【转调】
            line = f'{title}'
            detail = []
            if src:
                detail.append(f'《{src}》')
            if artist:
                detail.append(f'{artist}')
            if lyric:
                detail.append(f'“{lyric}”')
            if detail:
                line += f' ({", ".join(detail)})'
            if ruby:
                line += f'『{ruby}』'
            if mod:
                line += f'【{mod}】'
            md.write(f'{line_num}. {line}\n')
            line_num += 1
        md.write('\n')

md.close()
con.close()
