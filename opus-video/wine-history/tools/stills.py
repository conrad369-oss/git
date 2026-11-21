#!/usr/bin/env python3
"""Render several stills of a render(t) page in one browser session and tile them.
usage: stills.py page.html out.png t1 t2 ... [--cols 3] [--scale 0.5]"""
import argparse, io, pathlib, subprocess, tempfile

from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("page"); ap.add_argument("out"); ap.add_argument("times", nargs="+", type=float)
ap.add_argument("--cols", type=int, default=3); ap.add_argument("--scale", type=float, default=0.5)
a = ap.parse_args()
with tempfile.TemporaryDirectory() as td, sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto(pathlib.Path(a.page).resolve().as_uri())
    pg.wait_for_function("typeof window.render === 'function' && window.ready === true", timeout=60000)
    files = []
    for k, t in enumerate(a.times):
        pg.evaluate("t => window.render(t)", t)
        f = f"{td}/{k:03d}.png"; pg.screenshot(path=f); files.append(f)
    b.close()
    w = int(1920 * a.scale); rows = -(-len(files) // a.cols)
    inputs = sum([["-i", f] for f in files], [])
    n = len(files)
    filt = "".join(f"[{k}:v]scale={w}:-1,drawtext=text='{a.times[k]:.2f}s':x=10:y=10:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.6[v{k}];" for k in range(n))
    layout = "|".join(f"{(k % a.cols) * w}_{(k // a.cols) * int(1080 * a.scale)}" for k in range(n))
    filt += "".join(f"[v{k}]" for k in range(n)) + (f"xstack=inputs={n}:layout={layout}:fill=black" if n > 1 else "null")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", filt, "-frames:v", "1", a.out], check=True)
print(a.out)
