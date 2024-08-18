# Made by @kirito6969, 
# Dont kang without credits
"""
❍ Commands Available -
 
• `{i}fur` or `{i}fur <type>`
    Sends a furry image.
    
~ NSFW: `lick`, `kiss`, `butts`, `andro`, `gyno`, `lesbian`, `straight`

"""

import html
from . import ultroid_cmd, HNDLR
import aiohttp
import random

session = aiohttp.ClientSession()

NSFW = ["lick", "kiss", "butts", "andro", "gyno", "lesbian", "straight"]
replacement_map = {
    "andro": "andromorph",
    "gyno": "gynomorph"
}

@ultroid_cmd(pattern="fur ?(.*)")
async def furry(event):
    match = event.pattern_match.group(1)
    if not match:
    	match = random.choice(NSFW)
    if match not in NSFW:
        return await eod(event, f"**Please choose a correct category**\nType: `{HNDLR}help furry`")
    # Apply the replacement after confirming it's in NSFW
    match = replacement_map.get(match, match)
    reply_to = event.reply_to_msg_id
    base = "https://v2.yiff.rest/furry"
    url = f"{base}/yiff/{match}" if match not in ("kiss", "butts", "lick") else f"{base}/{match}"
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                _data = await resp.json()
            else:
                return await eod(event, f"**Failed to fetch image: HTTP Status {resp.status}**", 5)
    except Exception as e:
        return await eod(event, f"**Error fetching image: {str(e)}**")
    
    data = _data["images"][0]
    pic = data["url"]
    _artists = data["artists"]
    sources = data["sources"]
    
    # Prepare the artist information
    artist = ", ".join(_artists) if isinstance(_artists, list) else _artists
    artist_ = html.escape(artist)
    
    # Select specific sources (e.g., 1st and 2nd sources)
    _sources = [0, 1]  # 0-based indices for 1st and 2nd sources
    final_sources = [sources[i] for i in _sources if i < len(sources)]
    
    sources_text = "\n".join([f'<a href="{html.escape(source)}">{html.escape(source)}</a>' for source in final_sources])
    caption = f"<b>✘ Artist:</b> <i>{artist_}</i>\n\n<b>✘ Sources:</b>\n<i>{sources_text}</i>"
    await event.delete()
    await event.client.send_file(
        event.chat_id, 
        file=pic, 
        caption=caption, 
        parse_mode="html", 
        reply_to=reply_to
    )
