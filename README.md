# 歌曲调位总结

## 当前进度

对应知乎专栏文章：[有关歌曲调号的分布的简单统计与分析](https://zhuanlan.zhihu.com/p/56102065)

```
Key   Total(percent)      Chinese        Foreign       Instrumental
-------------------------------------------------------------------
C      124 (11.58%)     57 ( 9.63%)     33 ( 5.57%)     34 ( 5.74%)
C#      50 ( 4.67%)     30 ( 5.07%)     10 ( 1.69%)     10 ( 1.69%)
D      126 (11.76%)     67 (11.32%)     47 ( 7.94%)     12 ( 2.03%)
D#      94 ( 8.78%)     58 ( 9.80%)     26 ( 4.39%)     10 ( 1.69%)
E      109 (10.18%)     58 ( 9.80%)     43 ( 7.26%)      8 ( 1.35%)
F       91 ( 8.50%)     54 ( 9.12%)     23 ( 3.89%)     14 ( 2.36%)
F#      61 ( 5.70%)     31 ( 5.24%)     24 ( 4.05%)      6 ( 1.01%)
G      136 (12.70%)     84 (14.19%)     26 ( 4.39%)     26 ( 4.39%)
G#      65 ( 6.07%)     34 ( 5.74%)     24 ( 4.05%)      7 ( 1.18%)
A       85 ( 7.94%)     53 ( 8.95%)     26 ( 4.39%)      6 ( 1.01%)
A#      71 ( 6.63%)     34 ( 5.74%)     22 ( 3.72%)     15 ( 2.53%)
B       59 ( 5.51%)     32 ( 5.41%)     21 ( 3.55%)      6 ( 1.01%)
-------------------------------------------------------------------
Total      1071              592           325             154
```

![](result.png)

## 脚本使用方法

歌曲调号首先会被记录在 `歌曲调号总结.md` 中。如果需要进行分析及可视化，可以先将其转为 `.json` 文件：

```shell
python md2json.py
```

然后，可以运行 `visualize.py` 进行数据的进一步分析，包括生成 readme 文件中的表格，以及观察扇形图。
