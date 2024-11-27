"""
Reverse image search handler.

Usage:
	- `.search [engine]`: Search with a specific engine (e.g., `lens`, `bing`).
	- `.search`: Search with all engines.
"""    

import requests
from io import BytesIO
import os
import urllib.parse

apiflash_key = udB.get_key("APIFLASH_KEY")

# API endpoints for reverse image search engines
SEARCH_ENGINES = {
    "lens": "https://lens.google.com/uploadbyurl?url={image}",
    "google": "https://www.google.com/searchbyimage?sbisrc=4chanx&image_url={image}&safe=off",
    "tineye": "https://www.tineye.com/search?url={image}",
    "bing": "https://www.bing.com/images/search?view=detailv2&iss=sbi&form=SBIVSP&sbisrc=UrlPaste&q=imgurl:{image}",
    "yandex": "https://yandex.com/images/search?source=collections&&url={image}&rpt=imageview",
    "saucenao": "https://saucenao.com/search.php?db=999&url={image}",
}

@ultroid_cmd(pattern="rev")
async def reverse_image_search(event):
    reply = await event.get_reply_message()
    if not event.is_reply or not reply.media:
        await event.eor("Please reply to an image with `.search [engine]` or `.search`.", 5)
        return

    command_parts = event.text.split(maxsplit=1)
    engines_to_use = (
        [command_parts[1].strip().lower()] 
        if len(command_parts) > 1 and command_parts[1].strip() 
        else ["google"])
    

    invalid_engines = [engine for engine in engines_to_use if engine not in SEARCH_ENGINES]
    if invalid_engines:
        await event.eor(
            f"Invalid engine(s): {', '.join(invalid_engines)}. Available: {', '.join(SEARCH_ENGINES.keys())}", 7
        )
        return

    msg = await event.eor("`Processing the image...`")

    try:
        # Download and upload the image
        photo_path = await reply.download_media()
        img_url = upload_image(photo_path)
        if not img_url:
            await msg.edit("Error: Could not upload the image.")
            return

        # Perform searches for the selected engines
        for engine in engines_to_use:
            search_url = SEARCH_ENGINES[engine].format(image=img_url)
            await send_screenshot(event, search_url, engine)
            await msg.delete()
    except Exception as e:
        await msg.edit(f"An error occurred: {e}")
    finally:
        if photo_path and os.path.exists(photo_path):
            os.remove(photo_path)

def upload_image(photo_path):
    """Uploads an image to tmpfiles.org and returns the direct download URL."""
    try:
        with open(photo_path, "rb") as image_file:
            response = requests.post(
                "https://tmpfiles.org/api/v1/upload", files={"file": image_file}
            )
        if response.status_code == 200:
            data = response.json()
            url = data["data"]["url"]
            pic_url = url.split("/")[-2] + "/" + url.split("/")[-1]
            direct_download_url = url.replace(f"/{pic_url}", f"/dl/{pic_url}")
            print(direct_download_url)
            return direct_download_url
        else:
            return None
    except Exception:
        return None

async def send_screenshot(event, url, engine_name):
    """Takes a screenshot of the URL and sends it to the chat."""
    screenshot_data = generate_screenshot(url)
    if screenshot_data:
        await event.client.send_file(
            event.chat_id,
            screenshot_data,
            caption=f"<b>{engine_name.capitalize()} Result</b>\nURL: <i>{url}</i>",
            parse_mode="html",
            reply_to=event.reply_to_msg_id,
        )
        os.remove(screenshot_data)
    else:
        await event.eor(f"Failed to take screenshot for {engine_name.capitalize()}.")

        
def generate_screenshot(url):
    api_url = f"https://api.apiflash.com/v1/urltoimage?access_key={apiflash_key}&url={urllib.parse.quote(url)}&format=png"
    response = requests.get(api_url)
    if response.status_code == 200:
        with open("webshot.jpg", "wb") as f:
            f.write(response.content)
        return "webshot.jpg"     
    return None
    