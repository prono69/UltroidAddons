"""
Created by @cat_me_if_you_can2 on 31/05/24.
Developed by @TrueSaiyan
❍ Commands Available -

• `{i}corn <search query>`
    Random OnlyFans Downloads

• `{i}hub <query>`
    PHub Search.

"""

import asyncio
import json
import os
import random
import shutil

import aiofiles

from . import LOGS, async_searcher, eor, ultroid_cmd, set_attributes
from os import remove, system
import logging
from pyUltroid.fns.tools import metadata
from telethon.tl.types import DocumentAttributeFilename, DocumentAttributeVideo

from RyuzakiLib import PornoHub

LOGS = logging.getLogger(__name__)

WORKING_DIR = "of_ts_vids"

statements = [
    "Woah, you're eager! I'm busy finding and compiling your steamy video.",
    "Hold your horses, I'm on the hunt for that hot video and stitching it together.",
    "Easy there, I'm tracking down and piecing together your naughty video right now.",
    "Stay calm, I'm working on locating and assembling your sexy video.",
    "Whoa, slow down! I'm gathering and combining your spicy video for you.",
    "Take a breather, I'm fetching and merging your erotic video.",
    "Hold tight, I'm in the process of searching and crafting your raunchy video.",
    "Chill out, I'm busy locating and putting together your explicit video.",
    "Simmer down, I'm scouring and assembling your sultry video content.",
    "Easy there, I'm on the job, getting your provocative video ready.",
]


