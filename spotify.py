"""
✧ Ultroid Spotify Downloader ✧

Usage:
    .sp <song name>
    .sp <Spotify link>
    or reply to a text message with .sp
"""

import os
import time
import aiohttp
import aiofiles
from . import ultroid_cmd


SEARCH_API = "https://delirius-apiofc.vercel.app/search/spotify?q="
DOWNLOAD_API = "https://delirius-apiofc.vercel.app/download/spotifydl?url="


# --- Optional: progress indicator ---
async def progress(current, total, event, start, text):
    now = time.time()
    diff = now - start
    if diff % 3 == 0:
        await event.edit(f"{text}\n\nUploaded {current * 100 / total:.1f}%...")


@ultroid_cmd(pattern="sp(?: |$)(.*)")
async def spotify_download(event):
    """Main command: .sp <song name> or <Spotify link>"""
    query = event.pattern_match.group(1).strip()

    # --- Handle reply text ---
    if not query and event.reply_to_msg_id:
        reply = await event.get_reply_message()
        if reply and reply.text:
            query = reply.text.strip()

    if not query:
        return await event.eor("**Usage:** `.sp <song name or Spotify link>`")

    status = await event.eor("🎵 Processing your request...")

    song_title = None
    artist = None
    song_url = None
    dl_info = None

    # --- CASE 1: Direct Spotify link ---
    if "open.spotify.com" in query or "spotify.link" in query:
        await status.edit("🔗 Direct Spotify link detected. Fetching download link...")
        song_url = query.strip()

        # Directly call the download API
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{DOWNLOAD_API}{song_url}") as resp:
                    if resp.status != 200:
                        raise Exception("Failed to connect to download API.")
                    data = await resp.json()
        except Exception as e:
            return await status.edit(f"**Error:** API connection failed.\n`{e}`")

        if not data.get("status"):
            return await status.edit("⚠️ This track is unavailable or cannot be downloaded.")

        dl_info = data["data"]
        song_title = dl_info.get("title", "Unknown Title")
        artist = dl_info.get("author", "Unknown Artist")

    # --- CASE 2: Text query search ---
    else:
        await status.edit(f"🔎 Searching Spotify for `{query}`...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{SEARCH_API}{query}&limit=1") as resp:
                    if resp.status != 200:
                        raise Exception("Search API failed")
                    data = await resp.json()
        except Exception as e:
            return await status.edit(f"**Error:** Spotify search failed. {e}")

        if not data.get("status") or not data.get("data"):
            return await status.edit("**No results found.**")

        song = data["data"][0]
        song_title = song.get("title", "Unknown Title")
        artist = song.get("artist", "Unknown Artist")
        song_url = song.get("url")

        await status.edit(f"✅ Found: **{song_title}** by **{artist}**\nFetching download link...")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{DOWNLOAD_API}{song_url}") as resp:
                    if resp.status != 200:
                        raise Exception("Failed to fetch download link.")
                    data = await resp.json()
        except Exception as e:
            return await status.edit(f"**Error:** Failed to get download link. {e}")

        if not data.get("status"):
            return await status.edit("⚠️ This track isn't available for download.")
        dl_info = data["data"]

    # --- Common download logic ---
    download_url = dl_info.get("url")
    image_url = dl_info.get("image")
    author = dl_info.get("author", artist)
    spotify_link = song_url

    if (
        not download_url
        or not download_url.startswith("http")
        or "undefined" in download_url
    ):
        return await status.edit("⚠️ Invalid or unavailable download link. Try another song.")

    song_file = f"{song_title}.mp3"
    thumb_file = f"{song_title}.jpg"

    await status.edit(f"⬇️ Downloading **{song_title}**...")

    try:
        async with aiohttp.ClientSession() as session:
            # Download cover art
            if image_url:
                async with session.get(image_url) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(thumb_file, "wb") as f:
                            await f.write(await resp.read())

            # Download song audio
            async with session.get(download_url) as resp:
                if resp.status != 200 or "audio" not in resp.headers.get("Content-Type", ""):
                    raise Exception("Invalid audio data.")
                async with aiofiles.open(song_file, "wb") as f:
                    await f.write(await resp.read())
    except Exception as e:
        return await status.edit(f"**Error:** Failed to download. {e}")

    await status.edit(f"📤 Uploading **{song_title}**...")

    try:
        c_time = time.time()
        await event.client.send_file(
            event.chat_id,
            song_file,
            caption=(
                f"🎧 **Song Name:** {song_title}\n"
                f"👤 **Artist:** {author}\n"
                f"[Open in Spotify]({spotify_link})"
            ),
            thumb=thumb_file if os.path.exists(thumb_file) else None,
            progress_callback=lambda c, t: progress(c, t, status, c_time, f"📤 Uploading **{song_title}**..."),
            parse_mode="md",
        )
    except Exception as e:
        await status.edit(f"**Error:** Upload failed. {e}")
    finally:
        for f in (song_file, thumb_file):
            if os.path.exists(f):
                os.remove(f)

    await status.delete()