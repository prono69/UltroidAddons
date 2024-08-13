#
# Ultroid - UserBot
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
# .tweet made for ultroid

# .uta ported from Dark-Cobra
"""
✘ Commands Available -

• `{i}uta <search query>`
    Inline song search and downloader.

• `{i}gglax <query>`
    Create google search sticker with text.

• `{i}stic <emoji>`
    Get random stickers from emoji.

• `{i}frog <text>`
    make text stickers.

• `{i}tweet <text>`
    make twitter posts.

• `{i}quot <text>`
    write quote on animated sticker.
"""

import re
from random import choice
from . import get_string, ultroid_cmd

 
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+",
)
 

def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, "", inputString)

@ultroid_cmd(pattern="tweet ?(.*)")
async def tweet(e):
    wai = await e.eor()
    text = e.pattern_match.group(1)
    if not text:
        return await wai.edit("`Give me Some Text !`")
    try:
        results = await e.client.inline_query("twitterstatusbot", text)
        await e.reply("New Tweet", file=results[0].document)
        await wai.delete()
    except Exception as m:
        await e.eor(str(m))


@ultroid_cmd(pattern="stic ?(.*)")
async def tweet(e):
    if len(e.text) > 5 and e.text[5] != " ":
        return
    wai = await e.eor(get_string("com_1"))
    text = e.pattern_match.group(1)
    if not text:
        return await wai.edit("`Give me Some Emoji !`")
    results = await e.client.inline_query("sticker", text)
    num = choice(results)
    await e.reply("@sticker", file=num.document)
    await wai.delete()


@ultroid_cmd(pattern="gglax ?(.*)")
async def gglax_sticker(e):
    wai = await e.eor(get_string("com_1"))
    text = e.pattern_match.group(1)
    if not text:
        return await wai.edit("`Give me Some Text !`")
    try:
        results = await e.client.inline_query("googlaxbot", text)
        await e.reply("Googlax", file=results[0].document)
        await wai.delete()
    except Exception as m:
        await e.eor(str(m))


@ultroid_cmd(pattern="frog ?(.*)")
async def honkasays(e):
    wai = await e.eor(get_string("com_1"))
    text = e.pattern_match.group(1)
    if not text:
        return await wai.edit("`Give Me Some Text !`")
    text = deEmojify(text)
    if not text.endswith("."):
        text += "."
    if len(text) <= 9:
        q = 2
    elif len(text) >= 14:
        q = 0
    else:
        q = 1
    try:
        res = await e.client.inline_query("honka_says_bot", text)
        await e.reply("Honka", file=res[q].document)
        await wai.delete()
    except Exception as er:
        await wai.edit(str(er))


@ultroid_cmd(pattern="uta ?(.*)")
async def nope(doit):
    ok = doit.pattern_match.group(1)
    replied = await doit.get_reply_message()
    a = await doit.eor(get_string("com_1"))
    if ok:
        pass
    elif replied and replied.message:
        ok = replied.message
    else:
        return await doit.eor(
            "`Sir please give some query to search and download it for you..!`",
        )
    sticcers = await doit.client.inline_query("Lybot", f"{(deEmojify(ok))}")
    await doit.reply(file=sticcers[0].document)
    await a.delete()


@ultroid_cmd(pattern="quot ?(.*)")
async def quote_(event):
    IFUZI = event.pattern_match.group(1)
    if "quotly" in event.text:
        return
    if not IFUZI:
        return await event.eor("`Give some text to make Quote..`")
    EI_IR = await event.eor(get_string("com_1"))
    try:
        RE_ZK = await event.client.inline_query("@QuotAfBot", IFUZI)
        await event.reply(file=choice(RE_ZK).document)
    except Exception as U_TG:
        return await EI_IR.edit(str(U_TG))
    await EI_IR.delete()