async def get_video_urls():
    url = "https://api.fikfap.com/cached-high-quality/posts"
    params = {"amount": 1}
    headers = {
        "Host": "api.fikfap.com",
        "isloggedin": "false",
        "ispwa": "false",
        "authorization-anonymous": "d9e80904-171c-4d88-8372-929c6e6a3810",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Redmi Note 7 Pro Build/N6F26Q; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Accept": "*/*",
        "Origin": "https://fikfap.com",
        "X-Requested-With": "mark.via",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://fikfap.com/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = await async_searcher(
            url, headers=headers, object=True, params=params
        )
        response.headers.get("Content-Type", "")

        # Read response as text and then parse as JSON
        text = await response.text()
        data = json.loads(text)

        video_urls = []

        if isinstance(data, list):
            for post in data:
                if "videoStreamUrl" in post:
                    url = post["videoStreamUrl"]
                    url = url.replace("/playlist.m3u8", "")
                    video_urls.append(url)
        else:
            LOGS.error("Unexpected response format: %s", data)

        return video_urls
    except json.JSONDecodeError as e:
        LOGS.error("Failed to decode JSON: %s", str(e))
        LOGS.error("Response text: %s", text)
        return []
    except Exception as e:
        LOGS.error("Failed to fetch data: %s", str(e))
        return []


async def get_unique_filename(base_name, extension):
    counter = 1
    filename = os.path.join(WORKING_DIR, f"{base_name}.{extension}")
    while os.path.exists(filename):
        os.remove(filename)
        filename = os.path.join(WORKING_DIR, f"{base_name}_{counter}.{extension}")
        counter += 1
    return filename


async def download_videos():
    if not os.path.exists(WORKING_DIR):
        os.makedirs(WORKING_DIR)

    video_urls = await get_video_urls()

    headers = {
        "Host": "vz-5d293dac-178.b-cdn.net",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Redmi Note 7 Pro Build/N6F26Q; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
        "Accept": "*/*",
        "Origin": "https://fikfap.com",
        "X-Requested-With": "mark.via",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://fikfap.com/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
    }

    ts_files = []
    for idx, base_url in enumerate(video_urls):
        for i in range(5):
            url = f"{base_url}/480x842/video{i}.ts"
            ts_file = await get_unique_filename(f"video_{idx}_{i}", "ts")
            try:
                content = await async_searcher(url, headers=headers, re_content=True)
                async with aiofiles.open(ts_file, "wb") as file:
                    await file.write(content)
                ts_files.append(ts_file)
            except Exception:
                break

    combined_file = await get_unique_filename("combined_video", "ts")
    async with aiofiles.open(combined_file, "wb") as combined:
        for ts_file in ts_files:
            async with aiofiles.open(ts_file, "rb") as file:
                await combined.write(await file.read())

    output_file = await get_unique_filename("final_video", "mp4")
    process = await asyncio.create_subprocess_exec(
        "ffmpeg",
        "-i",
        combined_file,
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        output_file,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await process.communicate()

    return output_file, ts_files


@ultroid_cmd(pattern="corn")
async def corn(event):
    if (await ultroid_bot.get_me()).premium:
        limitedfile = False
    else:
        limitedfile = True

    try:
        random_statement = random.choice(statements)
        xx = await eor(event, f"{random_statement} 😈")
        output_file, ts_files = await download_videos()
        await xx.eor(
            "Video downloaded, now uploading... 😈"
        )

        file_size = os.path.getsize(output_file) / (1024 * 1024)

        if limitedfile and file_size > 2000:
            await eor(event, "The file is too big to upload (exceeds 2000 MB).")
            os.remove(output_file)
            for ts_file in ts_files:
                os.remove(ts_file)
            shutil.rmtree(WORKING_DIR)
            return

        process = await asyncio.create_subprocess_exec(
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-show_entries",
            "stream=width,height",
            "-of",
            "default=noprint_wrappers=1",
            output_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        output, _ = await process.communicate()
        output = output.decode("utf-8").split("\n")

        attribs = await set_attributes(output_file)

        await event.client.send_file(
            event.chat_id,
            output_file,
            caption="Here is your video! 😈",
            supports_streaming=True,
            attributes=attribs,
        )
        await asyncio.sleep(1)
        await xx.delete()
        os.remove(output_file)
        for ts_file in ts_files:
            os.remove(ts_file)
        shutil.rmtree(WORKING_DIR)
    except Exception as e:
        await eor(event, f"An error occurred: {str(e)}")
        shutil.rmtree(WORKING_DIR)


@ultroid_cmd(pattern="hub( (.*)|$)")
async def phub_search(e):
    query = e.pattern_match.group(2)
    reply = await e.get_reply_message()

    if not query:
        if reply and reply.text:
            query = reply.message.strip()
        else:
            return await e.eor("Please provide a query to search on PornHub.")

    moi = await e.eor("Searching for the video...")

    api = PornoHub()

    try:
        # Download video based on the query
        file_path, thumb = await api.x_download(query=query)
        output_message = f"Downloaded File: {file_path}\nThumbnail: {thumb}"
    except Exception as exc:
        LOGS.warning(exc, exc_info=True)
        return await moi.edit(f"Error: \n> {exc}")

    meta = await metadata(file_path)
    await moi.edit("Download completed. Uploading video...")
    if meta is not None:
        video_duration_in_seconds = meta.get("duration", "")
        thumbnail_size = (meta.get("width", ""), meta.get("height", ""))
        thumbnail_start_offset = 5

        attributes = [
            DocumentAttributeFilename(file_path),
            DocumentAttributeVideo(
            duration=video_duration_in_seconds,
            w=thumbnail_size[0],
            h=thumbnail_size[1],
            supports_streaming=True,
            ),
       ]
  
    file, _ = await e.client.fast_uploader(file_path, show_progress=True, event=moi, to_delete=True)
    thumbnail, _ = await e.client.fast_uploader(thumb, show_progress=True, event=moi, to_delete=True)
  
    try:
        await e.client.send_file(
            e.chat_id,
            file,
            thumb=thumbnail,
            caption=f"**Query:** `{query}`\n**Output:**\n{output_message}",
            reply_to=e.reply_to_msg_id,
      attributes=attributes,
            supports_streaming=True,
        )
    except Exception as send_exc:
        LOGS.error(send_exc, exc_info=True)
        await moi.edit(f"Error sending the file: \n> {send_exc}")
    finally:
        await moi.delete()
        if thumb:
            remove(thumb)
    try:
        await moi.delete()
    except Exception as er:
        LOGS.info("Error: {er}")