#!/usr/bin/env python3
"""爬取复旦百科人物及出生年份，保存为 data/people.json"""
import json
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.fudan.edu.cn/427/list.htm"
SITE_BASE = "https://www.fudan.edu.cn"


def extract_birth_from_text(text: str):
    if not text:
        return None
    # 优先匹配形如 (1918—1994) 或 （1918—1994）或 1918—1994 的出生年份范围，取第一个年份
    m = re.search(r"[\(（]\s*(\d{4})\s*[—\-–]\s*\d{4}\s*[\)）]", text)
    if m:
        try:
            y = int(m.group(1))
            if 1800 <= y <= 2025:
                return y
        except Exception:
            pass

    m = re.search(r"(\d{4})\s*[—\-–]\s*\d{4}", text)
    if m:
        try:
            y = int(m.group(1))
            if 1800 <= y <= 2025:
                return y
        except Exception:
            pass

    # 匹配“出生于 1900”之类
    m = re.search(r"出生[于:：\s]*(\d{4})", text)
    if m:
        try:
            y = int(m.group(1))
            if 1800 <= y <= 2025:
                return y
        except Exception:
            pass

    # 回退到找第一个合理的四位数，但跳过明显的发布时间/日期或带有连字符/斜杠的日期
    for m in re.finditer(r"(\d{4})", text):
        try:
            y = int(m.group(1))
        except Exception:
            continue
        if not (1800 <= y <= 2025):
            continue
        start = max(0, m.start() - 10)
        end = min(len(text), m.end() + 10)
        ctx = text[start:end]
        # 如果附近包含连字符或斜杠，可能是日期（2019-04-26），跳过
        if re.search(r"\d{4}[-/]\d{1,4}", ctx):
            continue
        # 跳过与发布相关的上下文
        if re.search(r"publish|发布时间|publishTime|publish|publish_date", ctx, re.I):
            continue
        return y

    return None


def main():
    session = requests.Session()
    # 添加重试策略，避免单次网络抖动导致全部失败
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    retries = Retry(total=3, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.mount('http://', HTTPAdapter(max_retries=retries))

    # 首先调用站点提供的内部 API 获取人物列表（columnId=427）
    api_url = "https://www.fudan.edu.cn/_wp3services/generalQuery?queryObj=articles&siteId=2&columnId=427&rows=1000"
    resp = session.get(api_url, timeout=10)
    resp.encoding = resp.apparent_encoding
    people = []
    seen = set()

    try:
        j = resp.json()
        items = j.get("data", [])
    except Exception:
        items = []

    for it in items:
        name = it.get("title")
        href = it.get("url") or it.get("wapUrl")
        if not name or not href:
            continue
        url = href if href.startswith("http") else urljoin(SITE_BASE, href)
        if name in seen:
            continue
        seen.add(name)

        # 直接抓取详情页，优先在姓名附近查找出生年份区间
        birth = None
        try:
            # 详情页使用较短超时以避免单个页面卡住整个过程
            r2 = session.get(url, timeout=5)
            r2.encoding = r2.apparent_encoding
            text2 = r2.text
            # 优先在姓名附近查找可能的出生-逝世年份区间，允许跨标签匹配
            pattern = re.compile(re.escape(name) + r"[\s\S]{0,300}?[\(（]\s*(\d{4})\s*[—\-–]\s*\d{4}\s*[\)）]")
            mname = pattern.search(text2)
            if mname:
                y = int(mname.group(1))
                if 1800 <= y <= 2025:
                    birth = y
            # 若仍未发现，再在整页中使用通用抽取（最后兜底可尝试摘要）
            if birth is None:
                birth = extract_birth_from_text(text2)
        except Exception:
            birth = None

        people.append({"name": name, "birth_year": birth, "url": url})
        time.sleep(0.05)

    # 保存数据
    import os

    os.makedirs("data", exist_ok=True)
    with open("data/people.json", "w", encoding="utf-8") as f:
        json.dump(people, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(people)} entries to data/people.json")


if __name__ == "__main__":
    main()
