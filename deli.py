# Made by @NeoMatrix90
"""
**Get Random NSFW pics from the api**

❍ Commands Available -

• `{i}de`
    __Random nsfw image__

• `{i}de <query> (ko, boobs, gal, loli, lolp)`
    __Random nsfw image by query__
"""

import os
import shutil

import requests


def delirus_api(query):
    base = "https://deliriusapi-official.vercel.app/"
    cn_api = "https://www.loliapi.com/acg/"

    # Determine the API URL and file name based on the query
    if query == "ko":
        url = base + "nsfw/corean"
        file_name = "corean_image.png"
    elif query == "boobs":
        url = base + "nsfw/boobs"
        file_name = "boobs_image.png"
    elif query == "gal":
        url = base + "nsfw/girls"
        file_name = "girls_image.png"
    elif query == "loli":
        url = cn_api + "pe?type=url"
        file_name = "loli_pic.png"
    elif query == "lolp":
        url = cn_api + "pc?type=url"
        file_name = "lolipc_pic.png"
    else:
        return "Invalid query"

    try:
        # Request to get the direct image URL
        response = requests.get(url, stream=True, timeout=120)

        if response.status_code == 200:
            if query in ["loli", "lolp"]:
                # The API returns the direct image URL as plain text
                direct_image_url = response.text.strip()  # Strip any whitespace
                # Replace .com with .cn in the image URL
                direct_image_url = direct_image_url.replace(".com/", ".cn/")

                # Step 2: Download the image using the modified direct URL
                image_response = requests.get(
                    direct_image_url, stream=True, timeout=120
                )

                if image_response.status_code == 200:
                    # Save the content to a file
                    with open(file_name, "wb") as file:
                        shutil.copyfileobj(image_response.raw, file)
                    return os.path.abspath(
                        file_name
                    )  # Return the full path of the saved file
                else:
                    return f"Failed to download the image. Status code: {image_response.status_code}"
            else:
                # For other queries, directly save the response content using shutil
                with open(file_name, "wb") as file:
                    shutil.copyfileobj(response.raw, file)
                return os.path.abspath(
                    file_name
                )  # Return the full path of the saved file
        else:
            return (
                f"Failed to retrieve the image URL. Status code: {response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"


@ultroid_cmd(pattern="de ?(.*)$")
async def r_pics(event):
    query = event.pattern_match.group(1)
    kk = await event.eor("__No horny...__", 10)
    if not query:
        pic = delirus_api("loli")
    else:
        pic = delirus_api(query)
    try:
        await event.client.send_file(event.chat_id, pic)
        os.remove(pic)
        await kk.delete()
    except Exception as e:
        await kk.edit(f"Error `{e}`")
