# Ported Plugin
"""
✘ Commands Available -

• `{i}waifu <text>`
    paste text on random stickers.
"""

import re

from . import *

EMOJI_PATTERN = re.compile(
    "["
    "\U0001f1e0-\U0001f1ff"  # flags (iOS)
    "\U0001f300-\U0001f5ff"  # symbols & pictographs
    "\U0001f600-\U0001f64f"  # emoticons
    "\U0001f680-\U0001f6ff"  # transport & map symbols
    "\U0001f700-\U0001f77f"  # alchemical symbols
    "\U0001f780-\U0001f7ff"  # Geometric Shapes Extended
    "\U0001f800-\U0001f8ff"  # Supplemental Arrows-C
    "\U0001f900-\U0001f9ff"  # Supplemental Symbols and Pictographs
    "\U0001fa00-\U0001fa6f"  # Chess Symbols
    "\U0001fa70-\U0001faff"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027b0"  # Dingbats
    "]+",
)


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, "", inputString)


@ultroid_cmd(
    pattern="waifu ?(.*)",
)
async def waifu(animu):
    xx = await eor(animu, get_string("com_1"))
    # """Creates random anime sticker!"""
    text = animu.pattern_match.group(1)
    if not text:
        if animu.is_reply:
            text = (await animu.get_reply_message()).message
        else:
            await xx.edit(get_string("sts_1"))
            return
    waifus = [32, 33, 37, 40, 41, 42, 58, 20]
    finalcall = "#" + (str(random.choice(waifus)))
    sticcers = await animu.client.inline_query(
        "stickerizerbot",
        f"{finalcall}{(deEmojify(text))}",
    )
    await sticcers[0].click(
        animu.chat_id,
        reply_to=animu.reply_to_msg_id,
        silent=bool(animu.is_reply),
        hide_via=True,
    )
    await xx.delete()
