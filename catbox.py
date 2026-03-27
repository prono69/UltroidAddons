# Catbox Uploader Made by @NeoMatrix90
"""
❍ Commands Available -

• `{i}catb <reply to media>`
    Upload image to catbox or envs

"""

import os

import aiohttp
from catbox import CatboxUploader

from . import udB, ultroid_cmd

userhash = udB.get_key("CATBOX") if udB.get_key("CATBOX") else ""
uploader = CatboxUploader(userhash=userhash)


async def upload_to_envs(file_path):
    url = "https://envs.sh"
    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as f:
            files = {"file": f.read()}  # Read file content asynchronously
        async with session.post(url, data=files) as response:
            if response.status == 200:
                response_text = await response.text()
                url_ = response_text.split(" ")[-1]
                return url_
            else:
                return f"Error: {response.status} - {await response.text()}"


async def upload_to_qu(file_path, url="https://qu.ax/upload.php"):
    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as f:
            files = {"files[]": f.read()}  # Read file content asynchronously
            data = {"expiry": "365"}  # Add expiry parameter
        async with session.post(url, data=files, params=data) as response:
            try:
                response_json = await response.json()
                file_url = response_json.get("files", [{}])[0].get(
                    "url", "URL not found"
                )
                return file_url
            except aiohttp.ContentTypeError:
                print("Response is not in JSON format")
    return None


@ultroid_cmd(pattern="catb ?(.*)$")
async def handler(event):
    reply = await event.get_reply_message()
    flag = event.pattern_match.group(1)
    if event.is_reply and reply.media:
        kk = await event.eor("`Uploading...`")
        file_path = await reply.download_media()

        if flag == "e":
            upload_link = await upload_to_envs(file_path)
            server = "Envs"
        elif flag == "q":
            upload_link = await upload_to_qu(file_path)
            server = "Qu"
        else:
            upload_link = uploader.upload_file(file_path)
            server = "Catbox"

        if upload_link and not upload_link.startswith("Error"):
            await kk.edit(f"✘ **File Uploaded to {server}!** \n>> __{upload_link}__")
        else:
            await kk.edit(f"__Failed to upload the file: {upload_link}__")

        os.remove(file_path)  # Clean up
    else:
        await event.eor("__Please send a file along with the command.__", 5)
