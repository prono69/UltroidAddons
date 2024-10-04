"""
✘ Commands Available -

• `{i}booru <no. of pics> (default to 1)`
    __Sends a random image from Danbooru.__
"""

import os
from io import BytesIO

import aiofiles
import requests
from aiohttp import ClientSession

from . import ultroid_cmd

session = ClientSession()


class Post:
    def __init__(self, source: dict, session: ClientSession):
        self._json = source
        self.session = session

    @property
    async def image(self):
        return (
            self.file_url
            if self.file_url
            else (
                self.large_file_url
                if self.large_file_url
                else (
                    self.source
                    if self.source and "pximg" not in self.source
                    else await self.pximg if self.source else None
                )
            )
        )

    @property
    async def pximg(self):
        async with self.session.get(self.source) as response:
            return BytesIO(await response.read())

    def __getattr__(self, item):
        return self._json.get(item)


async def random():
    async with session.get(
        url="https://danbooru.donmai.us/posts/random.json"
    ) as response:
        return Post(await response.json(encoding="utf-8"), session)


@ultroid_cmd(pattern="booru ?(.*)$")
async def booru(message):
    try:
        query = message.pattern_match.group(1).strip()
        num_images = 1
        save_to_disk = False

        if query.isdigit():
            num_images = int(query)
            save_to_disk = True

        await message.eor(
            f"<b><i>Searching {num_images} art(s)...</i></b>", parse_mode="html"
        )

        media_group = []
        for i in range(num_images):
            ra = await random()
            img_url = await ra.image

            if save_to_disk:
                response = requests.get(img_url, stream=True)
                if response.status_code == 200:
                    filename = f"booru_image_{i}.jpg"
                    async with aiofiles.open(filename, "wb") as f:
                        await f.write(response.content)

                    # Upload the file
                    uploaded_img = await message.client.upload_file(filename)
                    media_group.append(
                        {
                            "file": uploaded_img,
                            # "caption": f'<b>{ra.tag_string_general if ra.tag_string_general else "Untitled"}</b>',
                            # "parse_mode": "html",
                        }
                    )
                else:
                    await message.eor("Failed to fetch image.", parse_mode="html")
                    return

            else:
                # Directly send the file without saving to disk
                await message.client.send_file(
                    message.chat_id,
                    file=img_url,
                    caption=f'<b>{ra.tag_string_general if ra.tag_string_general else "Untitled"}</b>',
                    parse_mode="html",
                    reply_to=message.reply_to_msg_id,
                )
                return await message.delete()

        if save_to_disk and num_images > 1:
            # Send as media group
            await message.client.send_file(
                message.chat_id,
                [m["file"] for m in media_group],
                caption=f"<b><i>Here's your {num_images} images y~you pervert! ಠ⁠_⁠ಠ </i></b>",
                parse_mode="html",
                reply_to=message.reply_to_msg_id,
            )

            # Remove saved files from disk after sending
            for i in range(num_images):
                os.remove(f"booru_image_{i}.jpg")

        await message.delete()

    except Exception as e:
        await message.eor(f"Error:\n>> `{e}`")
