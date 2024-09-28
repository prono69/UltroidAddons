"""
**FLUX IMAGE GENERATOR**

❍ Commands Available -

• `{i}fai <promt or reply>`
    __Generate image using prompts.__
"""

import os

import requests


@ultroid_cmd(pattern="fai ?(.*)$")
async def flux_ai(event):
    # Extract the query from the user's input
    query = event.pattern_match.group(1)
    reply = await event.get_reply_message()

    if not query and event.is_reply:
        query = reply.text

    url = "https://private-akeno.randydev.my.id/akeno/fluxai"
    data = {"args": query}
    kk = await event.eor("__Generating image...__")
    try:
        response = requests.post(url, json=data)

        if response.status_code == 200:
            filename = "flux_image.jpg"
            with open(filename, "wb") as f:
                f.write(response.content)

            # Send the image to the chat
            await event.client.send_file(
                event.chat_id, filename, caption="__Here is your generated image!__"
            )

            os.remove(filename)
            await kk.delete()

        else:
            await kk.edit(f"Error: {response.status_code}\n`{response.text}`")

    except requests.exceptions.RequestException as e:
        await kk.edit(f"Failed to generate image: `{str(e)}`")

    except Exception as e:
        await kk.edit(f"An error occurred: `{str(e)}`")
