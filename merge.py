# -*- coding: utf-8 -*-
"""
TVBox 订阅源自动合并与缓存降级工具
- 支持普通 JSON、Base64 以及图片隐写(图床源)自动解析
- 当网络失效、502 或超时时，自动降级使用上一次成功的缓存
- 为每个 site 绑定专属 jar，彻底解决多源 spider 爬虫冲突问题
- 站点与直播均打上 [饭]、[摸] 来源前缀，方便在电视上辨识
"""

import os
import re
import json
import base64
import urllib.request
import urllib.parse

SOURCES = [
    {
        "id": "fty",
        "tag": "饭",
        "url": "http://www.xn--sss604efuw.top/tv/",  # http://www.饭太硬.top/tv/
        "backup_urls": [
            "http://fty.888484.xyz/tv",
            "http://xn--sss604efuw.top/tv",
            "http://www.xn--sss604efuw.net/tv",
            "http://xn--sss604efuw.net/tv"
        ]
    },
    {
        "id": "my",
        "tag": "摸",
        "url": "http://xn--ihqu10cn4c.xn--v4q818bf34b.top/",  # http://我不是.摸鱼儿.top
        "backup_urls": []
    }
]

# 额外置顶的高清精品直播源（范明明超清 IPv6 央视/卫视）
EXTRA_LIVES = [
    {
        "name": "⭐ 范明明超清IPv6 (央视/卫视)",
        "type": 0,
        "url": "https://live.fanmingming.com/tv/m3u/ipv6.m3u",
        "playerType": 1
    }
]

CACHE_DIR = "./cache"
OUTPUT_FILE = "merged.json"

def strip_json_comments(text: str) -> str:
    """安全去除 JSON 中的注释（保留字符串与 URL 内的 //）并移除尾随逗号"""
    pattern = re.compile(r'(".*?"|//[^\r\n]*|/\*.*?\*/)', re.DOTALL)
    def replacer(match):
        s = match.group(0)
        return '' if s.startswith('/') else s
    cleaned = pattern.sub(replacer, text)
    cleaned = re.sub(r',\s*([\]}])', r'\1', cleaned)
    return cleaned.strip()

def parse_tvbox_payload(raw_bytes: bytes) -> dict:
    """自动兼容 TVBox 的 3 种格式：普通 JSON、Base64、图片隐写(**base64)"""
    try:
        text = raw_bytes.decode('utf-8', errors='ignore').lstrip('\ufeff').strip()
        cleaned = strip_json_comments(text)
        data = json.loads(cleaned)
        if isinstance(data, dict) and "sites" in data:
            return data
    except Exception:
        pass

    if b'**' in raw_bytes:
        try:
            b64_part = raw_bytes.split(b'**', 1)[1].strip()
            decoded = base64.b64decode(b64_part).decode('utf-8', errors='ignore').lstrip('\ufeff').strip()
            cleaned = strip_json_comments(decoded)
            data = json.loads(cleaned)
            if isinstance(data, dict) and "sites" in data:
                return data
        except Exception:
            pass

    try:
        decoded = base64.b64decode(raw_bytes.strip()).decode('utf-8', errors='ignore').lstrip('\ufeff').strip()
        cleaned = strip_json_comments(decoded)
        data = json.loads(cleaned)
        if isinstance(data, dict) and "sites" in data:
            return data
    except Exception:
        pass

    raise ValueError("未能识别出包含 sites 的 TVBox 配置")

def fetch_single_url(url: str, timeout: int = 10) -> dict:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "okhttp/3.15.0", "Accept": "*/*"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status == 200:
            return parse_tvbox_payload(resp.read())
    raise ValueError(f"HTTP 状态异常: {resp.status}")

