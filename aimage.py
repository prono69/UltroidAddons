"""
✘ Commands Available -

• `{i}getai <reply to image>`
    __Get details of image with Ai.__
    
• `{i}aicook <reply to image>`
    __Generate Cooking instrunctions of the given food image.__
    
• `{i}aiseller <target audience> <reply to product image>`
    __Generate a promotional message for the given image product for the given target audience.__    
"""

import os
import PIL
import json
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from . import ultroid_cmd, udB, HNDLR

gemini_key = udB.get_key("GOOGLEAPI")
genai.configure(api_key=f"{gemini_key}")

generation_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

generation_config_cook = {
    "temperature": 0.35,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    generation_config=generation_config,  # Ensure this is defined elsewhere
    safety_settings=[
        {"category": "harassment", "threshold": "block_none"},
        {"category": "hate", "threshold": "block_none"},
        {"category": "sex", "threshold": "block_none"},
        {"category": "danger", "threshold": "block_none"}
    ]
)

model_cook = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest", generation_config=generation_config_cook
)

@ultroid_cmd(pattern="getai$")
async def getai(event):
    try:
        kk = await event.eor("`Please Wait...`")
        base = await event.get_reply_message()
        
        # Check if the base message has media
        if not base or not base.media:
            await kk.edit("Please reply to an image.")
            return
        
        base_img = await base.download_media()

        # Open the downloaded image
        img = PIL.Image.open(base_img)
        
        # Call the model to generate content with safety settings
        response_ = model.generate_content(
            img
        )
        
        # Extract and parse the text content
        text_content = response_.candidates[0].content.parts[0].text
        parsed_content = json.loads(text_content)
        
        # Safely get the description or error message
        response = parsed_content.get("description") or parsed_content.get("image_description") or parsed_content.get("caption") or parsed_content.get("error")

        # Edit the message with the response
        await kk.edit(f"**Details Of Image:** \n__{response}__")
        
    except Exception as e:
        # Handle any errors and send an error message
        await eod(event, f"An error occurred: {e}")
    
    finally:
        # Ensure the downloaded image is removed
        if os.path.exists(base_img):
            os.remove(base_img)


@ultroid_cmd(pattern="aicook$")
async def aicook(event):
    if event.get_reply_message():
        try:
            kk = await event.eor("`Cooking...`")
            base = await event.get_reply_message()
            base_img = await base.download_media()

            img = PIL.Image.open(base_img)
            cook_img = [
                "Accurately identify the baked good in the image and provide an appropriate and recipe consistent with your analysis. ",
                img,
            ]

            response = model_cook.generate_content(cook_img)

            await kk.edit(
                f"__{response.text}__"
            )
            os.remove(base_img)
            return
        except Exception as e:
            await eod(event, str(e))
    return await eod(event, "__Kindly reply to an image!__")


@ultroid_cmd(pattern="aiseller ?(.*)")
async def aiseller(event):
    if event.get_reply_message():
        try:
            kk = await event.eor("`Generating...`")
            if len(event.pattern_match.group(1)) > 1:
                taud = event.text.split(maxsplit=1)[1]
            else:
                return await eod(
                    event, f"<b>Usage: </b><code>{HNDLR}aiseller [target audience] [reply to product image]</code>", parse_mode="html"
                )

            base = await event.get_reply_message()
            base_img = await base.download_media()

            img = PIL.Image.open(base_img)
            sell_img = [
                "Given an image of a product and its target audience, write an engaging marketing description",
                "Product Image: ",
                img,
                "Target Audience: ",
                taud,
            ]

            response = model.generate_content(sell_img)

            await kk.edit(
                f"__{response.text}__"
            )
            os.remove(base_img)
            return
        except Exception:
            await eod(
                event, f"<b>Usage: </b><code>{HNDLR}aiseller [target audience] [reply to product image]</code>", parse_mode="html"
            )
    return await eod(event, "__Kindly reply to an image!__")

