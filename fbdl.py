"""
**FACEBOOK DOWNLOADER**

❍ Commands Available -

• `{i}fbdl <link or reply>`
    __Downloads facebook video using API.__
"""

import os
import requests
import aiofiles
from pyUltroid.fns.tools import metadata
from telethon.tl.types import DocumentAttributeFilename, DocumentAttributeVideo
import wget

@ultroid_cmd(pattern="fbdl ?(.*)$")
async def fb_dl(event):
    query = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not query and event.is_reply:
        query = reply.text

    if not query:
        return await event.eor("__Please provide a valid Facebook video URL__", 5)

    url = "https://fbdown.online/wp-json/aio-dl/video-data/"

    headers = {
        "Connection": "keep-alive",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-platform": "Android",
        "sec-ch-ua-mobile": "?1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36",
        "content-type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Origin": "https://fbdown.online",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://fbdown.online/",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    data = {
        "url": query,
        "token": "36d935ff24a0c15593d056afa4dd8c067084ba2f2f950dc81d5de85aad6f1d33",
    }

    kk = await event.eor("__Fetching video...__")

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Check if the request was successful

        result = response.json()
        
        video_url = result.get("medias", [])[0].get("url")
        thumbnail_url = result.get("thumbnail", "")
        thumb = wget.download(thumbnail_url)
        
        if not video_url:
            return await kk.edit("__Failed to retrieve video. Please check the URL or try again later.__")

        # asynchronous
        video_response = requests.get(video_url, stream=True)
        filename = "fb_video.mp4"
        async with aiofiles.open(filename, "wb") as f:
            await f.write(video_response.content)

        # Extract metadata from the downloaded video
        meta = await metadata(filename)
        if meta is not None:
            video_duration_in_seconds = meta.get("duration", "")
            video_size = (meta.get("width", ""), meta.get("height", ""))
            
            attributes = [
                DocumentAttributeFilename(filename),
                DocumentAttributeVideo(
                    duration=video_duration_in_seconds,
                    w=video_size[0],
                    h=video_size[1],
                    supports_streaming=True,
                ),
            ]

        
        file, _ = await event.client.fast_uploader(filename, show_progress=True, event=event, to_delete=True)
        thumbnail, _ = await event.client.fast_uploader(thumb, show_progress=True, event=event, to_delete=True)
        
        await event.client.send_file(
            event.chat_id,
            file=file,
            thumb=thumbnail,
            reply_to=event.reply_to_msg_id,
            attributes=attributes,
            supports_streaming=True,
        )
        
        await kk.delete()

    except requests.exceptions.RequestException as e:
        # Handle any request-related errors
        await event.eor(f"Failed to fetch video: `{str(e)}`", 6)

    except Exception as e:
        # Handle any other errors
        await event.eor(f"An error occurred: `{str(e)}`", 6)
