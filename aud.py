"""
✘ Commands Available -

• `{i}voice <reply or query>`
    __Convert text to speech with api.__
"""

import os

import requests

from . import ultroid_cmd

url = "https://ios-app.heypi.com/api/chat"
headers = {
    "Host": "ios-app.heypi.com",
    "x-api-version": "3",
    "accept": "text/event-stream",
    "user-agent": "Pi/1.5 (Android 7.1.2; Xiaomi; Redmi Note 7 Pro)",
    "sentry-trace": "",
    "baggage": "",
    "content-type": "application/json; charset=utf-8",
    "accept-encoding": "gzip",
    "cookie": "__cf_bm=ExQK1sZT9M_Sjt9I0OVRaSikmJCV03oWPOLpHARgOBA-1724570764-1.0.1.1-NyDZQZtLD3ZDF9T6EnKgYn87A0NLkbBAAVDPMsWQgEYLXXPsBm0dEZXEDz29NFxD82pccbOcQ_VsskiLO3H8gA; __Host-session=yiS8uBDdUYcaf1V1158V1",
}


@ultroid_cmd(pattern="voice(?: |$)(.*)")
async def tts_bot(event):
    text_to_speech = event.pattern_match.group(1)

    if not text_to_speech and event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        text_to_speech = reply_message.message

    if not text_to_speech:
        await event.eor("`Please provide some text or reply to a message.`", 5)
        return

    # No longer editing any messages
    response_message = await event.eor("`Processing your request...`")

    data = {"text": text_to_speech}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            json_response = response.text.splitlines()
            sid_value = None
            for line in json_response:
                if "sid" in line:
                    sid_value = line.split('"sid":"')[1].split('"')[0]
                    break

            if sid_value:
                voice_url = "https://ios-app.heypi.com/api/chat/voice"
                voice_params = {
                    "messageSid": sid_value,
                    "voice": udB.get_key(
                        "voice"
                    ),  # Default to voice4 or replace with desired value
                    "duplex": "false",
                    "mode": "eager",
                }
                voice_headers = {
                    "Cookie": "__Host-session=yiS8uBDdUYcaf1V1158V1",
                    "Icy-MetaData": "1",
                    "Accept-Encoding": "identity",
                    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; Redmi Note 7 Pro Build/N6F26Q)",
                    "Host": "ios-app.heypi.com",
                    "Connection": "Keep-Alive",
                }

                voice_response = requests.get(
                    voice_url, headers=voice_headers, params=voice_params
                )

                if voice_response.status_code == 200:
                    audio_content = voice_response.content

                    file_name = f"downloads/{event.chat_id}_{event.id}.ogg"
                    os.makedirs("downloads", exist_ok=True)
                    with open(file_name, "wb") as f:
                        f.write(audio_content)

                    await event.client.send_file(
                        event.chat_id,
                        file_name,
                        voice_note=True,
                        reply_to=event.reply_to_msg_id or event.id,
                    )

                    os.remove(file_name)
                    await response_message.delete()
                else:
                    await response_message.edit(
                        "`Error: Failed to generate audio file.`"
                    )
            else:
                await response_message.edit(
                    "`Error: 'sid' value not found in the response.`"
                )
        else:
            await response_message.edit(
                "`Error: Failed to get response from the first request.`"
            )
    except Exception as e:
        await response_message.edit(f"An error occurred: `{str(e)}`")
