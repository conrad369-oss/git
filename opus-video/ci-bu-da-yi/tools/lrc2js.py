#!/usr/bin/env python3
"""Convert an .lrc file into source/lyrics.js (window.LYRICS = [[t, text], ...]); credit lines (含「：」) are skipped.
usage: lrc2js.py source/lyrics.lrc source/lyrics.js"""
import json, re, sys
rows = []
for line in open(sys.argv[1], encoding="utf-8"):
    m = re.match(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)", line.strip())
    if not m: continue
    t, text = int(m[1]) * 60 + float(m[2]), m[3].strip()
    if not text or "：" in text or " - " in text: continue
    rows.append([round(t, 2), text])
open(sys.argv[2], "w", encoding="utf-8").write("window.LYRICS = " + json.dumps(rows, ensure_ascii=False) + ";\n")
print(f"{len(rows)} lines -> {sys.argv[2]}")
