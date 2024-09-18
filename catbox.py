# Catbox Uploader Made by @NeoMatrix90
"""
❍ Commands Available -

• `{i}catb <reply to media>`
    Upload image to catbox or envs

"""

import os

import requests
from pyUltroid.fns.misc import CatboxUploader

from . import udB, ultroid_cmd

userhash = udB.get_key("CATBOX") if udB.get_key("CATBOX") else ""
uploader = CatboxUploader(userhash)


def upload_to_envs(file_path):
    url = "https://envs.sh"
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            response_text = response.text
            url_ = response_text.split(" ")[-1]
            return url_
        else:
            return f"Error: {response.status_code} - {response.text}"


@ultroid_cmd(pattern="catb ?(.*)$")
async def handler(event):
    reply = await event.get_reply_message()
    flag = event.pattern_match.group(1)
    if event.is_reply and reply.media:
        kk = await event.eor("`Uploading...`")
        file_path = await reply.download_media()

        if flag == "e":
            upload_link = upload_to_envs(file_path)
            server = "Envs"
        else:
            upload_link = uploader.upload_file(file_path)
            server = "Catbox"

        if upload_link and not upload_link.startswith("Error"):
            await kk.edit(f"✘ **File Uploaded to {server}!** \n>> __{upload_link}__")
        else:
            await kk.edit(f"__Failed to upload the file: {upload_link}__")

        os.remove(file_path)  # Clean up
    else:
        await eod(event, "__Please send a file along with the command.__")
