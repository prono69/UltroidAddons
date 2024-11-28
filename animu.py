"""
──「 **Danbooru Search** 」──

❍ Commands Available -

• `{i}animu <query>` or `{i}aninsfw <nsfw query>`
    __Sends sfw or nsfw image from Danbooru.__

**✘ Tip:** __Put any number before the search query to send that number of images as album.__
"""

import os

import aiofiles
import aiohttp

from . import ultroid_cmd

# Create TEMP_DIR if it doesn't exist
TEMP_DIR = "temp_images"
os.makedirs(TEMP_DIR, exist_ok=True)


@ultroid_cmd(pattern=r"ani(mu|nsfw) (\d+)? ?([\s\S]*)")
async def danbooru(event):
    "Get anime character pic or nsfw images as media group."
    msg = await event.eor("`Processing...`")
    args = event.pattern_match.group(1)
    rating = "Explicit" if "nsfw" in args else "Safe"
    num_pics = int(event.pattern_match.group(2) or 1)
    search_query = event.pattern_match.group(3)

    # Search parameters
    params = {
        "limit": num_pics,
        "random": "true",
        "tags": f"Rating:{rating} {search_query}".strip(),
    }

    # API request
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://danbooru.donmai.us/posts.json", params=params
        ) as response:
            if response.status != 200:
                return await eor(event, f"Error: response code {response.status}")
            data = await response.json()

    if not data:
        return await event.eor(f"No results for query: __{search_query}__", 5)

    file_paths = []
    try:
        async with aiohttp.ClientSession() as session:
            # Download images and save to disk
            for index, post in enumerate(data[:num_pics]):
                image_url = next(
                    (
                        post.get(url)
                        for url in ["file_url", "large_file_url", "source"]
                        if url in post
                    ),
                    None,
                )
                if not image_url:
                    continue

                async with session.get(image_url) as img_resp:
                    if img_resp.status != 200:
                        continue
                    img_data = await img_resp.read()

                    file_path = os.path.join(TEMP_DIR, f"image_{index}.jpg")
                    async with aiofiles.open(file_path, "wb") as f:
                        await f.write(img_data)

                    file_paths.append(file_path)

        # Send images as a media group
        if file_paths:
            await event.client.send_file(
                event.chat_id,
                file=file_paths,
                caption=f"__Search results for {search_query}__",
                reply_to=event.reply_to_msg_id,
            )
        else:
            await event.eor("No valid images found.", 5)
    finally:
        # Clean up saved files
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)

    await msg.delete()
