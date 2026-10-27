#!/usr/bin/env python3
"""Generates card.svg (neofetch-style card) from photo.jpg + live GitHub stats."""
import json, os, subprocess, urllib.request
from html import escape
from PIL import Image, ImageOps, ImageFilter

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

# ---------- ASCII portrait ----------
img = Image.open("photo.jpg").convert("L")
w, h = img.size
img = img.crop((int(w*.10), int(h*.07), int(w*.90), int(h*.72)))
img = ImageOps.autocontrast(img, cutoff=1)
img = img.filter(ImageFilter.GaussianBlur(1.5))
AW = 50
AH = int(AW * img.height / img.width * 0.5)
small = img.resize((AW, AH), Image.LANCZOS)
RAMP = "@%#*+=-:. "
AFS, ALH = 12.5, 14
rows_txt = ["".join(RAMP[min(len(RAMP)-1, small.getpixel((x, y)) * len(RAMP) // 256)] for x in range(AW)).rstrip()
            for y in range(AH)]
while rows_txt and not rows_txt[0].strip(): rows_txt.pop(0)
while rows_txt and not rows_txt[-1].strip(): rows_txt.pop()

# ---------- info column ----------
AY = 24
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

W = 1000; H = int(max(len(rows_txt)*ALH + 2*AY, y)) + 10
CW = AFS * 0.6
AX = max(10, (TX - 20 - AW * CW) / 2)
AY0 = (H - (len(rows_txt) - 1) * ALH) / 2 + AFS * 0.35
art = [f'<tspan x="{AX:.1f}" y="{AY0 + i*ALH:.1f}">{escape(r).replace(" ", "&#160;")}</tspan>' for i, r in enumerate(rows_txt)]
svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xml:space="preserve" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Consolas,'DejaVu Sans Mono','Liberation Mono','Courier New',monospace">
<style>
.key{{fill:#ffa657}} .val{{fill:#a5d6ff}} .dim{{fill:#616e7f}} .bg{{fill:#161b22}} .base{{fill:#c9d1d9}} text,tspan{{white-space:pre}}
@media (prefers-color-scheme: light){{.bg{{fill:#f6f8fa}} .key{{fill:#953800}} .val{{fill:#0a3069}} .dim{{fill:#9aa7b5}} .base{{fill:#24292f}}}}
</style>
<rect class="bg" width="{W}" height="{H}" rx="15"/>
<text class="base" font-size="{AFS}px">
{chr(10).join(art)}
</text>
<text class="base" font-size="{TFS}px">
{chr(10).join(info)}
</text>
</svg>
'''
open("card.svg", "w").write(svg)
print(f"card.svg written ({len(svg)//1024} KB)")
