"""
**FLUX IMAGE GENERATOR**

❍ Commands Available -

• `{i}fai <promt or reply>`
    __Generate image using prompts.__
"""

import io
import os
import time

import requests
from PIL import Image

from . import LOGS

HUGGING_TOKEN = os.getenv("HF2")


async def schellwithflux(args):
    API_URL = (
        "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    )
    headers = {"Authorization": f"Bearer {HUGGING_TOKEN}"}
    payload = {"inputs": args}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        LOGS.error(f"Error status {response.status_code}")
        return None
    return response.content


@ultroid_cmd(pattern="fai ?(.*)$")
async def imgfluxai_(message):
    ok = await message.eor("`Processing...`", 20)
    question = message.pattern_match.group(1)
    reply = await message.get_reply_message()
    if not question and message.is_reply:
        question = reply.text
    else:
        return await ok.edit("__Please provide a question for Flux.__")
    try:
        if not HUGGING_TOKEN:
            return await ok.edit("`HUGGING_TOKEN` is required to use this feature.")
        image_bytes = await schellwithflux(question)
        if image_bytes is None:
            return await ok.edit("__Failed to generate an image.__")
        seconds_uploading = await ok.edit("`Uploading image...`")
        seconds_time = time.time()
        with Image.open(io.BytesIO(image_bytes)) as img:
            img.save("flux_ai.jpg", format="JPEG")
        await message.client.send_file(message.chat_id, "flux_ai.jpg")
        await seconds_uploading.delete()
        os.remove("flux_ai.jpg")
    except Exception as e:
        LOGS.error(str(e))
        await message.edit(f"`An error occurred: {str(e)}`")
