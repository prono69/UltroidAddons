# Ultroid plugin: NSFW Image Fetcher (improved)
# ©️ @NeoMatrix90

import asyncio
import os

import aiohttp
from pyUltroid.fns.helper import reply_id
from pyUltroid.fns.misc import unsavegif
from telethon.errors import PhotoSaveFileInvalidError
from waifu_python import Danbooru, RandomWaifu

TEMP_DIR = "./downloads/nsfw_temp/"
os.makedirs(TEMP_DIR, exist_ok=True)

# For ngif cmd
tag_aliases = {
    "bj": "blowjob",
    "pl": "pussylick",
    "fff": "threesome_fff",
    "ffm": "threesome_ffm",
    "mmf": "threesome_mmf",
}


@ultroid_cmd(pattern="nimg(?:\s|$)([\s\S]*)")
async def nsfw_images(event):
    args = event.pattern_match.group(1)
    reply_to = await reply_id(event)

    # Parse flags
    is_force_doc = "-d" in args

    # Extract remaining non-flag args
    parts = [p for p in args.split() if not p.startswith("-")]

    tag = "yuri"
    limit = 1

    # Determine if a number is passed and where
    for part in parts:
        if part.isdigit():
            limit = int(part)
        else:
            tag = part

    limit = min(limit, 10)
    await event.eor(f"🔞 Fetching `{limit}` `{tag}` image(s)...")

    try:
        images = await Danbooru.fetch_nsfw_images(tag, limit)
        if not images:
            return await event.eor("❌ No results found.", 5)

        # If only 1
        if limit == 1:
            try:
                await event.client.send_file(
                    event.chat_id,
                    images[0],
                    force_document=is_force_doc,
                    reply_to=reply_to,
                )
                return await event.delete()
            except PhotoSaveFileInvalidError:
                await event.client.send_file(
                    event.chat_id, images[0], force_document=True, reply_to=reply_to
                )
                return await event.delete()

        # Download to disk
        file_paths = []
        async with aiohttp.ClientSession() as session:
            for i, url in enumerate(images):
                try:
                    async with session.get(url) as resp:
                        if resp.status != 200:
                            continue
                        data = await resp.read()
                        ext = url.split("?")[0].split(".")[-1]
                        file_path = os.path.join(
                            TEMP_DIR, f"{event.sender_id}_{i}.{ext}"
                        )
                        with open(file_path, "wb") as f:
                            f.write(data)
                        file_paths.append(file_path)
                except:
                    continue

        if not file_paths:
            return await event.eor("❌ Failed to download any images.", 5)

        try:
            await event.client.send_file(
                event.chat_id,
                file_paths,
                reply_to=reply_to,
                force_document=is_force_doc,
            )
            await event.delete()
        except PhotoSaveFileInvalidError:
            await event.client.send_file(
                event.chat_id, file_paths, reply_to=reply_to, force_document=True
            )
            await event.delete()

        # Cleanup
        await asyncio.sleep(5)
        for f in file_paths:
            try:
                os.remove(f)
            except:
                pass

    except Exception as e:
        await event.eor(f"❌ Unexpected error: `{e}`", 5)


@ultroid_cmd(pattern="ngif(?:\s|$)([\s\S]*)")
async def nsfw_gifs(event):
    args = event.pattern_match.group(1)
    reply_to = await reply_id(event)

    is_force_doc = "-d" in args
    parts = [p for p in args.split() if not p.startswith("-")]

    tag = "yuri"
    limit = 1

    for part in parts:
        if part.isdigit():
            limit = int(part)
        else:
            tag = tag_aliases.get(part.lower(), part)

    limit = min(limit, 10)
    await event.eor(f"🔞 Fetching `{limit}` `{tag}` GIF(s)...")

    try:
        gifs = await RandomWaifu.get_random_nsfw_gif(tag, limit)
        if not gifs:
            return await event.eor("❌ No GIFs found.", 7)

        # Handle single GIF
        if limit == 1:
            try:
                msg = await event.client.send_file(
                    event.chat_id,
                    gifs[0],
                    reply_to=reply_to,
                    force_document=is_force_doc,
                )
                await unsavegif(event, msg)
                return await event.delete()
            except Exception:
                await event.client.send_file(
                    event.chat_id, gifs[0], reply_to=reply_to, force_document=True
                )
                return await event.delete()

        # For multiple GIFs
        file_paths = []
        async with aiohttp.ClientSession() as session:
            for i, url in enumerate(gifs):
                try:
                    async with session.get(url) as resp:
                        if resp.status != 200:
                            continue
                        data = await resp.read()
                        ext = url.split("?")[0].split(".")[-1]
                        file_path = os.path.join(
                            TEMP_DIR, f"{event.sender_id}_gif_{i}.{ext}"
                        )
                        with open(file_path, "wb") as f:
                            f.write(data)
                        file_paths.append(file_path)
                except Exception:
                    continue

        if not file_paths:
            return await event.eor("❌ Failed to download any GIFs.", 7)

        # If force_doc: send as media group
        if is_force_doc:
            try:
                await event.client.send_file(
                    event.chat_id, file_paths, reply_to=reply_to, force_document=True
                )
                await event.delete()
            except Exception:
                await event.eor("❌ Failed to send GIFs as documents.", 7)
        else:
            # Send one-by-one (as GIFs/animations)
            for gif_path in file_paths:
                try:
                    msg = await event.client.send_file(
                        event.chat_id, gif_path, reply_to=reply_to
                    )
                    await unsavegif(event, msg)
                except Exception:
                    # fallback to sending all as docs if any fail
                    await event.client.send_file(
                        event.chat_id,
                        file_paths,
                        reply_to=reply_to,
                        force_document=True,
                    )
                    break
            await event.delete()

        # Cleanup
        await asyncio.sleep(5)
        for f in file_paths:
            try:
                os.remove(f)
            except:
                pass

    except Exception as e:
        await event.eor(f"❌ Error: `{e}`", 9)
