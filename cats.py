# Ultroid plugin to fetch cat images or gifs from cataas.com
# Author: @NEOMATRIX90

import io
import os
import tempfile

import aiohttp
from pyUltroid.fns.misc import unsavegif

CAT_IMG_API = "https://cataas.com/cat"
CAT_GIF_API = "https://cataas.com/cat/gif"


@ultroid_cmd(pattern="cats(?: (\d+))?(?:\s+gif)?$")
async def cat_cmd(event):
    match = event.pattern_match.group(1)
    is_gif = "gif" in event.text.lower()
    await event.edit(f"🐾 __Fetching {match} cats...__ 🐾")

    api_url = CAT_GIF_API if is_gif else CAT_IMG_API

    try:
        num = int(match) if match else 1
        if num < 1:
            return await event.eor("❌ Number must be at least 1.", 5)
        if num > 10:
            return await event.eor(
                "⚠️ Maximum 10 items allowed due to Telegram limits.", 5
            )
    except ValueError:
        return await event.eor("❌ Invalid number.", 5)

    if num == 1:
        # For single image or gif, stream and send directly
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{api_url}") as resp:
                    if resp.status == 200:
                        data = await resp.read()

                        file_obj = io.BytesIO(data)
                        file_obj.name = f"cat{'.gif' if is_gif else '.jpg'}"

                        sent = await event.client.send_file(
                            event.chat_id,
                            file=file_obj,
                            # force_document=is_gif,
                            caption="😺 **__meyaoooooooooo__** 😺",
                            reply_to=event.reply_to_msg_id,
                        )
                        if is_gif:
                            await unsavegif(event, sent)
                        return await event.delete()
                    else:
                        return await event.eor("⚠️ Failed to fetch media.", 5)
            except Exception as e:
                return await event.eor(f"🚫 Error: {e}", 5)
    else:
        # For multiple images/gifs: download and send as media group
        temp_dir = tempfile.mkdtemp()
        files = []

        async with aiohttp.ClientSession() as session:
            for i in range(num):
                try:
                    url = f"{api_url}"
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            raw = await resp.read()
                            ext = ".gif" if is_gif else ".jpg"
                            path = os.path.join(temp_dir, f"cat_{i + 1}{ext}")
                            with open(path, "wb") as f:
                                f.write(raw)
                            files.append(path)
                        else:
                            return await event.eor(
                                f"❌ Failed to fetch media #{i + 1}", 5
                            )
                except Exception as e:
                    return await event.eor(f"🚫 Error fetching media #{i + 1}: {e}", 5)

        try:
            sent = await event.client.send_file(
                event.chat_id,
                file=files,
                caption=(
                    "😺 **__Bunch of Pussies!__** 😺\n🐈 **__meyaoooooooooo__** 🐈"
                    if not is_gif
                    else "🐅️ **__Cat bomb incoming!__** 🐅\n**__meyaoooooooooo__**"
                ),
                reply_to=event.reply_to_msg_id,
                # force_document=is_gif,
            )

            if is_gif:
                # sent can be a list if media group
                if isinstance(sent, list):
                    for m in sent:
                        await unsavegif(event, m)
                else:
                    await unsavegif(event, sent)
        except Exception as e:
            return await event.eor(f"🚫 Failed to send media group: {e}", 5)
        finally:
            for f in files:
                if os.path.exists(f):
                    os.remove(f)
            os.rmdir(temp_dir)

        await event.delete()
