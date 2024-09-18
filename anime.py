# Ported from Hellbot for Ultroid by @NeoMatrix90

"""
✘ Commands Available -

• `{i}anime <anime name>`
   __Get an info about the mentioned anime.__
   
• `{i}manga <manga name>`
   __Get an info about the mentioned manga.__
   
• `{i}char <character name>`
   __Get an info about the mentioned character.__
   
• `{i}airing <anime name>`
   __Get an airing info about the mentioned anime.__
   
• `{i}aniuser <anilist username>`
   __Get an info about the mentioned anilist user.__
   
• `{i}filler <anime name>`
   __Get the list of filler/canon episodes about the mentioned anime.__
   
• `{i}waord <anime name>`
   __Get the watch order about the mentioned anime.__
   
"""

import os
from . import ultroid_cmd
from telethon.errors import ChatSendMediaForbiddenError
from pyUltroid.fns.anilist import (
    get_airing_info,
    get_anilist_user_info,
    get_anime_info,
    get_character_info,
    get_filler_info,
    get_manga_info,
    get_watch_order,
)

@ultroid_cmd(pattern="anime ?(.*)$")
async def anime(message):
    query = message.pattern_match.group(1)
    if not query:
    	return await eod(message, "`B~Baka, I can't search the void`")
    hell = await message.eor("__Searching ...__")
    caption, photo = await get_anime_info(query)

    try:
        await message.client.send_file(message.chat_id, photo, caption=caption)
        await hell.delete()
    except ChatSendMediaForbiddenError:
        await hell.edit(caption, link_preview=False)

    if os.path.exists(photo):
        os.remove(photo)


@ultroid_cmd(pattern="manga ?(.*)$")
async def manga(message):
    query = message.pattern_match.group(1)
    if not query:
    	return await eod(message, "`B~Baka, I can't search the void`")
    hell = await message.eor("__Searching ...__")
    caption, photo = await get_manga_info(query)

    try:
        await message.client.send_file(message.chat_id, photo, caption=caption)
        await hell.delete()
    except ChatSendMediaForbiddenError:
        await hell.edit(caption, link_preview=False)

    if os.path.exists(photo):
        os.remove(photo)


@ultroid_cmd(pattern="char ?(.*)$")
async def character(message):
    query = message.pattern_match.group(1)
    if not query:
    	return await eod(message, "`B~Baka, I can't search the void`")
    hell = await message.eor("__Searching ...__")
    caption, photo = await get_character_info(query)

    try:
        await message.client.send_file(message.chat_id, photo, caption=caption)
        await hell.delete()
    except ChatSendMediaForbiddenError:
        await hell.edit(caption, link_preview=False)

    if os.path.exists(photo):
        os.remove(photo)


@ultroid_cmd(pattern="airing ?(.*)$")
async def airing(message):
    query = message.pattern_match.group(1)
    if not query:
    	return await eod(message, "`B~Baka, I can't search the void`")
    hell = await message.eor("__Searching ...__")
    caption, photo = await get_airing_info(query)

    try:
        await message.client.send_file(message.chat_id, photo, caption=caption)
        await hell.delete()
    except ChatSendMediaForbiddenError:
        await hell.edit(caption, link_preview=False)

    if os.path.exists(photo):
        os.remove(photo)


@ultroid_cmd(pattern="aniuser ?(.*)$")
async def anilist_user(message):
    query = message.pattern_match.group(1)
    if not query:
    	return await eod(message, "`B~Baka, I can't search the void`")
    hell = await message.eor("__Searching ...__")
    caption, photo = await get_anilist_user_info(query)

    try:
        await message.client.send_file(message.chat_id, photo, caption=caption)
        await hell.delete()
    except ChatSendMediaForbiddenError:
        await hell.edit(caption, link_preview=False)

    if os.path.exists(photo):
        os.remove(photo)


@ultroid_cmd(pattern="filler ?(.*)$")
async def fillers(message):
    query = message.pattern_match.group(1)
    if not query:
    	return await eod(message, "`B~Baka, I can't search the void`")
    hell = await message.eor("__Searching ...__")

    caption = await get_filler_info(query)
    if caption == "":
        return await eod(message, "__No results found!__")

    await hell.edit(caption, link_preview=False)


@ultroid_cmd(pattern="waord ?(.*)$")
async def watch_order(message):
    query = message.pattern_match.group(1)
    if not query:
    	return await eod(message, "`B~Baka, I can't search the void`")
    hell = await message.eor("__Searching ...__")

    caption = await get_watch_order(query)
    if caption == "":
        return await eod(message, "__No results found!__")

    await hell.edit(caption, link_preview=False)
