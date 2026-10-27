#!/usr/bin/env python3
"""Generates dark_mode.svg (neofetch-style card) from photo.jpg + live GitHub stats."""
import json, os, subprocess, urllib.request
from html import escape
from PIL import Image, ImageOps, ImageEnhance

USER = "shadymansour19"

def token():
    if os.environ.get("GH_TOKEN"): return os.environ["GH_TOKEN"]
    try:
        out = subprocess.run(["git", "credential", "fill"], input="protocol=https\nhost=github.com\n\n",
                             capture_output=True, text=True, timeout=10).stdout
        return next((l[9:] for l in out.splitlines() if l.startswith("password=")), "")
    except Exception:
        return ""

def api(path, tok):
    req = urllib.request.Request("https://api.github.com" + path)
    if tok: req.add_header("Authorization", "token " + tok)
    with urllib.request.urlopen(req, timeout=15) as r: return json.load(r)

try:
    tok = token(); u = api(f"/users/{USER}", tok)
    repos = api(f"/users/{USER}/repos?per_page=100", tok)
    REPOS, FOLLOWERS = u["public_repos"], u["followers"]
    STARS = sum(r["stargazers_count"] for r in repos)
except Exception as e:
    print("stats fetch failed:", e); REPOS, STARS, FOLLOWERS = 17, 0, 6
print(f"Repos={REPOS} Stars={STARS} Followers={FOLLOWERS}")

# ---------- colored ASCII portrait ----------
img = Image.open("photo.jpg").convert("RGB")
w, h = img.size
img = img.crop((int(w*.13), int(h*.06), int(w*.87), int(h*.80)))
img = ImageEnhance.Contrast(img).enhance(1.2)
img = ImageEnhance.Color(img).enhance(1.35)
AW = 76
AH = int(AW * img.height / img.width * 0.5)
small = img.resize((AW, AH), Image.LANCZOS)
gray = ImageOps.grayscale(small)
RAMP = "%#@&8B$MW"
def lift(c): return tuple(int(38 + v * 0.88) for v in c)
AFS, ALH = 9, 9.6
AX, AY = 18, 24
art = []
for y in range(AH):
    runs, prev, buf = [], None, ""
    for x in range(AW):
        r, g, b = small.getpixel((x, y)); lum = gray.getpixel((x, y))
        if lum > 205 and max(r, g, b) - min(r, g, b) < 28:
            ch, col = " ", None
        else:
            ch = RAMP[(x * 7 + y * 3) % len(RAMP)]
            q = tuple(min(255, v // 8 * 8) for v in lift((r, g, b))); col = "#%02x%02x%02x" % q
        if col != prev and buf:
            runs.append((prev, buf)); buf = ""
        prev = col; buf += ch
    if buf: runs.append((prev, buf))
    while runs and runs[-1][0] is None: runs.pop()
    parts = "".join(f'<tspan fill="{c}">{escape(s)}</tspan>' if c else escape(s) for c, s in runs)
    art.append(f'<tspan x="{AX}" y="{AY + y*ALH:.1f}">{parts}</tspan>')

# ---------- info column ----------
TFS, TLH, TX, TCW, KEYCOLS, LINE = 14, 21, 440, 8.4, 27, 58
VX = TX + KEYCOLS * TCW
rows = [("title", "shady@mansour"),
 ("OS", "Ubuntu 24.04, Windows 11, Android"), ("Uptime", "26 years"), ("Host", "Rashpetco"),
 ("Kernel", "I&C and Network Engineer"), ("IDE", "VS Code, Qt Creator, STM32CubeIDE"), ("", ""),
 ("Languages.Programming", "C, C++, Python, JavaScript"), ("Languages.HDL", "Verilog, VHDL"),
 ("Languages.Computer", "HTML, CSS, SQL, JSON, YAML"), ("Languages.Real", "Arabic, English"), ("", ""),
 ("Hobbies.Software", "PyQt6 Apps, Web Apps"), ("Hobbies.Hardware", "STM32, ARM, FreeRTOS, ESP"),
 ("Industrial", "Mark VIe, PCS7, HIMatrix, Bently"), ("", ""),
 ("section", "Contact"), ("Email", "shadymansour19@gmail.com"), ("LinkedIn", "shadymansour19"),
 ("Upwork", "~01798d29b8076093d9"), ("LeetCode", "shadymansour19"), ("", ""),
 ("section", "GitHub Stats"), ("Repos", str(REPOS)), ("Stars", str(STARS)), ("Followers", str(FOLLOWERS))]
info, y = [], AY + 4
for k, v in rows:
    t = f'x="{TX}" y="{y}"'
    if k == "title":
        info.append(f'<tspan {t} class="key">{v}</tspan><tspan class="dim"> {"-"*(LINE-len(v)-1)}</tspan>')
    elif k == "section":
        info.append(f'<tspan {t} class="dim">- </tspan><tspan class="key">{v}</tspan><tspan class="dim"> {"-"*(LINE-len(v)-3)}</tspan>')
    elif k == "":
        info.append(f'<tspan {t} class="dim">.</tspan>')
    else:
        dots = KEYCOLS - len(k) - 6
        info.append(f'<tspan {t} class="dim">. </tspan><tspan class="key">{k}</tspan>:'
                    f'<tspan class="dim"> {"."*dots}</tspan><tspan x="{VX:.0f}" class="val">{escape(v)}</tspan>')
    y += TLH

W = 1000; H = int(max(AY + AH*ALH, y)) + 10
svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xml:space="preserve" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Consolas,'DejaVu Sans Mono','Liberation Mono','Courier New',monospace">
<style>
.key{{fill:#ffa657}} .val{{fill:#a5d6ff}} .dim{{fill:#616e7f}} .bg{{fill:#161b22}} .base{{fill:#c9d1d9}}
@media (prefers-color-scheme: light){{.bg{{fill:#f6f8fa}} .key{{fill:#953800}} .val{{fill:#0a3069}} .dim{{fill:#9aa7b5}} .base{{fill:#24292f}}}}
</style>
<rect class="bg" width="{W}" height="{H}" rx="15"/>
<text font-size="{AFS}px" font-weight="bold">
{chr(10).join(art)}
</text>
<text class="base" font-size="{TFS}px">
{chr(10).join(info)}
</text>
</svg>
'''
open("dark_mode.svg", "w").write(svg)
print(f"dark_mode.svg written ({len(svg)//1024} KB)")
