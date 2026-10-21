#!/usr/bin/env python3
"""把 parts/*.html 拼成 index.html，并把 assets/img/*.jpg 内联为 data URI。
用法：python3 build.py
"""
import base64, glob, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
PARTS = ["part-a-head.html", "part-b-p01-10.html", "part-c-p11-18.html",
         "part-d-p19-29.html", "part-e-p30-35-tail.html"]

html = "".join(open(os.path.join(ROOT, "parts", p), encoding="utf-8").read() for p in PARTS)

def inline(m):
    rel = m.group(1)
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        raise SystemExit(f"缺少素材：{rel}")
    data = base64.b64encode(open(path, "rb").read()).decode()
    return f'src="data:image/jpeg;base64,{data}"'

html, n = re.subn(r'src="(assets/img/[^"]+\.jpg)"', inline, html)

out = os.path.join(ROOT, "index.html")
open(out, "w", encoding="utf-8").write(html)
print(f"内联图片 {n} 张 · 输出 {out} · {os.path.getsize(out)/1024/1024:.2f} MB")
