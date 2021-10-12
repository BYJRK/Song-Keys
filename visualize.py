import json
import sqlite3
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table

LABELS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def load_sql(filename='songs.json'):
    con = sqlite3.connect('songs.db')
    langs = ['国%', '外%', '纯%']
    data = {
        'total': {
            'all': con.execute("SELECT COUNT(title) FROM songs").fetchone()[0],
            'chn': con.execute(
                f"SELECT COUNT(title) FROM songs WHERE lang LIKE '{langs[0]}'"
            ).fetchone()[0],
            'for': con.execute(
                f"SELECT COUNT(title) FROM songs WHERE lang LIKE '{langs[1]}'"
            ).fetchone()[0],
            'ins': con.execute(
                f"SELECT COUNT(title) FROM songs WHERE lang LIKE '{langs[2]}'"
            ).fetchone()[0],
        },
        'count': {},
    }

    for key in LABELS:
        data['count'][key] = [
            con.execute(
                "SELECT COUNT(title) FROM songs WHERE lang LIKE (?) AND key= (?)",
                (lang, key),
            ).fetchone()[0]
            for lang in langs
        ]

    return data


def pie_chart(songs):
    fig, ax = plt.subplots()
    ax.pie(
        [sum(songs['count'][key]) for key in LABELS],
        labels=LABELS,
        autopct='%1.1f%%',
        explode=[0.1, 0, 0.1, 0, 0.1, 0, 0, 0.1, 0, 0, 0, 0],
    )
    ax.axis('equal')
    plt.show()
    fig.savefig('result.png')


def rich_table(songs):
    table = Table(show_header=True)
    table.add_column('Key', style='bold')
    table.add_column('Total(percent)', justify='right')
    table.add_column('Chinese', justify='right')
    table.add_column('Foreign', justify='right')
    table.add_column('Instrumental', justify='right')

    total = songs['total']['all']
    ctotal = songs['total']['chn']
    ftotal = songs['total']['for']
    itotal = songs['total']['ins']
    for key in LABELS:
        ss = sum(songs['count'][key])
        sp = float(ss) / total
        chn, frn, ins = songs['count'][key]
        cp, fp, ip = float(chn) / ctotal, float(frn) / ctotal, float(ins) / ctotal
        table.add_row(
            f'{key}',
            f'{ss:>5} ({sp*100:>5.2f}%)',
            f'{chn:>6} ({cp*100:>5.2f}%)',
            f'{frn:>6} ({fp*100:>5.2f}%)',
            f'{ins:>6} ({ip*100:>5.2f}%)',
            end_section=key == 'B',
        )
    table.add_row(
        'Total', str(total), str(ctotal), str(ftotal), str(itotal), style='bold'
    )
    console = Console()
    console.print(table)


def main():
    songs = load_sql()
    pie_chart(songs)
    rich_table(songs)


if __name__ == '__main__':
    main()
