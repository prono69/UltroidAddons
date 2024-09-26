"""
❍ Commands Available -

• `{i}nm or {i}nm <type>`
    __Sends a SFW waifu.__

• `{i}nm -n or {i}nm -n <type>`
    __Sends a NSFW waifu.__

~ NSFW: `ass` `ecchi` `ero` `milf` `hentai` `oral` `paizuri`

~ VERSITILE: `maid` `marin-kitagawa` `mori-calliope` `oppai`
     `raiden-shogun` `selfies` `uniform` `waifu`
"""

import os
from random import choice

import requests
from pyUltroid.fns.misc import unsavegif
from telethon.errors import PhotoSaveFileInvalidError, WebpageCurlFailedError

# This list is for waifu.im
ISFW = [
    "maid",
    "marin-kitagawa",
    "mori-calliope",
    "oppai",
    "raiden-shogun",
    "selfies",
    "uniform",
    "waifu",
]

INSFW = [
    "ass",
    "ecchi",
    "ero",
    "hentai",
    "milf",
    "oral",
    "paizuri",
]

waifu_help = "**🔞 NSFW** :  "
for i in INSFW:
    waifu_help += f"`{i.lower()}`   "
waifu_help += "\n\n**😇 SFW** :  "
for m in ISFW:
    waifu_help += f"`{m.lower()}`   "


@ultroid_cmd(pattern="nm ?(.*)$")
async def _(event):
    "Search images from waifu.im"
    reply_to = event.reply_to_msg_id
    args = event.pattern_match.group(1).split()
    # Identify if '-n' flag is present
    is_nsfw = "-n" in args
    # Filter out the '-n' flag from args to get the actual category
    args = [arg for arg in args if arg != "-n"]
    # Choose category (if present)
    choose = args[0] if args else ""

    # Base URL
    url = "https://api.waifu.im"

    # Check if no category is provided and '-n' is used (random NSFW image)
    if choose == "" and is_nsfw:
        url = f"{url}/search/?is_nsfw=True"
    elif choose != "":
        # Add the category if it's provided
        if choose not in waifu_help:
            return await event.eor(
                f"**Wrong Category!!**\nHere's theCategory list (*_*)\n{waifu_help}", 20
            )
        url = f"{url}/search/?included_tags={choose}"
        if is_nsfw:
            url += "&is_nsfw=True"
    else:
        # If no category and no '-n', fetch a random SFW image
        url = f"{url}/search/"

    # Send request and process the response
    catevent = await event.eor("`Processing...`")
    resp = requests.get(url).json()
    target = resp["images"][0]["url"]

    # Send the image
    nohorny = await event.client.send_file(
        event.chat_id, file=target, caption=f"__**{choose}**__", reply_to=reply_to
    )

    # Optionally unsave the image
    try:
        await unsavegif(event, nohorny)
    except Exception:
        pass
    await catevent.delete()


NSFW = [
    "genshin",
    "swimsuit",
    "schoolswimsuit",
    "white",
    "barefoot",
    "touhou",
    "gamecg",
    "hololive",
    "uncensored",
    "sunglasses",
    "glasses",
    "weapon",
    "shirtlift",
    "chain",
    "fingering",
    "flatchest",
    "torncloth",
    "bondage",
    "demon",
    "wet",
    "pantypull",
    "headdress",
    "headphone",
    "tie",
    "anusview",
    "shorts",
    "stokings",
    "topless",
    "beach",
    "bunnygirl",
    "bunnyear",
    "idol",
    "vampire",
    "gun",
    "maid",
    "bra",
    "nobra",
    "bikini",
    "whitehair",
    "blonde",
    "pinkhair",
    "bed",
    "ponytail",
    "nude",
    "dress",
    "underwear",
    "foxgirl",
    "uniform",
    "skirt",
    "sex",
    "sex2",
    "sex3",
    "breast",
    "twintail",
    "spreadpussy",
    "tears",
    "seethrough",
    "breasthold",
    "drunk",
    "fateseries",
    "spreadlegs",
    "openshirt",
    "headband",
    "food",
    "close",
    "tree",
    "nipples",
    "erectnipples",
    "horns",
    "greenhair",
    "wolfgirl",
    "catgirl",
]

fantox_help = "**🔞 NSFW** :  "
fantox_help += "   ".join(f"`{i.lower()}`" for i in NSFW)


@ultroid_cmd(pattern="fan ?(.*)$")
async def fanbox(event):
    query = event.pattern_match.group(1)
    kk = await event.eor(f"__Fetching {query} image...__")

    if query == "-h" or query not in NSFW:
        return await kk.edit(f"**Here's your tags!**\n\n{fantox_help}")
    query = query or choice(NSFW)
    try:
        response = requests.get(f"https://fantox-apis.vercel.app/{query}")
        pic = response.json().get("url")

        await event.client.send_file(event.chat_id, pic)
        # Uncomment the line below to delete the pic after sending (if saved locally)
        # os.remove(pic)
    except PhotoSaveFileInvalidError:
        await event.client.send_file(event.chat_id, pic, force_document=True)
    except WebpageCurlFailedError:
        await event.client.send_file(event.chat_id, file="https://http.cat/404.jpg")

    await kk.delete()
