"""
✘ Commands Available -

• `{i}pint <number> <query>`
    __Get images from pinterest.__
"""

import asyncio
import io
import os
import aiohttp
import aiofiles
from PIL import Image
from . import ultroid_cmd

SEARCH_API = "https://api.nekolabs.web.id/discovery/pinterest/search?q="
DOWNLOAD_API = "https://delirius-apiofc.vercel.app/download/pinterestdl?url="


# --- Resize large images ---
def resize_image(image_bytes):
    try:
        with Image.open(image_bytes) as img:
            max_size = (1280, 1280)
            if img.size > max_size:
                img.thumbnail(max_size)
                output = io.BytesIO()
                img.save(output, format="JPEG")
                output.seek(0)
                return output
            image_bytes.seek(0)
            return image_bytes
    except Exception:
        return image_bytes


# --- Download image ---
async def download_image(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    img_bytes = io.BytesIO(await resp.read())
                    return resize_image(img_bytes)
    except:
        return None


# --- Download video ---
async def download_video(url, path="pinterest.mp4"):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(path, "wb") as f:
                        await f.write(await resp.read())
                    return path
    except:
        return None


@ultroid_cmd(pattern="pint(?: |$)(.*)")
async def pinterest_handler(event):
    """Main Pinterest command"""
    args = event.pattern_match.group(1).strip().split()

    if not args:
        return await event.eor(
            "Usage:\n"
            "`.pint <number> <query>`\n"
            "or\n"
            "`.pint <Pinterest link>`"
        )

    query = " ".join(args)
    msg = await event.eor("🔎 Searching Pinterest...")

    # --- Pinterest link (video/image) ---
    if "pinterest.com" in query or "pin.it" in query:
        await msg.edit("📥 Downloading Pinterest media...")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{DOWNLOAD_API}{query}") as resp:
                if resp.status != 200:
                    return await msg.eor("`Failed to fetch Pinterest media.`")
                data = await resp.json()

        if not data.get("status") or "data" not in data:
            return await msg.eor("`Invalid Pinterest link or unavailable.`")

        media = data["data"]["download"]
        title = data["data"].get("title", "Pinterest Media")

        # --- Video ---
        if media["type"] == "video":
            path = await download_video(media["url"])
            if not path:
                return await msg.eor("`Failed to download video.`")
            await msg.delete()
            await event.client.send_file(
                event.chat_id, path, caption=title, reply_to=event.reply_to_msg_id
            )
            os.remove(path)
            return

        # --- Image ---
        image_bytes = await download_image(media["url"])
        if not image_bytes:
            return await msg.eor("`Failed to download image.`")
        image_bytes.name = "pinterest_image.jpg"
        await msg.delete()
        await event.client.send_file(
            event.chat_id, image_bytes, caption=title, reply_to=event.reply_to_msg_id
        )
        return

    # --- Pinterest image search ---
    num_pics = 5
    if args[0].isdigit():
        num_pics = max(1, min(30, int(args[0])))
        query = " ".join(args[1:]) or None
        if not query:
            return await msg.eor("`Usage: .pint <number> <query>`")

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{SEARCH_API}{query}") as resp:
            if resp.status != 200:
                return await msg.eor("`API request failed.`")
            data = await resp.json()

    if not data.get("success") or not data.get("result"):
        return await msg.eor("`No results found.`")

    results = data["result"][:num_pics]
    urls = [r["imageUrl"] for r in results if "imageUrl" in r]
    if not urls:
        return await msg.eor("`No valid image URLs found.`")

    await msg.edit(f"📸 Downloading {len(urls)} images...")

    semaphore = asyncio.Semaphore(5)

    async def safe_download(u, idx):
        async with semaphore:
            img = await download_image(u)
            if img:
                img.name = f"{query.replace(' ', '_')}_{idx+1}.jpg"
            return img

    downloaded = await asyncio.gather(*[safe_download(u, i) for i, u in enumerate(urls)])
    images = [i for i in downloaded if i]

    if not images:
        return await msg.eor("`Failed to download any images.`")

    await msg.edit("📤 Uploading results...")

    # --- Send in albums (groups of 10) ---
    for i in range(0, len(images), 10):
        batch = images[i:i + 10]
        try:
            await event.client.send_file(
                event.chat_id,
                file=batch,
                caption=f"**Pinterest Results for:** `{query}`",
                reply_to=event.reply_to_msg_id,
                force_document=False,
                allow_cache=False,
            )
            await asyncio.sleep(1)
        except Exception as e:
            await msg.eor(f"Upload error: {e}")
            continue

    await msg.delete()