import asyncio
import os
import random

import aiofiles
import requests

# Random API key selection
fg_key = "rsS5ATdq I3VLye8v"
fg = random.choice(fg_key.split(" "))
zenkey = random.choice(f"{udB.get_key('ZEN_API')}".split(" "))

# API URLS
BASE = "https://deliriusapi-official.vercel.app/"
CN_API = "https://www.loliapi.com/acg/"
FG_API = "https://api.fgmods.xyz/api/"
GURU_API = "https://guruapi.tech/api/rnsfw/"
ZEN_API = "https://api.ouzen.xyz/api/"
SHIZO_API = "https://shizoapi.onrender.com/api/"

# Using a session for connection pooling
session = requests.Session()


async def delirus_api(query):
    # Determine the API URL and file name based on the query.
    if query == "ko":
        url = BASE + "nsfw/corean"
        file_name = "corean_image.png"
    elif query == "boobs":
        url = BASE + "nsfw/boobs"
        file_name = "boobs_image.png"
    elif query == "gal":
        url = BASE + "nsfw/girls"
        file_name = "girls_image.png"
    elif query == "loli":
        url = CN_API + "pe?type=url"
        file_name = "loli_pic.png"
    elif query == "lolip":
        url = CN_API + "pc?type=url"
        file_name = "lolipc_pic.png"
    elif query == "loli2":
        url = "https://weeb-api.vercel.app/loli"
        file_name = "loli2.jpg"
    elif query == "loli4":
        url = FG_API + f"img/loli?apikey={fg}"
        file_name = "loli4.jpg"
    elif query == "yuri":
        url = FG_API + f"nsfw-nime/yuri?apikey={fg}"
        file_name = "yuri.png"
    elif query == "cos":
        url = FG_API + f"nsfw/cosplay?apikey={fg}"
        file_name = "cosplay.png"
    elif query == "les":
        url = FG_API + f"nsfw/lesbian?apikey={fg}"
        file_name = "lesbian.jpeg"
    elif query == "pussy":
        url = FG_API + f"nsfw/pussy?apikey={fg}"
        file_name = "pussy.png"
    elif query == "boob1":
        url = FG_API + f"nsfw/boobs?apikey={fg}"
        file_name = "boob.png"
    elif query == "gand":
        url = GURU_API + "gand"
        file_name = "gand.png"
    elif query == "tits":
        url = GURU_API + "tits"
        file_name = "tits.png"
    elif query == "chut":
        url = GURU_API + "porn"
        file_name = "chut.png"
    elif query == "les2":
        url = GURU_API + "imglesbian"
        file_name = "glesbian.png"
    elif query == "galp":
        url = GURU_API + "packgirl"
        file_name = "galp.jpg"
    elif query == "yuri2":
        url = ZEN_API + f"animensfw/yuri?apikey={zenkey}"
        file_name = "yuri2.png"
    elif query == "mas":
        url = ZEN_API + f"animensfw/masturbation?apikey={zenkey}"
        file_name = "mbation.png"
    elif query == "cos2":
        url = f"https://api.ouzen.xyz/randomimage/cosplay?apikey={zenkey}"
        file_name = "cos2.png"
    elif query == "chi":
        url = SHIZO_API + "pies/china?apikey=shizo"
        file_name = "china.jpg"
    elif query == "hi":
        url = SHIZO_API + "pies/hijab?apikey=shizo"
        file_name = "hijab.jpg"
    elif query == "indo":
        url = SHIZO_API + "pies/Indonesia?apikey=shizo"
        file_name = "indo.jpg"
    elif query == "jap":
        url = SHIZO_API + "pies/japan?apikey=shizo"
        file_name = "japan.jpg"
    elif query == "ko2":
        url = SHIZO_API + "pies/korea?apikey=shizo"
        file_name = "korean.jpg"
    elif query == "ind":
        url = SHIZO_API + "pies/indian?apikey=shizo"
        file_name = "ind.jpg"
    elif query == "mal":
        url = SHIZO_API + "pies/malaysia?apikey=shizo"
        file_name = "mal.jpg"
    elif query == "thai":
        url = SHIZO_API + "pies/thailand?apikey=shizo"
        file_name = "thai.jpg"
    elif query == "vit":
        url = SHIZO_API + "pies/vietnam?apikey=shizo"
        file_name = "vit.jpg"
    elif query == "loli3":
        url = SHIZO_API + "sfw/loli?apikey=shizo"
        file_name = "loli3.jpg"
    elif query == "milf":
        url = SHIZO_API + "sfw/milf?apikey=shizo"
        file_name = "milf.jpg"
    else:
        return "Invalid query"

    try:
        # Using the session for connection reuse
        response = session.get(url, stream=True, timeout=60)

        if response.status_code == 200:
            if query in ["loli", "lolip"]:
                direct_image_url = response.text.strip()
                direct_image_url = direct_image_url.replace(".com/", ".cn/")
                image_response = session.get(direct_image_url, stream=True, timeout=60)

                if image_response.status_code == 200:
                    async with aiofiles.open(file_name, "wb") as file:
                        await file.write(image_response.content)
                    return os.path.abspath(file_name)
                else:
                    return f"Failed to download the image. Status code: {image_response.status_code}"
            else:
                async with aiofiles.open(file_name, "wb") as file:
                    await file.write(response.content)
                return os.path.abspath(file_name)
        else:
            return (
                f"Failed to retrieve the image URL. Status code: {response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"


@ultroid_cmd(pattern="de ?(.*)$")
async def r_pics(event):
    query = event.pattern_match.group(1)
    kk = await event.eor("__No horny...__")
    pic = await delirus_api(query if query else "loli")

    try:
        await event.client.send_file(event.chat_id, pic)
        os.remove(pic)
        await kk.delete()
    except Exception as e:
        await kk.edit(f"Error: `{e}`")
