r"""
D2：抓第一个公开接口，打印前 3 条。

在 VS Code 里打开 py-tools 文件夹后，右键 → Run Python File，
或者在终端里执行：python d2_fetch.py
"""

import json

import requests

# 1. 请求头：这个 UA 不是可选的，是必须的。
#    很多站点会检查 User-Agent，不带或乱写会被直接拒绝（B 站返回 -352）。
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.bilibili.com/",
}

URL = "https://api.bilibili.com/x/web-interface/popular"


def fetch(page: int = 1, page_size: int = 3) -> dict:
    """请求一页数据，返回 JSON。"""
    params = {"ps": page_size, "pn": page}

    # timeout 一定要写。不写的话，网络卡住时程序会永远挂着。
    resp = requests.get(URL, params=params, headers=HEADERS, timeout=10)

    # raise_for_status 会在 4xx / 5xx 时抛异常，避免把错误页当数据解析
    resp.raise_for_status()

    # 网站声明了编码就用网站的，没声明就用 requests 的猜测
    resp.encoding = resp.apparent_encoding if not resp.encoding else resp.encoding

    return resp.json()


def main() -> None:
    data = fetch(page=1, page_size=3)

    # 2. 接口返回通常有两层：外层的 code/message，内层的 data
    print(f"外层字段: {list(data.keys())}")
    print(f"返回码 code = {data.get('code')}  message = {data.get('message')}")
    print()

    items = data["data"]["list"]
    print(f"本次拿到 {len(items)} 条\n")

    for i, item in enumerate(items, start=1):
        title = item.get("title", "")
        owner = item.get("owner", {}).get("name", "")
        view = item.get("stat", {}).get("view", 0)
        bvid = item.get("bvid", "")
        print(f"{i}. {title}")
        print(f"   UP主: {owner}   播放: {view:,}   BV号: {bvid}")

    # 3. 第一次接触一个接口时，先把它的一条数据的结构打印出来，
    #    比看文档快得多。后面写工具就是从这个结构里挑字段。
    print("\n第一条数据的字段（部分）:")
    first = items[0]
    for key in list(first.keys())[:12]:
        value = first[key]
        preview = str(value)[:60]
        print(f"  {key}: {type(value).__name__} = {preview}")


if __name__ == "__main__":
    main()
