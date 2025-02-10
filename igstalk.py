"""
**STALK INSTAGRAM PROFILE**

❍ Commands Available -

• `{i}igs <reply or ig username>`
    __Get details of a Instagram profile.__
"""

import io
import requests
import random
from addons.shen import format_number

apikey = udB.get_key('BETA_API')
betakey = random.choice(f'{apikey}'.split(' '))


@ultroid_cmd(pattern="igs ?(.*)$")
async def instagram_stalk(event):
    query = event.pattern_match.group(1)
    reply = await event.get_reply_message()

    if not query and event.is_reply:
        query = reply.text
    elif not query:
        return await event.eor(
            "Usage: `.igs <username>` or reply to a message containing the username.",
            time=5,
        )

    query = query.replace("@", "").strip()

    if query.startswith("https://www.instagram.com/"):
        query = query.split("/")[3].split("?")[0]

    kk = await event.eor(f"__Fetching `{query}'s` Instagram profile...__")

    url = f"https://api.betabotz.eu.org/api/stalk/ig?username={query}&apikey={betakey}"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json().get("result", {})
        if data:
            profile_pic_url = data.get("photoUrl", "")
            profile_pic_content = requests.get(profile_pic_url).content
            profile_pic_stream = io.BytesIO(profile_pic_content)
            profile_pic_stream.name = "profile.jpg"

            about = data.get("bio", "N/A")
            followers = data.get("followers", "N/A")
            following = data.get("following", "N/A")
            full_name = data.get("fullName", "N/A")
            is_private = data.get("is_private", "N/A")
            is_verified = data.get("is_verified", "N/A")
            posts = data.get("postsCount", "N/A")
            username = data.get("username", "N/A")
            # ext_url = data.get("external_url", "N/A")

            # Construct the caption for the profile data
            caption = (
                f"**Instagram Profile:**\n\n"
                f"**🍀 𝖥𝗎𝗅𝗅 𝖭𝖺𝗆𝖾:** `{full_name}`\n"
                f"**👤 𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾:** [{username}](https://instagram.com/{username})\n"
                # f"**🖇️ External URL:** __{ext_url}__\n"
                # f"**👁‍🗨 𝖯𝗋𝗂𝗏𝖺𝗍𝖾:** `{is_private}`\n"
                f"**👑 𝖵𝖾𝗋𝗂𝖿𝗂𝖾𝖽:** `{is_verified}`\n"
                f"**📸 𝖯𝗈𝗌𝗍𝗌:** `{format_number(posts)}`\n"
                f"**💫 𝖥𝗈𝗅𝗅𝗈𝗐𝖾𝗋𝗌:** `{format_number(followers)}`\n"
                f"**🍂 𝖥𝗈𝗅𝗅𝗈𝗐𝗂𝗇𝗀:** `{format_number(following)}`\n"
                f"**💬 𝖡𝗂𝗈:** `{about}`\n\n"
                "**</> @Neko_Drive**"
            )

            await event.client.send_file(
                event.chat_id,
                profile_pic_stream,
                caption=caption,
                reply_to=event.reply_to_msg_id,
            )
        else:
            await event.eor("`No data found for this Instagram user.`", time=5)

        await kk.delete()
    else:
        await event.eor("`An error occurred, please try again later.`", time=5)
