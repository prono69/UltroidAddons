"""
Transcribe an audio URL using the Gladia API.

Usage: .ytrans <audio_url>
"""

import os
import time

import requests
from telethon.errors.rpcerrorlist import MessageTooLongError

# Replace with your Gladia API key
gladia_key = f"{udB.get_key('GLADIA_API')}"
gladia_url = "https://api.gladia.io/v2/transcription/"


# Function to make fetch requests to the Gladia API
def make_fetch_request(url, headers, method="GET", data=None):
    if method == "POST":
        response = requests.post(url, headers=headers, json=data)
    else:
        response = requests.get(url, headers=headers)
    return response.json()


@ultroid_cmd(pattern="ytrans ?(.*)$")
async def transcribe_audio(message):
    query = message.pattern_match.group(1)
    reply = await message.get_reply_message()
    audio_url = query if query else None

    # Check if a valid URL was provided
    if not audio_url:
        await message.eor("Please provide a valid audio URL.")
        return

    headers = {"x-gladia-key": gladia_key, "Content-Type": "application/json"}

    request_data = {"audio_url": audio_url}

    # Send initial request to Gladia API
    status_message = await message.eor("- Sending initial request to Gladia API...")
    initial_response = make_fetch_request(gladia_url, headers, "POST", request_data)

    # Check if the response contains the result_url
    if "result_url" not in initial_response:
        await status_message.edit(f"Error in transcription request: {initial_response}")
        return

    result_url = initial_response["result_url"]
    await status_message.edit(
        f"Initial request sent. Polling for transcription results..."
    )

    # Polling for transcription result
    while True:
        poll_response = make_fetch_request(result_url, headers)

        if poll_response.get("status") == "done":
            transcription = (
                poll_response.get("result", {})
                .get("transcription", {})
                .get("full_transcript")
            )
            if transcription:
                # Format the transcription result with HTML
                result_html = f"""
                <u><b>Transcription Result</b></u>
                <br>
                <pre>{transcription}</pre>
                """
                try:
                    # Attempt to send transcription as a message
                    await message.eor(result_html, parse_mode="html")
                except MessageTooLongError:
                    # Save the large response to a file
                    with open("transcription.txt", "w") as f:
                        f.write(result_html)

                    # Read general details to include in the caption
                    general_details = "Here's the transcription result."

                    # Send the file with a caption
                    await message.client.send_file(
                        message.chat_id,
                        "transcription.txt",
                        caption=f"<u><b>General Details</b></u>:\n{general_details}",
                    )

                    # Clean up by removing the file
                    os.remove("transcription.html")
            else:
                await status_message.edit(
                    "Transcription completed, but no transcript was found."
                )
            break
        else:
            await status_message.edit(
                f"Transcription status: {poll_response.get('status')}"
            )
            time.sleep(30)  # Wait for a few seconds before polling again
