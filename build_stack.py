import os, glob
def local(key):
    f = sorted(glob.glob(f"assets/logos/{key}.*")); return f[0] if f else None
def cell(label, imgs=(), w=90, h=40):
    imgs = [i for i in imgs if i]
    tags = "&nbsp;".join(f'<img src="{s}" height="{h}" alt="{label}"/>' for s in imgs)
    return f'<td align="center" width="{w}">{tags + "<br>" if tags else "<br><br>"}<sub>{label}</sub></td>'
SK = "https://skillicons.dev/icons?i="; SI = "https://cdn.simpleicons.org/"; DV = "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/"
groups = [
 ("Core", [cell(n, [u]) for n, u in [("C",SK+"c"),("C++",SK+"cpp"),("Python",SK+"py"),("STM32",SI+"stmicroelectronics/3CB4E6"),
   ("Arduino",SK+"arduino"),("VS Code",SK+"vscode"),("Qt",SK+"qt"),("PostgreSQL",SK+"postgres"),("Supabase",SK+"supabase")]]),
 ("Embedded &amp; HDL", [cell("ARM<br>Cortex-M",[SI+"arm/0091BD"]), cell("Embedded C",[DV+"embeddedc/embeddedc-original.svg"]),
   cell("FreeRTOS",[local("freertos")]), cell("ESP8266",[SI+"espressif/E7352C"]), cell("AVR MCU",[local("microchip")]),
   cell("Verilog",[DV+"verilog/verilog-original.svg"]), cell("VHDL",[local("vhdl")]),
   cell("CAN · I²C · SPI · UART",[local("can"), local("i2c")], w=140, h=32)]),
 ("Industrial &amp; networking", [cell("GE Mark VIe",[SI+"generalelectric/3B8FE0"],120), cell("PCS7 / TIA Portal",[SI+"siemens/009999"],120),
   cell("Studio 5000",[SI+"rockwellautomation/CD163F"],120), cell("Bently Nevada<br>3500",[local("bently")],120),
   cell("HIMatrix SIS",[local("hima")],120), cell("Det-Tronics<br>F&amp;G",[local("dettronics")],120),
   cell("PROFIBUS · Modbus",[local("profibus"), local("modbus")],140,32), cell("Cisco · VLANs",[SI+"cisco/1BA0D7"],120)]),
 ("OS &amp; tools", [cell(n,[SK+i]) for n,i in [("Linux","linux"),("Ubuntu","ubuntu"),("Windows","windows"),("Bash","bash"),("Git","git"),("GitHub","github")]]),
 ("Web", [cell(n,[SK+i]) for n,i in [("JavaScript","js"),("HTML","html"),("CSS","css"),("Node.js","nodejs"),("React","react"),("Vercel","vercel"),("Netlify","netlify")]]),
]
sec = "### 🛠️ Tech stack\n\n" + "".join(f"**{t}**\n<table><tr>\n" + "\n".join(c) + "\n</tr></table>\n\n" for t, c in groups) + "---\n\n"
s = open("README.md").read(); a = s.index("### 🛠️ Tech stack"); b = s.index("### 🚀 Featured projects")
open("README.md", "w").write(s[:a] + sec + s[b:]); print("✅ tech stack rebuilt")
