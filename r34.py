# Rule34 Plugin for UltX by @Neo_Matrix90

from . import ultroid_cmd, udB
from pyUltroid.fns.tools import async_searcher
import re
import random
import asyncio
import aiohttp
from telethon.errors import PhotoSaveFileInvalidError

API_KEY = udB.get_key("RULE34_API_KEY")
USER_ID = udB.get_key("RULE34_USER_ID")

proxylist = []

IMAGE_EXTS = {"jpg", "jpeg", "png", "gif", "webp"}
VIDEO_EXTS = {"mp4", "webm", "avi", "mov", "mkv"}


async def get_proxy():
    global proxylist

    if proxylist:
        return proxylist

    temp_proxy = []

    try:
        url = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=ipport&format=text&timeout=3000"
        data = await async_searcher(url)
        temp_proxy += [x.strip() for x in data.split("\n") if x.strip()]
    except:
        pass

    try:
        url = "http://rootjazz.com/proxies/proxies.txt"
        data = await async_searcher(url)
        temp_proxy += [x.strip() for x in data.split("\n") if x.strip()]
    except:
        pass

    proxylist.extend(temp_proxy[:200])
    return proxylist


def get_ext(url):
    return url.split("?")[0].rsplit(".", 1)[-1].lower()


def filter_urls(urls, mode):
    """Filter URLs by media type based on mode: 'p' = photo, 'v' = video, 'm' = mixed"""
    if mode == "m":
        return urls
    elif mode == "v":
        return [u for u in urls if get_ext(u) in VIDEO_EXTS]
    else:  # default = photos only
        return [u for u in urls if get_ext(u) in IMAGE_EXTS]


async def fetch_rule34(tags, count=1, mode="p"):
    tags_encoded = tags.replace(" ", "%20")

    url = (
        "http://api.rule34.xxx/index.php?page=dapi&s=post&q=index"
        f"&tags={tags_encoded}&api_key={API_KEY}&user_id={USER_ID}&limit=100"
    )

    headers = {"User-Agent": "Mozilla/5.0"}
    file_urls = []

    # 1️⃣ Try direct request first
    try:
        data = await async_searcher(url, headers=headers)
        file_urls = re.findall(r'file_url="([^"]+)"', data)
    except:
        pass

    # 2️⃣ Proxy fallback if direct failed
    if not file_urls:
        proxies = await get_proxy()
        for proxy_host in proxies:
            try:
                proxy_url = f"http://{proxy_host}"
                data = await async_searcher(url, headers=headers, proxy=proxy_url)
                file_urls = re.findall(r'file_url="([^"]+)"', data)
                if file_urls:
                    break
            except:
                if proxy_host in proxylist:
                    proxylist.remove(proxy_host)

    if not file_urls:
        return []

    # Filter by media type
    file_urls = filter_urls(file_urls, mode)

    if not file_urls:
        return []

    count = min(count, len(file_urls))
    return random.sample(file_urls, count)


async def download_to_bytes(session, url):
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=60)) as resp:
        return await resp.read()


@ultroid_cmd(pattern=r"r34 (?:(\d+) )?(.+?)( v| m)?$")
async def rule34(event):
    match = event.pattern_match
    count_str = match.group(1)
    tags = match.group(2).strip()
    flag = match.group(3).strip() if match.group(3) else "p"

    # flag: "v" = video only, "m" = mixed, anything else = photos only
    mode = flag if flag in ("v", "m") else "p"
    mode_label = {"p": "🖼 photos", "v": "🎥 videos", "m": "🎲 mixed"}[mode]

    if not tags:
        return await event.eor("Give some tags...")

    count = int(count_str.strip()) if count_str else 1
    count = min(count, 10)

    msg = await event.eor(f"__Searching for {count} {tags} {mode_label}...__ 😒")

    urls = await fetch_rule34(tags, count, mode)

    if not urls:
        return await msg.edit(f"No {mode_label} found for `{tags}`...")

    # Single file — upload from memory, no disk
    if len(urls) == 1:
        try:
            async with aiohttp.ClientSession() as session:
                data = await download_to_bytes(session, urls[0])
            ext = get_ext(urls[0])
            uploaded = await event.client.upload_file(data, file_name=f"r34.{ext}")
            try:
                await event.client.send_file(
                event.chat_id,
                file=uploaded,
                caption=f"**Tags:** `{tags}`")
            except PhotoSaveFileInvalidError:
                await event.client.send_file(
                event.chat_id,
                file=uploaded,
                force_document=True,
                caption=f"**Tags:** `{tags}`")
                
            return await msg.delete()
        except Exception as e:
            return await msg.edit(f"Failed to send.\n\n**Tags:** `{tags}`\n`{e}`")

    # Multiple files — download all to memory concurrently, then send as album
    await msg.edit(f"__Sending {len(urls)} {tags} {mode_label}...__ ⏳")

    try:
        async with aiohttp.ClientSession() as session:
            all_bytes = await asyncio.gather(
                *[download_to_bytes(session, url) for url in urls]
            )

        uploaded = []
        for i, (data, url) in enumerate(zip(all_bytes, urls)):
            ext = get_ext(url)
            uploaded.append(await event.client.upload_file(data, file_name=f"r34_{i}.{ext}"))

        await event.client.send_file(
            event.chat_id,
            file=uploaded,
            caption=f"**Tags:** `{tags}`"
        )
        await msg.delete()

    except Exception as e:
        await msg.edit(f"Failed to send.\n\n**Tags:** `{tags}`\n`{e}`")
        