"""
❍ Commands Available -

• `{i}ide <any number>`
    __Download a desi video.__
"""

import os
from pathlib import Path

import wget
from plugins.downloadupload import process_video


@ultroid_cmd(pattern="ide ?(.*)")
async def desixx_download(message):
    """Download videos from Desixx"""
    query = message.pattern_match.group(1)
    if not query.isdigit():
        return await message.eor(
            "⚠️ Invalid query. Please provide a number (e.g., .desixx 892)."
        )

    url = f"https://files.desixx.net/files/{query}.mp4"
    filename = f"downloads/{query}.mp4"

    processing_msg = await message.eor(f"📥 Downloading {filename}...")

    try:
        # Download file using wget
        wget.download(url, filename)

        if not Path(filename).exists():
            return await processing_msg.edit("❌ Failed to download the file.")

        await processing_msg.edit("✅ __Download complete. Uploading...__")

        # Upload the file
        file_name = f"{query}.mp4"
        caption = f"✅ **Download Complete!**\n📂 `{file_name}`"
        await process_video(filename, "downloads", caption, message)

    except Exception as e:
        await message.eor(f"❌ Error: {e}", 5)
