import asyncio
import random
import time
import requests
from random import choice
from datetime import datetime as dt
from . import start_time, ultroid_bot, inline_mention, time_formatter

PING_DISABLE_NONPREM = {}
ANIME_WAIFU_IS_RANDOM = {}

def waifu_hentai():
    LIST_SFW_JPG = ["trap", "waifu", "blowjob", "neko"]
    waifu_link = "https"
    waifu_api = "api.waifu.pics"
    waifu_types = "nsfw"
    waifu_category = choice(LIST_SFW_JPG)
    waifu_param = f"{waifu_link}://{waifu_api}/{waifu_types}/{waifu_category}"
    response = requests.get(waifu_param).json()
    return response["url"]

def waifu_random():
    LIST_SFW_JPG = ["neko", "waifu", "megumin"]
    waifu_link = "https"
    waifu_api = "api.waifu.pics"
    waifu_types = "sfw"
    waifu_category = choice(LIST_SFW_JPG)
    waifu_param = f"{waifu_link}://{waifu_api}/{waifu_types}/{waifu_category}"
    response = requests.get(waifu_param).json()
    return response["url"]

    
@ultroid_cmd(pattern="pingset", chats=[], type=["official", "assistant"])
async def pingsetsetting(event):
    global PING_DISABLE_NONPREM, ANIME_WAIFU_IS_RANDOM
    args = event.text.lower().split()[1:]
    chat = event.chat_id
    if not event.is_private:
        if args:
            if args[0] == "anime":
                ANIME_WAIFU_IS_RANDOM[event.sender_id] = {
                    "anime": True,
                    "hentai": False,
                }
                await event.eor(f"__Turned on {args[0]} ping__", 7)
            elif args[0] == "hentai":
                ANIME_WAIFU_IS_RANDOM[event.sender_id] = {
                    "anime": False,
                    "hentai": True,
                }
                await event.eor(f"__Turned on {args[0]} ping__", 7)
            elif args[0] in ("no", "off", "false"):
                PING_DISABLE_NONPREM[event.sender_id] = False
                ANIME_WAIFU_IS_RANDOM[event.sender_id] = {
                    "anime": False,
                    "hentai": False
                }
                await event.eor("__Turned off picture ping.__", 7)
        else:
            reply_text = f"Ping Mode: {'On' if PING_DISABLE_NONPREM.get(event.sender_id) else 'Anime' if ANIME_WAIFU_IS_RANDOM.get(event.sender_id) else 'Off'}"
            await event.eor(reply_text, 7)


@ultroid_cmd(pattern="cping$", chats=[], type=["official", "assistant"])
async def custom_ping_handler(event):
    uptime = time_formatter((time.time() - start_time) * 1000)
    start = time.time()
    lol = await event.edit("__**Pong!!**__")
    duration = round((time.time() - start) * 1000)
    if PING_DISABLE_NONPREM.get(event.sender_id):
        return await lol.edit(
            f" **Pong !!** " f"`%sms` \n" f" **Uptime** - " f"`{uptime}` " % (duration)
        )
    is_anime = ANIME_WAIFU_IS_RANDOM.get(event.sender_id)
    if is_anime is None:
        if not (await ultroid_bot.get_me()).premium:
            caption = (
                f"**TEST** ◎ **PING**\n"
                f"🏓 **Pɪɴɢᴇʀ :** "
                f"`{duration}ms` \n"
                f"⌛ **Uᴘᴛɪᴍᴇ :** "
                f"`{uptime}` \n"
                f"🤴 **Oᴡɴᴇʀ :** {inline_mention(ultroid_bot.me)}"
            )
        else:
            caption = (
                f" **Pong !!** " f"`{duration}ms` \n" f" **Uptime** - " f"`{uptime}` "
            )
        return await lol.edit(caption)
    if is_anime.get("anime", False):
        photo = waifu_random()
        if not (await ultroid_bot.get_me()).premium:
            caption = (
                f"**TEST** ◎ **PING**\n"
                f"🏓 **Pɪɴɢᴇʀ :** "
                f"`{duration}ms` \n"
                f"⌛ **Uᴘᴛɪᴍᴇ :** "
                f"`{uptime}` \n"
                f"🤴 **Oᴡɴᴇʀ :** {inline_mention(ultroid_bot.me)}"
            )
        else:
            caption = (
                f" **Pong !!** " f"`{duration}ms` \n" f" **Uptime** - " f"`{uptime}` "
            )
        await event.client.send_file(event.chat_id, photo, caption=caption)
        await lol.delete()
        return 
    if is_anime.get("hentai", False):
        photo = waifu_hentai()
        if not (await ultroid_bot.get_me()).premium:
            caption = (
                f"**TEST** ◎ **PING**\n"
                f"🏓 **Pɪɴɢᴇʀ :** "
                f"`{duration}ms` \n"
                f"⌛ **Uᴘᴛɪᴍᴇ :** "
                f"`{uptime}` \n"
                f"🤴 **Oᴡɴᴇʀ :** {inline_mention(ultroid_bot.me)}"
            )
        else:
            caption = (
                f" **Pong !!** " f"`{duration}ms` \n" f" **Uptime** - " f"`{uptime}` "
            )
        await event.client.send_file(event.chat_id, photo, caption=caption)
        await lol.delete()
        return
    if not (await ultroid_bot.get_me()).premium:
        await lol.edit(
            f"**TEST** ◎ **PING**\n"
            f"🏓 **Pɪɴɢᴇʀ :** "
            f"`{duration}ms` \n"
            f"⌛ **Uᴘᴛɪᴍᴇ :** "
            f"`{uptime}` \n"
            f"🤴 **Oᴡɴᴇʀ :** {inline_mention(ultroid_bot.me)}"
        )
    else:
        await lol.edit(
            f" **Pong !!** " f"`{duration}ms` \n" f" **Uptime** - " f"`{uptime}` "
        )
