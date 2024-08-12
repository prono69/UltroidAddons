"""
Get instagram videos by bot conv

Command : `{i}insta <input or reply link>`
"""

import asyncio

from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import ultroid_cmd


async def delete_conv(event, chat, from_message):
    itermsg = event.client.iter_messages(chat, min_id=from_message.id)
    msgs = [from_message.id]
    async for i in itermsg:
        msgs.append(i.id)
    await event.client.delete_messages(chat, msgs)
    await event.client.send_read_acknowledge(chat)


@ultroid_cmd(pattern="idl ?(.*)")
async def insta_dl(event):
    "For downloading instagram media"
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not link and reply:
        link = reply.text
    if not link:
        return await eod(event, "**ಠ∀ಠ Give me link to search..**")
    if "instagram.com" not in link:
        return await eod(
            event, "` I need a Instagram link to download it's Video...`(*_*)"
        )
    v1 = "Fullsavebot"
    v2 = "UVDownloaderBot"
    media_list = []
    eyepatch = await event.eor("**Downloading.....**")
    async with event.client.conversation(v1) as conv:
        try:
            v1_flag = await conv.send_message("/start")
        except YouBlockedUserError:
            # await catub(unblock("Fullsavebot"))
            v1_flag = await conv.send_message("/start")
        checker = await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        if "Choose the language you like" in checker.message:
            await checker.click(1)
            await conv.send_message(link)
            await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        await conv.send_message(link)
        await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        try:
            media = await conv.get_response(timeout=10)
            await event.client.send_read_acknowledge(conv.chat_id)
            if media.media:
                while True:
                    media_list.append(media)
                    try:
                        media = await conv.get_response(timeout=2)
                        await event.client.send_read_acknowledge(conv.chat_id)
                    except asyncio.TimeoutError:
                        break
                details = media_list[0].message.splitlines()
                await eyepatch.delete()
                await event.client.send_file(
                    event.chat_id,
                    media_list,
                    caption=f"**{details[0]}**",
                )
                return await delete_conv(event, v1, v1_flag)
        except asyncio.TimeoutError:
            await delete_conv(event, v1, v1_flag)
        await event.eor("**Switching v2...**")
        async with event.client.conversation(v2) as conv:
            try:
                v2_flag = await conv.send_message("/start")
            except YouBlockedUserError:
                # await catub(unblock("UVDownloaderBot"))
                v2_flag = await conv.send_message("/start")
            await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            await asyncio.sleep(1)
            await conv.send_message(link)
            # await conv.get_response()
            # await event.client.send_read_acknowledge(conv.chat_id)
            media = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            if media.media:
                await eyepatch.delete()
                await event.client.send_file(event.chat_id, media)
            else:
                await eod(
                    event,
                    f"**#ERROR\nv1 :** __Not valid URL__\n\n**v2 :**__ {media.text}__",
                )
            await delete_conv(event, v2, v2_flag)
