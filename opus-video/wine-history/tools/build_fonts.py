#!/usr/bin/env python3
"""Copy only the @fontsource woff2 chunks needed for the given text into fonts/ and write fonts/fonts.css.

usage: build_fonts.py <fontsource_root> <text_file> <out_dir>
fontsource_root holds extracted packages: <root>/fontsource-<name>-<ver>/package/
"""
import pathlib, re, shutil, sys

WANT = [  # (package dir prefix, weight)
    ("fontsource-noto-sans-sc", 400), ("fontsource-noto-sans-sc", 900),
    ("fontsource-noto-serif-sc", 400), ("fontsource-noto-serif-sc", 900),
    ("fontsource-zcool-kuaile", 400), ("fontsource-zcool-qingke-huangyou", 400),
]

root, text_file, out = map(pathlib.Path, sys.argv[1:4])
chars = {ord(c) for c in text_file.read_text(encoding="utf-8")} | set(range(0x20, 0x7F))
(out / "files").mkdir(parents=True, exist_ok=True)


def covers(rng):
    for part in rng.split(","):
        part = part.strip().upper().replace("U+", "")
        a, _, b = part.partition("-")
        lo, hi = int(a, 16), int(b or a, 16)
        if any(lo <= c <= hi for c in chars):
            return True
    return False


css = []
for prefix, w in WANT:
    pkg = next(root.glob(prefix + "-*")) / "package"
    src = (pkg / f"{w}.css").read_text()
    for block in re.findall(r"@font-face\s*{[^}]*}", src):
        rng = re.search(r"unicode-range:\s*([^;]+);", block)
        if rng and not covers(rng.group(1)):
            continue
        f = re.search(r"url\(\./files/([^)]+\.woff2)\)", block).group(1)
        shutil.copy(pkg / "files" / f, out / "files" / f)
        block = re.sub(r"src:[^;]+;", f"src: url(./files/{f}) format('woff2');", block)
        css.append(block.replace("font-display: swap;", "font-display: block;"))
(out / "fonts.css").write_text("\n".join(css) + "\n")
print(f"{len(css)} chunks -> {out}/fonts.css")
