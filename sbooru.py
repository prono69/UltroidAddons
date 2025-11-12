"""
✘ Commands Available -

• `{i}sbo <n for NSFW only> <tags> <no. of pics> (default to 1)`
    __Sends an image with that tag from Danbooru.__
"""

import html
import os
import random
from io import BytesIO

import aiofiles
import requests
from aiohttp import ClientSession
from telethon.errors import PhotoSaveFileInvalidError

from . import ultroid_cmd

session = ClientSession()


# --- helpers ---
def sanitize_caption(text: str, max_len: int = 1012) -> str:
    """
    Escape HTML and truncate to a safe length for Telegram captions.
    Telegram caption limit ≈ 1024 chars; keep a margin for safety and extra text.
    """
    if not text:
        return ""
    escaped = html.escape(text)
    if len(escaped) > max_len:
        return escaped[: max_len - 3] + "..."
    return escaped


async def fetch_and_save(img_url: str, filename: str) -> bool:
    """Download image (sync requests) and save to disk asynchronously."""
    response = requests.get(img_url, stream=True, timeout=15)
    if response.status_code != 200:
        return False
    async with aiofiles.open(filename, "wb") as f:
        await f.write(response.content)
    return True


# --- Post class & search_danbooru unchanged from your version ---
class Post:
    def __init__(self, source: dict, session: ClientSession):
        self._json = source
        self.session = session

    @property
    async def image(self):
        return (
            self._json.get("file_url")
            or self._json.get("large_file_url")
            or (
                self._json.get("source")
                if self._json.get("source")
                and "pximg" not in self._json.get("source", "")
                else await self.pximg
            )
        )

    @property
    async def pximg(self):
        async with self.session.get(self._json.get("source")) as response:
            return BytesIO(await response.read())

    def __getattr__(self, item):
        return self._json.get(item)


async def search_danbooru(tags: str, limit: int = 20):
    url = f"https://danbooru.donmai.us/posts.json?tags={tags}&limit={limit}"
    async with session.get(url) as response:
        if response.status != 200:
            return []
        data = await response.json(encoding="utf-8")
        return [Post(post, session) for post in data if post.get("file_url")]


@ultroid_cmd(pattern="sbo ?(.*)$")
async def sbooru(message):
    try:
        query = message.pattern_match.group(1).strip()
        if not query:
            return await message.eor(
                "`Give me something to search, e.g. waifu, maid, swimsuit...`"
            )

        # ---- Parse tags, limit, and nsfw flags ----
        parts = query.split()
        tags_list = []
        nsfw_mode = False
        limit = 1

        for token in parts:
            tok = token.strip()
            if not tok:
                continue

            # standalone nsfw flags
            if tok in {"+", "n", "-n"}:
                nsfw_mode = True
                continue

            # prefix-based (+neko)
            if tok.startswith("+") and len(tok) > 1:
                nsfw_mode = True
                tok = tok[1:]

            # numeric token = limit
            if tok.isdigit():
                limit = int(tok)
                continue

            tags_list.append(tok)

        tags = " ".join(tags_list).strip()
        if not tags:
            return await message.eor("`No tags provided. Example: /booru waifu 3`")

        # Rating tag logic
        if nsfw_mode:
            rating_tag = "rating:e"
            mode_text = "🔞 Explicit mode enabled"
        else:
            rating_tag = ""  # mixed mode, no filter
            mode_text = ""

        full_tags = f"{tags} {rating_tag}".strip()

        await message.eor(
            f"<b><i>Searching Danbooru for:</i></b> <code>{html.escape(tags)}</code>\n{mode_text}",
            parse_mode="html",
        )

        # --- Fetch posts ---
        posts = await search_danbooru(full_tags, limit=limit * 2)
        if not posts:
            return await message.eor("`No results found for your query.`")

        selected = random.sample(posts, k=min(limit, len(posts)))

        # --- Single image mode ---
        if limit == 1:
            ra = selected[0]
            img_url = await ra.image
            caption_text = sanitize_caption(
                ra._json.get("tag_string_general") or "Untitled"
            )

            try:
                await message.client.send_file(
                    message.chat_id,
                    file=img_url,
                    caption=f"<b>{caption_text}</b>",
                    parse_mode="html",
                    reply_to=message.reply_to_msg_id,
                )
            except PhotoSaveFileInvalidError:
                # Fallback to document
                await message.client.send_file(
                    message.chat_id,
                    file=img_url,
                    caption=f"<b>(Sent as document due to large size)</b>\n{caption_text}",
                    parse_mode="html",
                    reply_to=message.reply_to_msg_id,
                    force_document=True,
                )
            return await message.delete()

        # --- Multi-image (album) mode ---
        media_files = []
        idx = 0
        for i, ra in enumerate(selected, 1):
            img_url = await ra.image
            filename = f"booru_{i}.jpg"
            ok = await fetch_and_save(img_url, filename)
            if not ok:
                continue
            uploaded = await message.client.upload_file(filename)
            media_files.append(uploaded)
            idx += 1

        if not media_files:
            return await message.eor("`Failed to download any images.`")

        caption_album = f"<b><i>Here’s your {len(media_files)} {html.escape(tags)} images (•‿•)</i></b>"

        try:
            # Try sending normally
            await message.client.send_file(
                message.chat_id,
                media_files,
                caption=caption_album,
                parse_mode="html",
                reply_to=message.reply_to_msg_id,
            )
        except PhotoSaveFileInvalidError:
            # Fallback to documents
            await message.client.send_file(
                message.chat_id,
                media_files,
                caption=f"<b><i>(Sent as documents due to large size)</i></b>\n{mode_text}",
                parse_mode="html",
                reply_to=message.reply_to_msg_id,
                force_document=True,
            )

        # cleanup
        for i in range(1, idx + 1):
            try:
                os.remove(f"booru_{i}.jpg")
            except OSError:
                pass

        await message.delete()

    except Exception as e:
        await message.eor(f"Error:\n>> `{e}`")