def get_source_data(source_cfg: dict) -> tuple:
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f"{source_cfg['id']}.json")

    urls_to_try = [source_cfg["url"]] + source_cfg.get("backup_urls", [])
    fetched_data = None
    success_url = ""

    for u in urls_to_try:
        try:
            print(f"[{source_cfg['id']}] 正在尝试拉取: {u}")
            fetched_data = fetch_single_url(u)
            success_url = u
            print(f"[{source_cfg['id']}] -> 拉取最新成功! (包含 {len(fetched_data.get('sites', []))} 个站点)")
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(fetched_data, f, ensure_ascii=False, indent=2)
            break
        except Exception as e:
            print(f"[{source_cfg['id']}] -> 失败 ({u}): {e}")

    if fetched_data:
        return fetched_data, success_url

    if os.path.exists(cache_path):
        print(f"[{source_cfg['id']}] [FALLBACK] 上游均失败，自动降级使用本地历史缓存: {cache_path}")
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f), source_cfg["url"]
        except Exception as e:
            print(f"[{source_cfg['id']}] 本地缓存读取异常: {e}")

    print(f"[{source_cfg['id']}] [WARN] 该源无可用最新数据且无历史缓存，已跳过")
    return None, ""

def main():
    merged_sites = []
    seen_site_keys = set()
    merged_parses = []
    seen_parse_names = set()
    merged_lives = []
    seen_live_urls = set()
    merged_rules = []
    base_config = {}

    # 1. 优先加入高品质置顶直播源
    for l in EXTRA_LIVES:
        seen_live_urls.add(l["url"])
        merged_lives.append(l)

    for cfg in SOURCES:
        data, base_url = get_source_data(cfg)
        if not data:
            continue

        tag = cfg["tag"]
        source_spider = data.get("spider", "")
        if source_spider and base_url and not source_spider.startswith(("http://", "https://")):
            source_spider = urllib.parse.urljoin(base_url, source_spider)

        if not base_config:
            base_config = {
                "spider": source_spider,
                "wallpaper": data.get("wallpaper", ""),
                "logo": data.get("logo", ""),
                "danmaku": data.get("danmaku", ""),
                "ijk": data.get("ijk", [])
            }

        # 站点合并与 Jar 强绑定
        for site in data.get("sites", []):
            if not isinstance(site, dict):
                continue
            site_item = dict(site)
            orig_key = str(site_item.get("key", ""))
            orig_name = str(site_item.get("name", "未命名"))

            if not site_item.get("jar") and source_spider:
                site_item["jar"] = source_spider

            if site_item.get("api") and base_url and not str(site_item["api"]).startswith(("http://", "https://", "csp_")):
                site_item["api"] = urllib.parse.urljoin(base_url, site_item["api"])

            site_item["name"] = f"[{tag}] {orig_name}"
            unique_key = f"{cfg['id']}_{orig_key}"
            site_item["key"] = unique_key

            if unique_key not in seen_site_keys:
                seen_site_keys.add(unique_key)
                merged_sites.append(site_item)

        # 合并解析 parses
        for p in data.get("parses", []):
            if isinstance(p, dict):
                p_name = p.get("name", "")
                if p_name and p_name not in seen_parse_names:
                    seen_parse_names.add(p_name)
                    merged_parses.append(p)

        # 合并直播 lives
        for l in data.get("lives", []):
            if isinstance(l, dict):
                l_item = dict(l)
                l_url = l_item.get("url", "")
                if l_url and l_url not in seen_live_urls:
                    if base_url and not l_url.startswith(("http://", "https://")):
                        l_item["url"] = urllib.parse.urljoin(base_url, l_url)
                    orig_lname = l_item.get("name", "直播")
                    l_item["name"] = f"[{tag}] {orig_lname}"
                    seen_live_urls.add(l_url)
                    merged_lives.append(l_item)

        # 合并规则 rules
        for r in data.get("rules", []):
            merged_rules.append(r)

    if not base_config:
        print("[FATAL] 所有源均无法访问且无缓存可用，合并失败！")
        return

    base_config["sites"] = merged_sites
    base_config["parses"] = merged_parses
    base_config["lives"] = merged_lives
    base_config["rules"] = merged_rules

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(base_config, f, ensure_ascii=False, indent=2)

    print("\n" + "="*40)
    print("TVBox 站点与直播全量合并成功!")
    print(f"输出文件: {OUTPUT_FILE}")
    print(f"合并后站点总数: {len(merged_sites)} 个")
    print(f"合并后直播总数: {len(merged_lives)} 个")
    print("="*40)

if __name__ == "__main__":
    main()
