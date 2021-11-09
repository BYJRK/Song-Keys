# 歌曲调位总结

## 当前进度

对应知乎专栏文章：[有关歌曲调号的分布的简单统计与分析](https://zhuanlan.zhihu.com/p/56102065)

```
┏━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Key   ┃ Total(percent) ┃         Chinese ┃         Foreign ┃    Instrumental ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ A     │    84 ( 7.72%) │     52 ( 8.71%) │     26 ( 4.36%) │      6 ( 1.01%) │
│ A#    │    72 ( 6.62%) │     35 ( 5.86%) │     22 ( 3.69%) │     15 ( 2.51%) │
│ B     │    59 ( 5.42%) │     32 ( 5.36%) │     20 ( 3.35%) │      7 ( 1.17%) │
│ C     │   125 (11.49%) │     58 ( 9.72%) │     32 ( 5.36%) │     35 ( 5.86%) │
│ C#    │    51 ( 4.69%) │     31 ( 5.19%) │     10 ( 1.68%) │     10 ( 1.68%) │
│ D     │   129 (11.86%) │     67 (11.22%) │     50 ( 8.38%) │     12 ( 2.01%) │
│ D#    │    98 ( 9.01%) │     58 ( 9.72%) │     30 ( 5.03%) │     10 ( 1.68%) │
│ E     │   110 (10.11%) │     59 ( 9.88%) │     43 ( 7.20%) │      8 ( 1.34%) │
│ F     │    95 ( 8.73%) │     56 ( 9.38%) │     25 ( 4.19%) │     14 ( 2.35%) │
│ F#    │    62 ( 5.70%) │     31 ( 5.19%) │     25 ( 4.19%) │      6 ( 1.01%) │
│ G     │   139 (12.78%) │     85 (14.24%) │     27 ( 4.52%) │     27 ( 4.52%) │
│ G#    │    64 ( 5.88%) │     33 ( 5.53%) │     24 ( 4.02%) │      7 ( 1.17%) │
├───────┼────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Total │           1088 │             597 │             334 │             157 │
└───────┴────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

![](result.png)

## 脚本使用方法

从 2021 年 11 月 9 日开始，不再使用 Markdown 文档记录歌曲，而是全部记录在 sqlite 数据库文件（`songs.db`）中。推荐使用 [SQLite Browser](https://github.com/sqlitebrowser/sqlitebrowser) 对 `songs.db` 文件进行查看。

可以运行 `visualize.py` 进行数据的进一步分析，包括生成表格以及扇形图。

```shell
python visualize.py
```

如果想要查看以前的 Markdown 文件，除了可以在 commit 历史中找到，还可以运行 `sql2md.py` 来生成 Markdown 文档。

```shell
python sql2md.py
```

## 规则

* 按照国语歌曲、外语歌曲、纯音乐的顺序进行排序
* 按照歌曲主歌部分（而非前奏部分）的调号进行归纳
* 同一类别下按照英文名、中文名、日文名、其他（如数字、法语、韩语）的顺序进行排列
* 歌曲后面的备注分别为：（《出处》，歌手1[&歌手2]，“歌词”）『注音』【转调】
