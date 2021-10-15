import sqlite3
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table

LABELS = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']


def pie_chart(cur: sqlite3.Cursor) -> None:
    fig, ax = plt.subplots()

    counts = [
        line[0]
        for line in cur.execute(
            'select count(key) from songs group by key order by key'
        ).fetchall()
    ]

    ax.pie(
        counts,
        labels=LABELS,
        autopct='%1.1f%%',
        explode=[0, 0, 0, 0.1, 0, 0.1, 0, 0.1, 0, 0, 0.1, 0],
    )
    ax.axis('equal')
    plt.show()
    fig.savefig('result.png')


def rich_table(cur: sqlite3.Cursor) -> None:
    table = Table(show_header=True)
    table.add_column('Key', style='bold')
    table.add_column('Total(percent)', justify='right')
    table.add_column('Chinese', justify='right')
    table.add_column('Foreign', justify='right')
    table.add_column('Instrumental', justify='right')

    total = cur.execute('select count(title) from songs').fetchone()[0]
    chn_count, for_count, ins_count = [
        line[0]
        for line in cur.execute(
            'select count(title) from songs group by lang'
        ).fetchall()
    ]

    for key in LABELS:
        key_total = cur.execute(
            'select count(title) from songs where key = (?)', (key,)
        ).fetchone()[0]
        key_percent = float(key_total) / total
        chn, frn, ins = [
            line[0]
            for line in cur.execute(
                'select count(title) from songs where key = (?) group by lang', (key,)
            ).fetchall()
        ]
        cp, fp, ip = (
            float(chn) / chn_count,
            float(frn) / chn_count,
            float(ins) / chn_count,
        )
        table.add_row(
            f'{key}',
            f'{key_total:>5} ({key_percent*100:>5.2f}%)',
            f'{chn:>6} ({cp*100:>5.2f}%)',
            f'{frn:>6} ({fp*100:>5.2f}%)',
            f'{ins:>6} ({ip*100:>5.2f}%)',
            end_section=key == 'G#',
        )
    table.add_row('Total', str(total), str(chn_count), str(for_count), str(ins_count))
    console = Console()
    console.print(table)


def main():
    con = sqlite3.connect('songs.db')
    cur = con.cursor()

    pie_chart(cur)
    rich_table(cur)

    con.close()


if __name__ == '__main__':
    main()
