"""
Get Facebook videos/photos via bot conversation

Command : `{i}fb <input or reply link>`
Auto-downloads bare Facebook links sent in MEME_CHAT_ID.
"""

import asyncio
import re
import time
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import MessageMediaWebPage

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


def has_downloadable_media(msg):
    """Check if a message contains an actual video, photo, or document (ignoring link previews)."""
    if not msg or not msg.media or isinstance(msg.media, MessageMediaWebPage):
        return False
    return bool(msg.video or msg.photo or msg.document)


def is_text_or_link_preview(msg):
    """Allow text-only messages AND messages with URL link previews, but ignore uploaded files."""
    if not msg or not msg.text:
        return False
    return not msg.media or isinstance(msg.media, MessageMediaWebPage)


async def fetch_from_bot(client, bot_username, link, initial_timeout=25, album_timeout=3):
    """
    Sends a Facebook link to a downloader bot and collects returned media,
    reliably polling edited 'Downloading...' placeholders until media appears.
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

            first_resp = await conv.get_response(timeout=12)
            await client.send_read_acknowledge(conv.chat_id)

            # Case 1: Bot sent media directly
            if has_downloadable_media(first_resp):
                media_list.append(first_resp)

            # Case 2: Bot sent a placeholder ("Downloading...") and edits it into media
            else:
                initial_text = (first_resp.text or "").lower()
                deadline = time.monotonic() + initial_timeout
                current_msg = first_resp

                while time.monotonic() < deadline:
                    await asyncio.sleep(1.5)
                    current_msg = await client.get_messages(bot_username, ids=first_resp.id)
                    if not current_msg:
                        break

                    if has_downloadable_media(current_msg):
                        await client.send_read_acknowledge(conv.chat_id)
                        media_list.append(current_msg)
                        break

                    # If the text changed to something that is NOT a progress status, stop early
                    new_text = (current_msg.text or "").lower()
                    if new_text and new_text != initial_text:
                        if not any(
                            word in new_text
                            for word in ("download", "upload", "process", "wait", "fetch", "loading")
                        ):
                            error_text = current_msg.text
                            break

                if not media_list and not error_text:
                    error_text = (
                        current_msg.text
                        if current_msg and current_msg.text
                        else f"Timed out after {initial_timeout}s."
                    )

            # Gather any additional media messages if the post has multiple items
            if media_list:
                while True:
                    try:
                        next_resp = await conv.get_response(timeout=album_timeout)
                        await client.send_read_acknowledge(conv.chat_id)
                        if has_downloadable_media(next_resp):
                            media_list.append(next_resp)
                    except asyncio.TimeoutError:
                        break

        except asyncio.TimeoutError:
            error_text = "Bot did not respond."

    return media_list, error_text


async def process_facebook_link(event, link, is_auto=False):
    """Shared pipeline to download, send, and optionally forward Facebook media."""
    fwrd = udB.get_key("FWRD")
    status = (
        await event.reply("__Fetching Facebook media from v1...__")
        if is_auto
        else await event.eor("__Fetching Facebook media from v1...__")
    )

    # Attempt 1: @coboldbot (edits 'Downloading...' message into media)
    media_list, v1_err = await fetch_from_bot(
        event.client, "coboldbot", link, initial_timeout=25, album_timeout=3
    )

    # Attempt 2: Fallback to @go_vdbot
    v2_err = None
    if not media_list:
        await status.edit("__v1 failed, switching to v2...__")
        media_list, v2_err = await fetch_from_bot(
            event.client, "go_vdbot", link, initial_timeout=20, album_timeout=3
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
    func=lambda e: e.chat_id == MEME_CHAT_ID and is_text_or_link_preview(e),
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
