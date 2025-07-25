"""
✘ Commands Available -

• `{i}shen <count> <query>`
    __Get information about the Hentai.__

**>> Default count set to 1**
"""

import asyncio
import os
import re

import aiofiles
import aiohttp
import requests

API_URL = "https://api-hanime-two.vercel.app/search?query="


def format_number(num):
    """Convert a large number into a shortened format."""
    if not isinstance(num, (int, float)):
        raise ValueError("Input must be a number")

    if num < 0:
        return "-" + format_number(-num)

    if num >= 1_000_000_000:
        return f"{num // 1_000_000_000}{'' if num % 1_000_000_000 == 0 else f'.{(num % 1_000_000_000) // 100_000_000:.0f}'}B"
    elif num >= 1_000_000:
        return f"{num // 1_000_000}{'' if num % 1_000_000 == 0 else f'.{(num % 1_000_000) // 100_000:.0f}'}M"
    elif num >= 1_000:
        return f"{num // 1_000}{'' if num % 1_000 == 0 else f'.{(num % 1_000) // 100:.0f}'}K"
    return str(num)


def truncate_text(text: str, limit: int = 300) -> str:
    return text if len(text) <= limit else f"{text[:limit].rstrip()}..."


def extract_slug_from_url(url):
    """
    Extracts the last part of a URL, removes the trailing hyphen and number,
    and replaces remaining hyphens with spaces.
    Example: https://hanime.tv/videos/hentai/iribitari-gal-ni-manko-tsukawasete-morau-hanashi-1
             -> iribitari gal ni manko tsukawasete morau hanashi
    """
    # Get the last part of the URL after the final slash
    last_part = url.rstrip("/").split("/")[-1]
    # Remove trailing hyphen and number (e.g., -1, -2, etc.)
    slug = re.sub(r"-\d+$", "", last_part)
    # Replace remaining hyphens with spaces
    slug = slug.replace("-", " ")
    return slug


async def download_file(url: str, save_path: str):
    """Download a file asynchronously using aiohttp."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(save_path, mode="wb") as f:
                    await f.write(await response.read())
    return save_path


@ultroid_cmd(pattern="shen ?([\d]*) ?(.*)")
async def hanime_search(event):
    args = event.pattern_match.groups()
    count = (
        int(args[0]) if args[0].isdigit() else 1
    )  # Default to 1 if no number is provided
    query = args[1]
    if event.is_reply and not query:
        reply = await event.get_reply_message()
        query = reply.text

    if query.startswith("http://") or query.startswith("https://"):
        query = extract_slug_from_url(query)

    if not query:
        return await event.eor("`Please provide a search query.`", 5)

    msg = await event.eor(f"__🔍 Searching for {query}...__")

    try:
        # Fetch data from the API
        response = requests.get(API_URL + query)
        response.raise_for_status()
        data = response.json()

        # Check if results exist
        if not data or "results" not in data or not data["results"]:
            return await event.eor("__No results found for your query.__", 5)

        results = data["results"][:count]  # Limit results to the specified count
        messages = []

        for result in results:
            name = result.get("name", "N/A")
            description = truncate_text(result.get("description", "No Description"))
            views = format_number(result.get("views", 0))
            likes = format_number(result.get("likes", 0))
            dislikes = format_number(result.get("dislikes", 0))
            is_censored = "Yes" if result.get("is_censored") else "No"
            brand = result.get("brand", "Unknown")
            monthly_rank = result.get("monthly_rank", "N/A")
            cover_url = result.get("cover_url", "")
            slug = result.get("slug", "")
            tags = result.get("tags", [])
            joined_tags = ", ".join(tags[:5]) if tags else "No tags available"
            is_futa = "Yes" if "futa" in tags or "futanari" in tags else "No"
            is_creampie = "Yes" if "creampie" in tags else "No"
            is_ntr = "Yes" if "ntr" in tags else "No"

            # Append "More Info" link to the description
            more_info_url = f"https://hanime.tv/videos/hentai/{slug}"
            description += f" <a href='{more_info_url}'>More Info</a>"

            # Construct the caption
            caption = (
                f"🎬 <b>{name}</b>\n\n"
                f"👀 <b>Views:</b> <code>{views}</code>\n"
                f"👍 <b>Likes:</b> <code>{likes}</code>\n"
                f"👎 <b>Dislikes:</b> <code>{dislikes}</code>\n"
                f"🔒 <b>Censored:</b> <code>{is_censored}</code>\n"
                f"🏢 <b>Brand:</b> <code>{brand}</code>\n"
                f"📊 <b>Monthly Rank:</b> <code>{monthly_rank}</code>\n"
                f"💦 <b>Creampie:</b> <code>{is_creampie}</code>\n"
                f"🍆 <b>Futa:</b> <code>{is_futa}</code>\n"
                f"⚠️ <b>NTR:</b> <code>{is_ntr}</code>\n"
                f"🏷️ <b>Tags:</b> <code>{joined_tags}</code>\n\n"
                f"📖 <b>Description:</b> <i>{description}</i>\n\n"
                f"©️ &lt;/&gt; @Neko_Drive"
            )

            # Prepare the message
            messages.append({"file_url": cover_url, "caption": caption})

        # Download, send, and delete files
        for message in messages:
            file_url = message["file_url"]
            file_path = f"{os.path.basename(file_url)}"
            await download_file(file_url, file_path)

            try:
                await event.client.send_file(
                    event.chat_id,
                    file=file_path,
                    caption=message["caption"],
                    parse_mode="html",
                    reply_to=event.reply_to_msg_id,
                )
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)

            await asyncio.sleep(1)

        await msg.delete()

    except requests.exceptions.RequestException as e:
        await event.eor(f"❌ API Request Failed: \n`{e}`", 5)
    except Exception as e:
        await event.eor(f"❌ An error occurred: \n`{e}`", 5)
