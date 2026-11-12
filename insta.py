"""
Get Instagram videos/photos via bot conversation

Command : `{i}idl <input or reply link>`
Auto-downloads bare Instagram links sent in MEME_CHAT_ID.
"""

import asyncio
import re

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest

from . import ultroid_cmd

# Stops at whitespace OR '?' so tracking params (?cplk=, ?srtk=, ?igsh=, etc.) are stripped
IG_REGEX = re.compile(r"(https?://(?:www\.)?instagram\.com/[^\s?]+)")
MEME_CHAT_ID = -1002051913343


async def delete_conv(client, chat, from_msg_id):
    """Delete all messages in the bot chat starting from /start."""
    try:
        msgs = [from_msg_id]
        async for msg in client.iter_messages(chat, min_id=from_msg_id):
            msgs.append(msg.id)
        await client.delete_messages(chat, msgs)
        await client.send_read_acknowledge(chat)
    except Exception:
        pass


async def fetch_from_bot(client, bot_username, link, initial_timeout=15, album_timeout=2):
    """
    Sends an Instagram link to a downloader bot and collects all returned media.
    Returns (media_list, error_text).
    """
    media_list = []
    error_text = None
    start_msg_id = None

    async with client.conversation(bot_username, exclusive=True) as conv:
        try:
            start_msg = await conv.send_message("/start")
        except YouBlockedUserError:
            await client(UnblockRequest(bot_username))
            start_msg = await conv.send_message("/start")

        start_msg_id = start_msg.id

        try:
            # Consume /start greeting
            await conv.get_response(timeout=8)
            await client.send_read_acknowledge(conv.chat_id)

            # Send clean Instagram link
            await conv.send_message(link)

            # Wait for first response (media or error text)
            first_resp = await conv.get_response(timeout=initial_timeout)
            await client.send_read_acknowledge(conv.chat_id)

            if first_resp.media:
                media_list.append(first_resp)

                # Gather remaining items if post is a carousel/album
                while True:
                    try:
                        next_resp = await conv.get_response(timeout=album_timeout)
                        await client.send_read_acknowledge(conv.chat_id)
                        if next_resp.media:
                            media_list.append(next_resp)
                    except asyncio.TimeoutError:
                        break
            else:
                error_text = first_resp.text or "Bot returned no media."

        except asyncio.TimeoutError:
            error_text = f"Timed out after {initial_timeout}s."
        finally:
            if start_msg_id:
                await delete_conv(client, bot_username, start_msg_id)

    return media_list, error_text


async def process_instagram_link(event, link, is_auto=False):
    """Shared pipeline to download, send, and optionally forward Instagram media."""
    fwrd = udB.get_key("FWRD")
    status = (
        await event.reply("__Fetching media from v1...__")
        if is_auto
        else await event.eor("__Fetching media from v1...__")
    )

    # Attempt 1: @TeleInstadlBot
    media_list, v1_err = await fetch_from_bot(
        event.client, "TeleInstadlBot", link, initial_timeout=15, album_timeout=2
    )

    # Attempt 2: Fallback to @go_vdbot
    v2_err = None
    if not media_list:
        await status.edit("__v1 failed, switching to v2...__")
        media_list, v2_err = await fetch_from_bot(
            event.client, "go_vdbot", link, initial_timeout=25, album_timeout=4
        )

    if media_list:
        await status.delete()
        reply_target = None if is_auto else event.reply_to_msg_id

        # Extract underlying .media objects so Telethon preserves exact video dimensions (w x h)
        if len(media_list) == 1:
            payload = media_list[0].media
        else:
            payload = [m.media for m in media_list]

        await event.client.send_file(
            event.chat_id,
            payload,
            caption=f"__{link}__",
            reply_to=reply_target,
            supports_streaming=True,
        )

        # In auto mode, remove your original bare link message so only the media remains
        if is_auto:
            try:
                await event.delete()
            except Exception:
                pass

        if fwrd and MEME_CHAT_ID != event.chat_id:
            try:
                await event.client.send_file(
                    MEME_CHAT_ID,
                    payload,
                    caption=f"__{link}__",
                    supports_streaming=True,
                )
            except Exception:
                pass
    else:
        await status.edit(
            f"**#ERROR**\n**v1:** __{v1_err}__\n**v2:** __{v2_err}__"
        )
        await asyncio.sleep(5)
        await status.delete()


@ultroid_cmd(pattern="idl ?(.*)")
async def insta_dl(event):
    """Manual command: Download Instagram media via Telegram bots."""
    raw_input = event.pattern_match.group(1)
    if not raw_input and event.is_reply:
        reply = await event.get_reply_message()
        raw_input = reply.text if reply else ""

    if not raw_input:
        return await eod(event, "**ಠ∀ಠ Give me an Instagram link or reply to one.**")

    match = IG_REGEX.search(raw_input)
    if not match:
        return await eod(event, "`Invalid or missing Instagram URL.`")

    await process_instagram_link(event, match.group(1), is_auto=False)


@ultroid_cmd(
    outgoing=True,
    func=lambda e: e.chat_id == MEME_CHAT_ID
    and bool(e.text)
    and not (e.photo or e.video or e.document),
)
async def auto_meme_insta_dl(event):
    """Auto-watcher: Download Instagram links sent directly in MEME_CHAT_ID."""
    if event.chat_id != MEME_CHAT_ID:
        return

    text = event.text.strip()

    # Ignore if it's already an explicit .idl command (handled by insta_dl above)
    if re.match(r"^[.!/?]idl\b", text, re.IGNORECASE):
        return

    match = IG_REGEX.search(text)
    if not match:
        return

    await process_instagram_link(event, match.group(1), is_auto=True)
