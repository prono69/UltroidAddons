"""
✘ Commands Available -

• `{i}sinfo`
    __Get all information about the server.__
"""

import os
import platform
import sys

import psutil
from pyUltroid.version import __version__ as UltVer
from telethon import __version__


def b2mb(b):
    return round(b / 1024 / 1024, 1)


def find_lib(lib: str) -> str:
    try:
        ver = (
            os.popen(f"python3 -m pip freeze | awk '/^{lib}==/'").read().split("==")[1]
        )
        if "\n" in ver:
            return ver.split("\n")[0]
        return ver
    except Exception:
        return "Not Installed"


def escape_html(txt: str) -> str:
    return txt.replace("<", "").replace(">", "")


text = (
    "<b><u>👾 Server Info:</u>\n\n"
    "<u>🗄 Used resources:</u>\n"
    "    CPU: {} Cores {}%\n"
    "    RAM: {} / {}MB ({}%)\n\n"
    "<u>🧾 Dist info</u>\n"
    "    Kernel: {}\n    Arch: {}\n"
    "    OS: {}\n\n"
    "<u>📦 Python libs:</u>\n"
    "    Telethon: {}\n"
    "    Aiohttp: {}\n"
    "    GitPython: {}\n"
    "    PyUltroid: {}\n"
    "    Python: {}\n"
    "    Pip: {}</b>"
)


@ultroid_cmd(pattern="sinfo$")
async def serverinfo_cmd(m):
    await m.edit("<b><i>🔄 Getting server info...</i></b>", parse_mode="html")

    inf = []
    try:
        inf.append(psutil.cpu_count(logical=True))
    except Exception:
        inf.append("n/a")

    try:
        inf.append(psutil.cpu_percent())
    except Exception:
        inf.append("n/a")

    try:
        inf.append(
            b2mb(psutil.virtual_memory().total - psutil.virtual_memory().available)
        )
    except Exception:
        inf.append("n/a")

    try:
        inf.append(b2mb(psutil.virtual_memory().total))
    except Exception:
        inf.append("n/a")

    try:
        inf.append(psutil.virtual_memory().percent)
    except Exception:
        inf.append("n/a")

    try:
        inf.append(escape_html(platform.release()))
    except Exception:
        inf.append("n/a")

    try:
        inf.append(escape_html(platform.architecture()[0]))
    except Exception:
        inf.append("n/a")

    try:
        system = os.popen("cat /etc/*release").read()
        b = system.find('DISTRIB_DESCRIPTION="') + 21
        system = system[b : system.find('"', b)]
        inf.append(escape_html(system))
    except Exception:
        inf.append("n/a")

    try:
        inf.append(__version__)
    except Exception:
        inf.append("n/a")

    try:
        inf.append(find_lib("aiohttp"))
    except Exception:
        inf.append("n/a")

    try:
        inf.append(find_lib("GitPython"))
    except Exception:
        inf.append("n/a")

    try:
        inf.append(UltVer)
    except Exception:
        inf.append("n/a")

    try:
        inf.append(
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )
    except Exception:
        inf.append("n/a")

    try:
        inf.append(os.popen("python3 -m pip --version").read().split()[1])
    except Exception:
        inf.append("n/a")

    await m.eor(text.format(*inf), parse_mode="html")
