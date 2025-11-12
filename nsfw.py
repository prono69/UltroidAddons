"""
❍ Commands Available -

• `{i}nm or {i}nm <type>`
    __Sends a SFW waifu.__

• `{i}nm -n or {i}nm -n <type>`
    __Sends a NSFW waifu.__

~ NSFW: `ass` `ecchi` `ero` `milf` `hentai` `oral` `paizuri`

~ VERSITILE: `maid` `marin-kitagawa` `mori-calliope` `oppai`
     `raiden-shogun` `selfies` `uniform` `waifu`

✘ `{i}fan <count> or {i}fan -h (for list)`
    __Sends a NSFW image from the api.__

**>> Default count set to 1**
"""

import os
import subprocess
from random import choice

import aiofiles
import aiohttp
import requests
from telethon.errors import PhotoSaveFileInvalidError, WebpageCurlFailedError

from . import ultroid_cmd

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
    "kamisato-ayaka",
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
async def waifu_im(event):
    input_args = event.pattern_match.group(1).strip()
    num_images = 1
    is_nsfw = False
    query = ""
    reply_to = event.reply_to_msg_id

    args = input_args.split()
    if len(args) >= 1:
        if args[0].isdigit():
            num_images = int(args[0])
            query = " ".join(args[1:])
        else:
            query = " ".join(args)

    is_nsfw = "-n" in args
    query = query.replace("-n", "").strip()  # Remove '-n' flag from the query

    if not query:
        query = "random"

    # Validate category if provided
    if query and query not in waifu_help and query != "random":
        return await event.eor(
            f"❌ Invalid Category!\nHere's the Category list:\n{waifu_help}",
            time=10,
        )

    # Construct the API URL
    base_url = "https://api.waifu.im/search/"
    params = {
        "is_nsfw": str(is_nsfw).lower(),
    }
    if num_images > 1:
        params["limit"] = num_images
    if query != "random":
        params["included_tags"] = query

    # Fetch data from API
    response_msg = await event.eor(f"__Fetching {num_images} {query} images...__")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(base_url, params=params) as resp:
                if resp.status != 200:
                    return await response_msg.edit(
                        f"Error: API responded with status code `{resp.status}`"
                    )

                data = await resp.json()
                images = [img["url"] for img in data.get("images", [])]

                if not images:
                    return await response_msg.edit(
                        f"No images found for the query {query}"
                    )

        except Exception as e:
            return await response_msg.edit(f"Error: {e}")

    if num_images == 1:
        try:
            await event.client.send_file(
                event.chat_id, images[0], caption=f"__**{query}**__", reply_to=reply_to
            )
        except PhotoSaveFileInvalidError:
            await event.client.send_file(
                event.chat_id,
                images[0],
                caption=f"__**{query}**__",
                force_document=True,
                reply_to=reply_to,
            )
        except WebpageCurlFailedError:
            return await event.eor(
                "__Failed to get media from web. Webpage media empty (caused by SendMediaRequest)__",
                7,
            )
        await response_msg.delete()
    else:
        media_group = []
        temp_dir = "./temp_images"
        os.makedirs(temp_dir, exist_ok=True)

        try:
            for idx, img_url in enumerate(images):
                file_path = os.path.join(temp_dir, f"image_{idx + 1}.jpg")
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(img_url) as img_resp:
                            if img_resp.status == 200:
                                async with aiofiles.open(file_path, mode="wb") as f:
                                    await f.write(await img_resp.read())
                                media_group.append(file_path)
                            else:
                                await event.eor(f"`Error fetching image {idx + 1}`")
                except Exception as e:
                    await event.eor(f"`Error saving image {idx + 1}: {e}`")
                    continue

            if media_group:
                await event.client.send_file(
                    event.chat_id,
                    file=media_group,
                    caption=f"__Here's your {num_images} {query} images__",
                    reply_to=reply_to,
                )

        finally:
            for file_path in media_group:
                if os.path.exists(file_path):
                    os.remove(file_path)
            os.rmdir(temp_dir)  # Remove temp directory

        await response_msg.delete()


