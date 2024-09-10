"""
✘ Commands Available -

• `{i}booru`
    __Send a random image from Danbooru.__
"""

from . import ultroid_cmd
from aiohttp import ClientSession
from io import BytesIO

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
            else self.large_file_url
            if self.large_file_url
            else self.source
            if self.source and "pximg" not in self.source
            else await self.pximg
            if self.source
            else None
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
async def anime_handler(message):
    try:
        await message.eor("<b>Searching art</b>", parse_mode="html")
        ra = await random()
        img = await ra.image
        await message.client.send_file(
            message.chat_id,
            file=img,
            caption=f'<b>{ra.tag_string_general if ra.tag_string_general else "Untitled"}</b>',
            parse_mode="html"
        )
        return await message.delete()
    except Exception as e:
        await eod(message, f"Error:\n>> `{e}`", parse_mode="html")
