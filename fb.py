"""
Get Facebook videos/photos via bot conversation

Command : `{i}fb <input or reply link>`
Auto-downloads bare Facebook links sent in MEME_CHAT_ID.
"""

import asyncio
import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest

from . import ultroid_cmd

FB_REGEX = re.compile(
    r"(https?://(?:(?:www|m|web)\.)?(?:facebook\.com|fb\.watch|fb\.com)/[^\s]+)"
)
MEME_CHAT_ID = -1002051913343


def clean_fb_url(raw_url):
    """Strip tracking params (?mibextid=, ?rdid=, etc.) while keeping ?v= video IDs."""
    parsed = urlparse(raw_url)
    query = parse_qs(parsed.query)
    clean_query = {"v": query["v"]} if "v" in query else {}
    return urlunparse(parsed._replace(query=urlencode(clean_query, doseq=True)))


async def fetch_from_bot(client, bot_username, link, initial_timeout=18, album_timeout=3):
    """
    Sends a Facebook link directly to a downloader bot and collects all returned media.
    Returns (media_list, error_text).
    """
    media_list = []
    error_text = None

    async with client.conversation(bot_username, exclusive=True) as conv:
        try:
            try:
                await conv.send_message(link)
            except YouBlockedUserError:
                await client(UnblockRequest(bot_username))
                await conv.send_message(link)

            first_resp = await conv.get_response(timeout=initial_timeout)
            await client.send_read_acknowledge(conv.chat_id)

            if first_resp.media and (
                first_resp.video or first_resp.photo or first_resp.document
            ):
                media_list.append(first_resp)

                # Gather remaining items if post has multiple attachments
                while True:
                    try:
                        next_resp = await conv.get_response(timeout=album_timeout)
                        await client.send_read_acknowledge(conv.chat_id)
                        if next_resp.media and (
                            next_resp.video or next_resp.photo or next_resp.document
                        ):
                            media_list.append(next_resp)
                    except asyncio.TimeoutError:
                        break
            else:
                error_text = first_resp.text or "Bot returned no media."

        except asyncio.TimeoutError:
            error_text = f"Timed out after {initial_timeout}s."

    return media_list, error_text


async def process_facebook_link(event, link, is_auto=False):
    """Shared pipeline to download, send, and optionally forward Facebook media."""
    fwrd = udB.get_key("FWRD")
    status = (
        await event.reply("__Fetching Facebook media from v1...__")
        if is_auto
        else await event.eor("__Fetching Facebook media from v1...__")
    )

    # Attempt 1: @coboldbot
    media_list, v1_err = await fetch_from_bot(
        event.client, "coboldbot", link, initial_timeout=20, album_timeout=3
    )

    # Attempt 2: Fallback to @go_vdbot
    v2_err = None
    if not media_list:
        await status.edit("__v1 failed, switching to v2...__")
        media_list, v2_err = await fetch_from_bot(
            event.client, "go_vdbot", link, initial_timeout=18, album_timeout=3
        )

    if media_list:
        await status.delete()
        reply_target = None if is_auto else event.reply_to_msg_id

        payload = (
            media_list[0].media
            if len(media_list) == 1
            else [m.media for m in media_list]
        )

        await event.client.send_file(
            event.chat_id,
            payload,
            caption=f"__{link}__",
            reply_to=reply_target,
            supports_streaming=True,
        )

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


@ultroid_cmd(pattern="fb ?(.*)")
async def fb_dl(event):
    """Manual command: Download Facebook media via Telegram bots."""
    raw_input = event.pattern_match.group(1)
    if not raw_input and event.is_reply:
        reply = await event.get_reply_message()
        raw_input = reply.text if reply else ""

    if not raw_input:
        return await eod(event, "**ಠ∀ಠ Give me a Facebook link or reply to one.**")

    match = FB_REGEX.search(raw_input)
    if not match:
        return await eod(event, "`Invalid or missing Facebook URL.`")

    clean_link = clean_fb_url(match.group(1))
    await process_facebook_link(event, clean_link, is_auto=False)


@ultroid_cmd(
    outgoing=True,
    func=lambda e: e.chat_id == MEME_CHAT_ID
    and bool(e.text)
    and not (e.photo or e.video or e.document),
)
async def auto_meme_fb_dl(event):
    """Auto-watcher: Download Facebook links sent directly in MEME_CHAT_ID."""
    if event.chat_id != MEME_CHAT_ID:
        return

    text = event.text.strip()

    if re.match(r"^[.!/?]fb\b", text, re.IGNORECASE):
        return

    match = FB_REGEX.search(text)
    if not match:
        return

    clean_link = clean_fb_url(match.group(1))
    await process_facebook_link(event, clean_link, is_auto=True)