NSFW = [
    "animal",
    "animalears",
    "anusview",
    "ass",
    "barefoot",
    "beach",
    "bed",
    "bell",
    "bikini",
    "blonde",
    "bondage",
    "bra",
    "breast",
    "breasthold",
    "breasts",
    "bunnyears",
    "bunnygirl",
    "catgirl",
    "chain",
    "close",
    "cloudsview",
    "cum",
    "demon",
    "dress",
    "drunk",
    "elbowgloves",
    "erectnipples",
    "fateseries",
    "fingering",
    "flatchest",
    "food",
    "foxgirl",
    "gamecg",
    "genshin",
    "glasses",
    "gloves",
    "greenhair",
    "gun",
    "hatsunemiku",
    "headband",
    "headdress",
    "headphones",
    "hololive",
    "horns",
    "idol",
    "japanesecloths",
    "loli",
    "maid",
    "necklace",
    "neko",
    "nipples",
    "nobra",
    "nude",
    "openshirt",
    "pantypull",
    "pantyhose",
    "penis",
    "pinkhair",
    "ponytail",
    "pussy",
    "ribbons",
    "schoolswimsuit",
    "schooluniform",
    "seethrough",
    "sex",
    "sex2",
    "sex3",
    "shirt",
    "shirtlift",
    "shorts",
    "skirt",
    "spreadlegs",
    "spreadpussy",
    "squirt",
    "stockings",
    "stokings",
    "sunglasses",
    "swimsuit",
    "tail",
    "tattoo",
    "tears",
    "thighhighs",
    "tie",
    "topless",
    "tornclothes",
    "touhou",
    "tree",
    "twintails",
    "twogirls",
    "uncensored",
    "underwear",
    "vampire",
    "vocaloid",
    "weapon",
    "wet",
    "white",
    "whitehair",
    "wings",
    "withflowers",
    "withpetals",
    "wolfgirl",
    "yuri",
]

fantox_help = "**🔞 NSFW** :  "
fantox_help += "   ".join(f"`{i.lower()}`" for i in NSFW)


@ultroid_cmd(pattern="fan ?(.*)$")
async def fanbox(event):
    args = event.pattern_match.group(1).strip().split()
    num_images = 1
    query = ""

    if len(args) >= 1:
        if args[0].isdigit():
            num_images = int(args[0])
            query = " ".join(args[1:])
        else:
            query = " ".join(args)

    if query == "-h":
        return await event.eor(f"**Here's your tags!**\n\n{fantox_help}", 15)

    # If no query is provided or invalid, choose randomly
    if not query or query not in NSFW:
        if query and query not in NSFW:
            return await event.eor(
                f"**❌ Invalid tag!**\n\nChoose from:\n{fantox_help}", 15
            )
        query = choice(NSFW)

    if num_images > 10:
        return await event.eor("__⚠️ You can fetch up to 10 images at once.__", 5)

    msg = await event.eor(f"__Fetching {num_images} image(s) for {query}...__")

    try:
        if num_images == 1:
            response = requests.get(f"https://fantox-apis.vercel.app/{query}")
            pic_url = response.json().get("url")

            filename = "single_image.jpg"
            try:
                subprocess.run(["wget", "-O", filename, pic_url], check=True)
                caption = f"__Here is your {query} image! 🖼__️\n©️ @Neko_Drive"
                try:
                    await event.client.send_file(
                        event.chat_id,
                        file=filename,
                        caption=caption,
                        reply_to=event.reply_to_msg_id,
                    )
                except PhotoSaveFileInvalidError:
                    await event.client.send_file(
                        event.chat_id,
                        file=pic_url,
                        captain=caption,
                        force_document=True,
                        reply_to=event.reply_to_msg_id,
                    )
                os.remove(filename)
            except Exception as e:
                await msg.edit(f"❌ Error downloading the image: `{e}`")
        else:
            media_list = []

            async with aiohttp.ClientSession() as session:
                for i in range(num_images):
                    try:
                        response = await session.get(
                            f"https://fantox-apis.vercel.app/{query}"
                        )
                        json_data = await response.json()
                        pic_url = json_data.get("url")

                        # Save image locally using aiofiles
                        filename = f"temp_{i}.jpg"
                        async with session.get(pic_url) as img_response:
                            if img_response.status == 200:
                                async with aiofiles.open(filename, "wb") as out_file:
                                    await out_file.write(await img_response.read())
                                media_list.append(filename)
                    except Exception as e:
                        await msg.edit(f"❌ Error fetching image {i + 1}: `{e}`")
                        continue

            # Send images as an album
            caption = f"__Here are your {num_images} {query} images! 🖼️__\n©️ @Neko_Drive"
            await event.client.send_file(
                event.chat_id,
                file=media_list,
                caption=caption,
                reply_to=event.reply_to_msg_id,
            )

            # Remove local files
            for file in media_list:
                try:
                    os.remove(file)
                except Exception:
                    continue
        await msg.delete()
    except Exception as e:
        await msg.edit(f"❌ An error occurred: `{e}`")
