# bili-hot · B 站热门视频采集器

一个用 Python 写的命令行小工具：增量抓取 B 站热门视频，输出 CSV，可直接用 Excel 打开。

## 它能做什么

- 抓取热门榜（可指定页数），每页 20 条
- **增量**：先读已有 CSV，只追加新出现的视频，不重复
- 单页失败自动重试（指数退避），不会整轮白跑
- 日志同时输出到控制台和 `logs/run-YYYYMMDD.log`
- 可打包成单个 exe，在没有装 Python 的电脑上直接运行

## 快速开始

```bash
# 安装依赖
pip install requests

# 抓 3 页（默认）
python d4_incremental.py

# 抓 5 页，每页间隔 2 秒，输出到指定文件
python d4_incremental.py --pages 5 --delay 2 --output data/hot.csv

# 查看全部参数
python d4_incremental.py --help
```

## 打包成 exe

```bash
pip install pyinstaller
pyinstaller --onefile --name bili-hot --clean --noconfirm d4_incremental.py
```

产物在 `dist/bili-hot.exe`（约 10 MB）。

> 双击运行时会使用默认参数，结束后窗口会停住等回车，不会一闪就关。

## 参数

| 参数 | 简写 | 默认值 | 说明 |
|---|---|---|---|
| `--pages` | `-p` | 3 | 抓几页 |
| `--delay` | `-d` | 1.0 | 每页间隔秒数 |
| `--output` | `-o` | `data/bilibili_hot.csv` | CSV 输出路径 |

## 输出

`data/bilibili_hot.csv`，UTF-8 with BOM（Excel 双击不乱码）：

```
bvid,title,up主,分区,播放量,弹幕数,时长秒,点赞数,发布时间,链接
```

## 目录结构

```
py-tools/
├── d2_fetch.py          # 第一步：抓一页，打印
├── d3_collect.py        # 第二步：多页 + 去重 + 存 CSV
├── d4_incremental.py    # 第三步：增量 + 重试 + 日志 + 参数化（主程序）
├── data/                # CSV 输出
├── logs/                # 运行日志
└── dist/                # 打包产物（不提交到 Git）
```

## 设计说明

**为什么用原子写入**：`open("w")` 会立刻清空原文件，若写入中途异常，历史数据全部丢失。这里先写 `.tmp`，成功后再 `replace` 覆盖，失败时原文件完好。

**为什么按 `bvid` 去重**：B 站视频的唯一标识，标题和播放量都会变，只有 `bvid` 稳定。

**为什么每页停 1 秒**：控制请求频率，避免给对方服务器造成压力，也降低被限流的概率。

## 免责声明

本工具仅用于个人学习与数据分析，抓取的是 B 站公开接口数据。使用时请遵守目标站点的服务条款与 robots 协议，控制请求频率，不要用于商业用途或大规模数据采集。

## 环境

- Python 3.12
- requests
- PyInstaller（仅打包时需要）
