# < Source - t.me/testingpluginnn >
# < Made for Ultroid by @Spemgod! >
# < https://github.com/TeamUltroid/Ultroid >
#
# 'TG Regex taken from @TheUserge'

"""
✘ **Download Forward restricted files!**

• **CMD:**
>  `{i}fdl <msg_link>`
>  `{i}fdl https://t.me/nofwd/14`
"""

import os
import re
import time
from datetime import datetime

from plugins.downloadupload import process_video
from telethon.errors.rpcerrorlist import MessageNotModifiedError

from . import LOGS, downloader, random_string, time_formatter

# Source: https://github.com/UsergeTeam/Userge/blob/master/userge/plugins/misc/download.py
REGEXA = r"^(?:(?:https|tg):\/\/)?(?:www\.)?(?:t\.me\/|openmessage\?)(?:(?:c\/(\d+))|(\w+)|(?:user_id\=(\d+)))(?:\/|&message_id\=)(\d+)(?:\?single)?$"
DL_DIR = "resources/downloads"


def rnd_filename(path):
    """Generate a random filename while preserving extension"""
    if not os.path.exists(path):
        return path
    spl = os.path.splitext(path)
    rnd = "_" + random_string(5).lower() + "_"
    return spl[0] + rnd + spl[1]


def ensure_directory():
    """Ensure download directory exists"""
    os.makedirs(DL_DIR, exist_ok=True)


async def cleanup_file(file_path):
    """Clean up downloaded file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        LOGS.error(f"Error cleaning up file {file_path}: {e}")


@ultroid_cmd(
    pattern="fdl(?: |$)((?:.|\n)*)",
)
async def fwd_dl(e):
    ensure_directory()
    ghomst = await e.eor("`checking...`")
    args = e.pattern_match.group(1)

    if not args:
        reply = await e.get_reply_message()
        if reply and reply.text:
            args = reply.message
        else:
            return await eod(ghomst, "Give a tg link to download", time=10)

    remgx = re.findall(REGEXA, args)
    if not remgx:
        return await ghomst.edit("`Probably an invalid Link!`")

    try:
        chat, id = [i for i in remgx[0] if i]
        if chat.isdigit():
            channel = int(f"-100{chat}")
        else:
            channel = chat
        msg_id = int(id)
    except Exception as ex:
        return await ghomst.edit("`Give a valid tg link to proceed`")

    try:
        msg = await e.client.get_messages(channel, ids=msg_id)
    except Exception as ex:
        return await ghomst.edit(f"**Error:**  `{ex}`")

    if not msg or not msg.media:
        return await ghomst.edit("`Message doesn't contain any media to download.`")

    start_ = datetime.now()
    dls = None

    try:
        if hasattr(msg.media, "photo"):
            dls = await e.client.download_media(msg, DL_DIR)
        elif hasattr(msg.media, "document"):
            fn = msg.file.name or f"{channel}_{msg_id}{msg.file.ext}"
            filename = os.path.join(DL_DIR, fn)
            # filename = rnd_filename(filename)  # Ensure unique filename

            try:
                dlx = await downloader(
                    filename,
                    msg.document,
                    ghomst,
                    time.time(),
                    f"Downloading {os.path.basename(filename)}...",
                )
                dls = dlx.name
            except MessageNotModifiedError as err:
                LOGS.exception(err)
                await ghomst.edit(str(err))
                return

        if not dls:
            return await ghomst.edit("`Download failed!`")

        end_ = datetime.now()
        ts = time_formatter(((end_ - start_).seconds) * 1000)
        caption = f"**Uploaded:**\n`{os.path.basename(dls)}`"

        await ghomst.edit(
            f"**Downloaded in {ts} !!**\n » `{dls}`\n\n⬆️ __Uploading Now__"
        )
        await process_video(dls, DL_DIR, caption, e)

    except Exception as ex:
        await ghomst.edit(f"**Error during processing:**\n`{str(ex)}`")
        LOGS.exception(ex)
    finally:
        if dls:
            await cleanup_file(dls)
        await ghomst.delete()
