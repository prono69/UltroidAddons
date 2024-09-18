import os

from pyUltroid.fns.anilist import (
    get_airing_info,
    get_anilist_user_info,
    get_anime_info,
    get_character_info,
    get_filler_info,
    get_manga_info,
    get_watch_order,
)

from . import ultroid_cmd


@ultroid_cmd(pattern="anime ?(.*)$")
async def anime(message):
    query = message.pattern_match.group(1)
    if not query:
        return await eod(message, "Give search query")
    hell = await message.eor("Searching ...")
    caption, photo = await get_anime_info(query)

    try:
        await message.client.send_file(message.chat_id, photo, caption=caption)
        await hell.delete()
    except Exception:
        await hell.edit(caption, link_preview=False)

    if os.path.exists(photo):
        os.remove(photo)


@ultroid_cmd(pattern="manga ?(.*)$")
async def manga(message):
    query = message.pattern_match.group(1)
    if not query:
        return await eod(message, "Give search query")
    hell = await message.eor("Searching ...")
    caption, photo = await get_manga_info(query)

    try:
        await message.client.send_file(message.chat_id, photo, caption=caption)
        await hell.delete()
    except Exception:
        await hell.edit(caption, link_preview=False)

    if os.path.exists(photo):
        os.remove(photo)


@ultroid_cmd(pattern="char ?(.*)$")
async def character(message):
    query = message.pattern_match.group(1)
    if not query:
        return await eod(message, "Give search query")
    hell = await message.eor("Searching ...")
    caption, photo = await get_character_info(query)

    try:
        await message.client.send_file(message.chat_id, photo, caption=caption)
        await hell.delete()
    except Exception:
        await hell.edit(caption, link_preview=False)

    if os.path.exists(photo):
        os.remove(photo)


@ultroid_cmd(pattern="airing ?(.*)$")
async def airing(message):
    query = message.pattern_match.group(1)
    if not query:
        return await eod(message, "Give search query")
    hell = await message.eor("Searching ...")
    caption, photo = await get_airing_info(query)

    try:
        await message.client.send_file(message.chat_id, photo, caption=caption)
        await hell.delete()
    except Exception:
        await hell.edit(caption, link_preview=False)

    if os.path.exists(photo):
        os.remove(photo)


@ultroid_cmd(pattern="aniuser ?(.*)$")
async def anilist_user(message):
    query = message.pattern_match.group(1)
    if not query:
        return await eod(message, "Give search query")
    hell = await message.eor("Searching ...")
    caption, photo = await get_anilist_user_info(query)

    try:
        await message.client.send_file(message.chat_id, photo, caption=caption)
        await hell.delete()
    except Exception:
        await hell.edit(caption, link_preview=False)

    if os.path.exists(photo):
        os.remove(photo)


@ultroid_cmd(pattern="filler ?(.*)$")
async def fillers(message):
    query = message.pattern_match.group(1)
    if not query:
        return await eod(message, "Give search query")
    hell = await message.eor("Searching ...")

    caption = await get_filler_info(query)
    if caption == "":
        return await eod(message, "No results found!")

    await hell.edit(caption, link_preview=False)


@ultroid_cmd(pattern="waord ?(.*)$")
async def watch_order(message):
    query = message.pattern_match.group(1)
    if not query:
        return await eod(message, "Give search query")
    hell = await message.eor("Searching ...")

    caption = await get_watch_order(query)
    if caption == "":
        return await eod(message, "No results found!")

    await hell.edit(caption, link_preview=False)
