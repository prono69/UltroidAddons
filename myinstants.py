# Created by @cat_me_if_you_can on 12/1/23.
"""
> {i}rc (query)

• Examples:
> {i}rc john cena

"""

import os
import re

import requests
from bs4 import BeautifulSoup


@ultroid_cmd(pattern="rc (.+)")
async def rc_cmd(event):
    name_query = event.pattern_match.group(1)

    url = f"https://www.myinstants.com/en/search/?name={name_query}"
    headers = {
        "Host": "www.myinstants.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.101 Mobile Safari/537.36",
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    button_tags = soup.find_all(
        "button", class_="small-button", onclick=re.compile(r"play\('(.+?)',")
    )

    for button_tag in button_tags:
        data_src = button_tag["onclick"]
        match = re.search(r"play\('(.+?)',", data_src)

        if match:
            mp3_path = match.group(1)
            title_tag = button_tag.find_next("div", class_="title")
            title = title_tag.text.strip() if title_tag else "Unknown Title"

            audio_url = f"https://www.myinstants.com{mp3_path}"
            audio_response = requests.get(audio_url, headers=headers, cookies={})

            mp3_filename = f"{mp3_path.replace('/', '_')}.mp3"
            with open(mp3_filename, "wb") as audio_file:
                audio_file.write(audio_response.content)

            await event.client.send_file(
                event.chat_id,
                mp3_filename,
                reply_to=event.reply_to_msg_id,
                voice_note=True,
            )
            await event.delete()
            os.remove(mp3_filename)
            break
    else:
        await event.edit(f"No results found for `{name_query}`.")
