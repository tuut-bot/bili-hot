import requests

import sys

import csv

import argparse

from pathlib import Path

COLUMNS = ["bvid", "标题", "播放量"]

parser = argparse.ArgumentParser(description="B站热门视频采集器")
parser.add_argument("-p", "--pages", type=int, default=3, help="抓几页，默认 3")
args = parser.parse_args()
url = "https://api.bilibili.com/x/web-interface/popular"
headers = {"User-Agent":"Mozilla/5.0"}

params = {"ps":3,"pn":3}

resp = requests.get(url,params=params,headers=headers,timeout=10)
# resp = requests.get(url,headers=headers,timeout=10)

print("实际地址：",resp.url)
data = resp.json()

# print("返回码",data["code"])
# print("第一条标题",data["data"]["list"][0]["title"])
# print("状态码:", resp.status_code)
# print("内容类型:", resp.headers["Content-Type"])
# print("这页有几条:", len(data["data"]["list"]))
# print("第二条标题:", data["data"]["list"][1]["title"])

# for item in data["data"]["list"][:3]:
#     print(item["title"],"|",item["stat"]["view"])

def save_titles(items, filename="mini.csv"):
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["bvid","标题","播放量"])
            for item in items:
                writer.writerow([item["bvid"],item["title"],item["stat"]["view"]])

def load_existing(filename):
    #  """读旧数据，返回（旧的所有行, 旧的 bvid 集合）。文件不存在就返回空的。"""
     if not Path(filename).exists():
          return[],set()
     with open(filename,"r",newline="",encoding="utf-8-sig") as f:
          rows = list(csv.DictReader(f))
     # print("这是你想要的：",{r["bvid"] for r in rows if r.get("bvid")})
     # print("这是你想要的：",rows)
     return rows,{r["bvid"] for r in rows if r.get("bvid")}


def save_rows(rows,filename):
    #   """整体写回：旧数据 + 新数据。"""
     with open(filename,"w",newline="",encoding="utf-8-sig") as f:
          writer = csv.DictWriter(f,fieldnames=COLUMNS)
          writer.writeheader()
          writer.writerows(rows)

all_items= [] 
# seen = set()
old_rows, seen = load_existing("mini9.csv")

for page in range(1,args.pages + 1):
    params = {"ps": 3, "pn": page}
    resp = requests.get(url,params=params,headers=headers,timeout=10)
    data = resp.json()
    items = data["data"]["list"]
    print(f"第{page}页拿到{len(items)}条")
    for item in items:
        bvid = item["bvid"]
        if bvid in seen:
             continue
        seen.add(bvid)
        all_items.append({
             "bvid":item["bvid"],
             "标题": item["title"],
             "播放量": item["stat"]["view"],
        })
    

     
print("总共：",len(all_items),"条")

# save_titles(all_items,"mini9.csv")

print("原有：",len(old_rows),"条；本次新增:", len(all_items), "条")

if all_items:
     # print("22222",old_rows + all_items)
     save_rows(old_rows + all_items, "mini9.csv")
     print("已写回，累计:", len(old_rows) + len(all_items), "条")
else:
     print("没有新数据，文件保持不动")

if len(sys.argv) == 1:
     input("按回车键推出...")