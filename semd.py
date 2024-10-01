# < Source - t.me/testingpluginnn >
# < https://github.com/TeamUltroid/Ultroid >

"""
✘ **Send any Installed Plugin to the Chat!**

>> Use : `{i}semd <plugin_name>`
"""

from pathlib import Path
from re import findall

from pyUltroid.dB._core import LIST
from . import LOGS, ULTConfig, get_paste, ultroid_cmd


def send(fn):
    tmp_list = ("plugins", "addons")
    if not fn.endswith(".py"):
        fn += ".py"
    for i in tmp_list:
        path = Path(i).joinpath(fn)
        if path.is_file():
            return str(path)


def alt_send(plugin):
    for k, v in LIST.items():
        for cmds in v:
            if findall(plugin, cmds):
                return send(k)


async def pastee(filepath):
    with open(filepath) as f:
        data = f.read()
    ok, out = await get_paste(data)
    if not ok:
        return LOGS.warning(f"Error in pasting file: {filepath}", exc_info=True)
    return f"<b>>> <a href='https://spaceb.in/{out}'>Pasted Here!</a></b> \n"


@ultroid_cmd(
    pattern="semd(?: (.*)|$)",
    fullsudo=True,
)
async def semd_plugin(ult):
    args = ult.pattern_match.group(1)
    if not args:
        return await ult.eor("`Give a plugin name to send..`", time=5)

    eris = await ult.eor(f"__Sending {args} plugin...__")
    if not (path := send(args)):
        path = alt_send(args)
    if not path:
        return await eris.edit(f"No plugins were found for: `{args}`")

    paste_link = await pastee(path) or ""
    repo = "https://github.com/TeamUltroid/Ultroid"
    caption = f"<b>>> </b><code>{path}</code>\n{paste_link}\n© <a href={repo}>Team Ultroid</a>"
    try:
        await ult.client.send_file(
            ult.chat_id,
            path,
            caption=caption,
            parse_mode="html",
            thumb=ULTConfig.thumb,
            reply_to=ult.reply_to_msg_id or ult.id,
        )
        await eris.delete()
    except Exception as exc:
        LOGS.exception(exc)
        await eris.edit(f"**Error:**  `{exc}`")
