import glob
def local(key):
    f = sorted(glob.glob(f"assets/logos/{key}.*")); return f[0] if f else None
def cell(label, imgs=(), w=90, h=40):
    imgs = [i for i in imgs if i]
    tags = "&nbsp;".join(f'<img src="{s}" height="{h}" alt="{label}"/>' for s in imgs)
    return f'<td align="center" width="{w}">{tags + "<br>" if tags else "<br><br>"}<sub>{label}</sub></td>'
SK = "https://skillicons.dev/icons?i="; SI = "https://cdn.simpleicons.org/"; DV = "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/"
groups = [
 ("Core", [cell(n, [u]) for n, u in [("C",SK+"c"),("C++",SK+"cpp"),("Python",SK+"py"),("Java",SK+"java"),
   ("STM32",SI+"stmicroelectronics/3CB4E6"),("Arduino",SK+"arduino"),("VS Code",SK+"vscode"),("Qt",SK+"qt"),
   ("PostgreSQL",SK+"postgres"),("Supabase",SK+"supabase")]]),
 ("Embedded &amp; HDL", [cell("ARM Cortex-M",[SI+"arm/0091BD"],145), cell("Embedded C",[DV+"embeddedc/embeddedc-original.svg"],135),
   cell("FreeRTOS",[local("freertos")],100), cell("ESP8266",[SI+"espressif/E7352C"],100), cell("AVR",[local("microchip")],70),
   cell("Verilog · VHDL",[DV+"verilog/verilog-original.svg"],145), cell("CAN · I²C · SPI · UART",[local("bus")],195)]),
 ("Industrial &amp; networking", [cell("GE Mark VIe",[SI+"generalelectric/3B8FE0"],120), cell("PCS7 / TIA Portal",[SI+"siemens/009999"],130),
   cell("Studio 5000",[SI+"rockwellautomation/CD163F"],120), cell("Bently Nevada<br>3500",[local("bently")],135),
   cell("HIMatrix SIS",[local("hima")],105), cell("Det-Tronics<br>F&amp;G",[local("dettronics")],135),
   cell("PROFIBUS · Modbus",[local("profibus"), local("modbus")],140,32), cell("Cisco · VLANs",[SI+"cisco/1BA0D7"],100)]),
 ("OS &amp; tools", [cell(n,[SK+i]) for n,i in [("Linux","linux"),("Ubuntu","ubuntu"),("Windows","windows"),("Bash","bash"),("Git","git"),("GitHub","github")]]),
 ("Web", [cell(n,[SK+i]) for n,i in [("JavaScript","js"),("HTML","html"),("CSS","css"),("Node.js","nodejs"),("React","react"),("Vercel","vercel"),("Netlify","netlify")]]),
]
SMALL = ("Core", "Industrial &amp; networking")
def shrink(t, x): return x.replace("<sub>", "<sub><sub>").replace("</sub>", "</sub></sub>")
sec = "### 🛠️ Tech stack\n\n" + "".join(f"**{t}**\n<table><tr>\n" + "\n".join(shrink(t, x) for x in c) + "\n</tr></table>\n\n" for t, c in groups) + "---\n\n"
s = open("README.md").read(); a = s.index("### 🛠️ Tech stack"); b = s.index("### 🚀 Featured projects")
open("README.md", "w").write(s[:a] + sec + s[b:]); print("✅ tech stack rebuilt")
