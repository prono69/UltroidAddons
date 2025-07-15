"""
✘ Commands Available -

• `{i}hen`
    __Get information about top 5 trending hentai of the week.__
"""

import os

import aiofiles
import requests
from addons.shen import format_number


@ultroid_cmd(pattern="hen(?: |$)(.*)")
async def hentai_trend(event):
    # Get the time period from the command (default to "week")
    time_period = event.pattern_match.group(1).strip().lower() or "week"

    # Validate time period
    valid_periods = ["day", "week", "month", "year"]
    if time_period not in valid_periods:
        await event.eor(f"Invalid time period! Use one of: {', '.join(valid_periods)}")
        return

    period_display = {
        "day": "24 Hours",
        "week": "Week",
        "month": "Month",
        "year": "Year",
    }.get(time_period, "Week")

    kk = await event.eor(
        f"__Fetching top trending hentai of the {period_display.lower()}...__"
    )

    try:
        res = requests.get(
            f"https://htv-api.vercel.app/trending/{time_period}?limit=10"
        )
        res.raise_for_status()

        json_data_ = res.json()
        json_data = json_data_.get("results")

        if not json_data or len(json_data) == 0:
            return await kk.edit("No data found", time=5)

        # Get the top 5 trending hentai
        top_trending = json_data[:5]

        # Prepare the media group (album) and the caption details
        media_group = []
        caption_message = f"🔥 **Top 5 Trending Hentai of the {period_display}** 🔥\n\n"

        for index, data in enumerate(top_trending, 1):
            message_part = (
                f"**{index}.** `{data['name']}`\n"
                f"   - **📎 Link:** __https://hanime.tv/videos/hentai/{data['slug']}__\n"
                f"   - **👁️ Views:** `{format_number(data['views'])}`\n\n"
            )
            caption_message += message_part

            cover_url = data.get("cover_url", "")

            # Download the cover image
            filename = f"hentai_cover_{index}.jpg"
            cover_response = requests.get(cover_url)
            if cover_response.status_code == 200:
                async with aiofiles.open(filename, "wb") as f:
                    await f.write(cover_response.content)

                # Add to media group (the album)
                media_group.append(await event.client.upload_file(filename))

                # Remove the file after adding to media group
                os.remove(filename)
            else:
                await event.eor(f"Failed to fetch image for {data['name']}", 5)

        # Send the media group (album) with the combined caption
        await event.client.send_file(
            event.chat_id,
            media_group,
            caption=caption_message,
            reply_to=event.reply_to_msg_id,
        )

        await kk.delete()

    except requests.exceptions.RequestException as e:
        await kk.edit(f"ERROR: Failed to fetch data. Try again later.\n\n`{str(e)}`")
    except Exception as e:
        await kk.edit(f"An error occurred: \n\n`{str(e)}`")
