# sauce.py plugin for ultroid bot
# Author: @NEOMATRIX90

import requests
import aiohttp
import os
import tempfile

TRACE_API = "https://api.trace.moe/search"
ANILIST_API = "https://graphql.anilist.co"
TRACE_KEY = None  # Optional


@ultroid_cmd(pattern="sauce$")
async def sauce_local_upload(event):
    reply = await event.get_reply_message()
    if not reply or not reply.media:
        return await event.eor("❌ Reply to an image or video.", 5)

    msg = await event.eor("📥 Downloading media...")

    try:
        # Save media to temp file
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp_path = tmp.name
        await event.client.download_media(reply, file=tmp_path)
        tmp.close()

        # Guess MIME
        mime_type = (
            reply.document.mime_type if hasattr(reply, "document") and reply.document else
            "image/jpeg" if reply.photo else
            "application/octet-stream"
        )

        headers = {"Content-Type": mime_type}
        # if TRACE_KEY:
        #     headers["x-trace-key"] = TRACE_KEY

        with open(tmp_path, "rb") as file:
            res = requests.post(TRACE_API, data=file, headers=headers)

        os.unlink(tmp_path)

        if res.status_code != 200:
            return await msg.edit(f"❌ trace.moe error: {res.status_code}")

        data = res.json()
        if not data.get("result"):
            return await msg.edit("❌ No results found.")

        top = data["result"][0]
        similarity = round(top["similarity"] * 100, 1)
        timestamp = format_time(top["from"])
        filename = top.get("filename", "unknown")
        episode = top.get("episode", "unknown")
        video = top.get("video")
        anilist_id = top.get("anilist")

        anime_title = await get_anilist_info(anilist_id)

        caption = (
            f"**🎬 Title:** `{anime_title}`\n"
            f"**📂 File:** `{filename}`\n"
            f"**📺 Episode:** `{episode}`\n"
            f"**⏱ Time:** `{timestamp}`\n"
            f"**🔎 Similarity:** `{similarity}%`"
        )

        if video:
            await event.client.send_file(
                event.chat_id,
                video,
                caption=caption,
                buttons=buttons,
                reply_to=reply.id
            )
            return await msg.delete()

        await msg.edit(caption)

    except Exception as e:
        await msg.edit(f"❌ Error: `{str(e)}`")


async def get_anilist_info(anilist_id):
    query = """
    query($id: Int) {
      Media(id: $id, type: ANIME) {
        title {
          romaji
          english
          native
        }
      }
    }
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
            ANILIST_API,
            json={"query": query, "variables": {"id": anilist_id}},
        ) as resp:
            res = await resp.json()
            titles = res["data"]["Media"]["title"]
            return ", ".join(
                filter(None, [titles.get("romaji"), titles.get("english"), titles.get("native")])
            )


def format_time(seconds):
    s = int(seconds)
    return f"{s//3600:02}:{(s%3600)//60:02}:{s%60:02}"