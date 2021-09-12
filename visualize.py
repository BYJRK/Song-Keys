import json
import matplotlib.pyplot as plt

LABELS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def load_json(filename='songs.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def pie(songs):
    fig, ax = plt.subplots()
    ax.pie(
        [len([s for s in songs if s['key'] == l]) for l in LABELS],
        labels=LABELS,
        autopct='%1.1f%%',
        explode=[0.1, 0, 0.1, 0, 0.1, 0, 0, 0.1, 0, 0, 0, 0],
    )
    ax.axis('equal')
    plt.show()
    fig.savefig('result.png')


def table(songs):
    """
    Key   Total(percent)      Chinese        Foreign       Instrumental
    -------------------------------------------------------------------
    C      124 (11.69%)     57 ( 9.79%)     33 (10.15%)     34 (22.08%)
    C#      49 ( 4.62%)     29 ( 4.98%)     10 ( 3.08%)     10 ( 6.49%)
    D      126 (11.88%)     67 (11.51%)     47 (14.46%)     12 ( 7.79%)
    D#      94 ( 8.86%)     58 ( 9.97%)     26 ( 8.00%)     10 ( 6.49%)
    E      108 (10.18%)     57 ( 9.79%)     43 (13.23%)      8 ( 5.19%)
    F       90 ( 8.48%)     53 ( 9.11%)     23 ( 7.08%)     14 ( 9.09%)
    F#      61 ( 5.75%)     31 ( 5.33%)     24 ( 7.38%)      6 ( 3.90%)
    G      135 (12.72%)     83 (14.26%)     26 ( 8.00%)     26 (16.88%)
    G#      63 ( 5.94%)     32 ( 5.50%)     24 ( 7.38%)      7 ( 4.55%)
    A       84 ( 7.92%)     52 ( 8.93%)     26 ( 8.00%)      6 ( 3.90%)
    A#      70 ( 6.60%)     33 ( 5.67%)     22 ( 6.77%)     15 ( 9.74%)
    B       57 ( 5.37%)     30 ( 5.15%)     21 ( 6.46%)      6 ( 3.90%)
    -------------------------------------------------------------------
    Total      1061              582           325             154
    """
    total = len(songs)
    ctotal = len([s for s in songs if s['lang'] == '国语歌曲'])
    ftotal = len([s for s in songs if s['lang'] == '外语歌曲'])
    itotal = len([s for s in songs if s['lang'] == '纯音乐'])
    res = "Key   Total(percent)      Chinese        Foreign       Instrumental\n"
    res += '-' * 67 + '\n'
    for key in LABELS:
        ss = [s for s in songs if s['key'] == key]
        sp = float(len(ss)) / total
        chn = [s for s in ss if s['lang'] == "国语歌曲"]
        cp = float(len(chn)) / ctotal
        frn = [s for s in ss if s['lang'] == "外语歌曲"]
        fp = float(len(frn)) / ctotal
        ins = [s for s in ss if s['lang'] == "纯音乐"]
        ip = float(len(ins)) / ctotal
        res += f'{key:<4} '
        res += f'{len(ss):>5} ({sp*100:>5.2f}%) '
        res += f'{len(chn):>6} ({cp*100:>5.2f}%) '
        res += f'{len(frn):>6} ({fp*100:>5.2f}%) '
        res += f'{len(ins):>6} ({ip*100:>5.2f}%)\n'
    res += '-' * 67 + '\n'
    res += f'Total     {total:>5}            {ctotal:>5}         {ftotal:>5}           {itotal:>5}\n'

    print(res)


def main():
    songs = load_json()
    pie(songs)
    table(songs)


if __name__ == '__main__':
    main()
