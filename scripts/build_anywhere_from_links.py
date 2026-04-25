#!/usr/bin/env python3

import argparse
import urllib.request
import re
import json
from pathlib import Path
from collections import OrderedDict, defaultdict

# Anywhere:
# 0 = IPv4 CIDR
# 1 = IPv6 CIDR
# 2 = Domain Suffix
# 3 = Domain Keyword

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")

def dedupe(lst):
    return list(OrderedDict.fromkeys(lst))

def parse_links(text):
    result = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if "," in line:
            name, url = line.split(",", 1)
        elif "|" in line:
            name, url = line.split("|", 1)
        elif "=" in line:
            name, url = line.split("=", 1)
        else:
            name = url = line

        result.append((name.strip(), url.strip()))
    return result

def convert_line(line):
    line = line.strip()

    if not line or line.startswith("#"):
        return None

    # 去掉 no-resolve
    line = re.sub(r",\s*no-resolve", "", line, flags=re.I)

    parts = [p.strip() for p in line.split(",")]

    if len(parts) < 2:
        return None

    t, v = parts[0].upper(), parts[1]

    if t in ["DOMAIN", "DOMAIN-SUFFIX"]:
        return f"2, {v.lstrip('.')}"
    if t == "DOMAIN-KEYWORD":
        return f"3, {v}"
    if t == "IP-CIDR":
        return f"0, {v}"
    if t == "IP-CIDR6":
        return f"1, {v}"

    return None

def classify(rule):
    v = rule.lower()

    if any(x in v for x in ["apple", "icloud", "itunes", "mzstatic"]):
        return "apple"

    if any(x in v for x in ["openai", "chatgpt", "anthropic", "claude", "ai"]):
        return "ai"

    if any(x in v for x in ["ads", "tracker", "doubleclick"]):
        return "reject"

    if ".cn" in v:
        return "cn"

    return "proxy"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--links", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    links_text = Path(args.links).read_text(encoding="utf-8")
    sources = parse_links(links_text)

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    buckets = defaultdict(list)
    all_rules = []

    for name, url in sources:
        print(f"fetching {name}")
        try:
            content = fetch(url)
        except Exception as e:
            print("error:", e)
            continue

        rules = []
        for line in content.splitlines():
            r = convert_line(line)
            if r:
                rules.append(r)

        rules = dedupe(rules)

        # 单文件输出
        (outdir / f"{name}.txt").write_text("\n".join(rules), encoding="utf-8")

        for r in rules:
            buckets[classify(r)].append(r)

        all_rules.extend(rules)

    # 分类输出
    for k in ["apple", "ai", "cn", "proxy", "reject"]:
        lst = dedupe(buckets[k])
        (outdir / f"{k}.txt").write_text("\n".join(lst), encoding="utf-8")

    # all
    all_rules = dedupe(all_rules)
    (outdir / "all.txt").write_text("\n".join(all_rules), encoding="utf-8")

    # index
    index = {
        "apple": "rule/apple.txt",
        "ai": "rule/ai.txt",
        "cn": "rule/cn.txt",
        "proxy": "rule/proxy.txt",
        "reject": "rule/reject.txt",
        "all": "rule/all.txt"
    }

    (outdir / "index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")

    print("done")

if __name__ == "__main__":
    main()
