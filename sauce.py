# sauce.py plugin for ultroid bot
# Author: @NEOMATRIX90

import aiohttp

TRACE_API = "https://api.trace.moe/search"
ANILIST_API = "https://graphql.anilist.co"
# TRACE_KEY = "your_trace_moe_key_here"  # Optional


@ultroid_cmd(pattern="sauce$")
async def sauce_upload(event):
    reply = await event.get_reply_message()
    if not reply or not reply.media:
        return await event.eor("❌ Please reply to an image or video message.", 7)

    msg = await event.eor("🔍 __Searching for anime sauce...__")

    try:
        # Download file into memory and get MIME type
        mime = (
            reply.document.mime_type
            if reply.document
            else ("image/jpeg" if reply.photo else None)
        )
        if not mime:
            return await event.eor("❌ Could not detect MIME type.", 7)

        file = await event.client.download_media(reply, file=bytes)
        headers = {"Content-Type": mime}
        # if TRACE_KEY:
        # headers["x-trace-key"] = TRACE_KEY

        async with aiohttp.ClientSession() as session:
            async with session.post(TRACE_API, data=file, headers=headers) as resp:
                if resp.status != 200:
                    return await event.eor(f"❌ trace.moe error: `{resp.status}`", 7)
                data = await resp.json()

        if not data.get("result"):
            return await event.eor("❌ No matching anime found.", 7)

        top = data["result"][0]
        similarity = round(top["similarity"] * 100, 1)
        timestamp = format_time(top["from"])
        filename = top.get("filename", "unknown")
        episode = top.get("episode", "unknown")
        video = top.get("video")
        anilist_id = top.get("anilist")

        anime_title = await get_anilist_info(anilist_id)

        caption = (
            f"**Title:** `{anime_title}`\n"
            f"**File:** `{filename}`\n"
            f"**Episode:** `{episode}`\n"
            f"**Time:** `{timestamp}`\n"
            f"**Similarity:** `{similarity}%`"
        )

        if video:
            await event.client.send_file(
                event.chat_id, video + "&size=l", caption=caption, reply_to=reply.id
            )
            return await msg.delete()

        await msg.edit(caption)

    except Exception as e:
        await event.eor(f"❌ Error: `{str(e)}`", 7)


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
                filter(
                    None,
                    [titles.get("romaji"), titles.get("english"), titles.get("native")],
                )
            )


def format_time(seconds):
    s = int(seconds)
    return f"{s // 3600:02}:{(s % 3600) // 60:02}:{s % 60:02}"
