"""
✘ Commands Available -

• `{i}pint`
    __Get images from pinterest.__
"""

import asyncio
import io
import os

import aiofiles
import requests
from PIL import Image

# Pinterest API URL
API_URL = "https://bk9.fun/pinterest/search?q="


# Resize the image if it's larger than 1280x1280
def resize_image(image_bytes):
    try:
        with Image.open(image_bytes) as img:
            max_size = (1280, 1280)
            if img.size > max_size:
                img.thumbnail(max_size)
                output = io.BytesIO()
                img.save(output, format="JPEG")
                output.seek(0)
                return output
            image_bytes.seek(0)  # Reset pointer if not resized
            return image_bytes
    except Exception as e:
        print(f"Error resizing image: {e}")
        return image_bytes


# Download image from the URL and resize it
async def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img_bytes = io.BytesIO(response.content)
            return resize_image(img_bytes)
    except Exception as e:
        print(f"Error downloading image: {e}")
    return None


# Command for Pinterest search
@ultroid_cmd(pattern="pint ?(.*)$")
async def pinterest_search(event):
    args = event.pattern_match.group(1).strip().split()

    if len(args) < 1:
        return await event.eor("Usage: `.pint [number] <query>`")

    num_pics = 5  # Default number of pictures
    query = " ".join(args)

    if args[0].isdigit():
        num_pics = int(args[0])
        query = " ".join(args[1:])

    if not query:
        return await event.eor("`Please provide a search query.`", 5)

    status_message = await event.eor("__Searching for images...__")

    # API Request
    url = f"{API_URL}{query}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("status"):
            urls = [item["images_url"] for item in data.get("BK9", [])[:num_pics]]
            images = [download_image(img_url) for img_url in urls]

            # Download the images asynchronously
            downloaded_images = await asyncio.gather(*images)

            media_group = []
            for img_bytes in downloaded_images:
                if img_bytes:
                    img_bytes.seek(0)  # Ensure pointer is at the start
                    # Save to disk
                    filename = "pinterest_image.jpg"
                    async with aiofiles.open(filename, "wb") as f:
                        await f.write(img_bytes.read())

                    # Upload the image to Telethon
                    file = await event.client.upload_file(filename)

                    media_group.append(file)

            if media_group:
                await status_message.edit("__Uploading pictures...__")

                # Send all photos as a media group
                await event.client.send_file(
                    event.chat_id,
                    file=media_group,
                    caption=f"__Search results for {query}__",
                    reply_to=event.reply_to_msg_id,
                )
                os.remove(filename)

                await status_message.delete()
            else:
                await status_message.edit("No valid images found.")
        else:
            await status_message.edit("No images found for the given query.")
    else:
        await status_message.edit("An error occurred, please try again later.")
