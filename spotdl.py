"""
**SPOTIFY DOWNLOADER**

❍ Commands Available -

• `{i}spot <search query or track url>`
    __Donwload Spotify songs.__
"""

import asyncio
import os
import re

import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from telethon.tl.types import DocumentAttributeAudio

client_id = udB.get_key("SPOTIFY_CLIENT_ID")
client_secret = udB.get_key("SPOTIFY_CLIENT_SECRET")

spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
)


async def send_song(e, url, duration, title, performer, eris):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        content_disposition = response.headers.get("content-disposition")
        if content_disposition:
            match = re.search(r'filename="(.+)"', content_disposition)
            if match:
                filename = match.group(1)
                with open(filename, "wb") as file:
                    file.write(response.content)
                attributes = [
                    DocumentAttributeAudio(
                        duration=duration, title=title, performer=performer
                    )
                ]
                await e.client.send_file(
                    e.chat_id,
                    filename,
                    attributes=attributes,
                    caption=title,
                    reply_to=e.reply_to_msg_id,
                )
                os.remove(filename)
                await asyncio.sleep(1)  # Wait for 1 second
                await eris.delete()  # Delete the message indicating song generation
            else:
                await e.reply("`Failed to extract file name from response headers.`")
        else:
            await e.reply("`No content-disposition header found in response.`")
    else:
        await e.reply(f"`Failed to download song. Status code: {response.status_code}`")


async def send_song_link(e, track_name):
    if not track_name:
        return await e.eor("__Give a song name as well vro...__", 5)

    eris = await e.eor(f"___Requesting {track_name}... From Spotify___")

    if track_name.startswith("https://open.spotify.com/track"):
        results = spotify.track(track_name)
        items = results
    else:
        results = spotify.search(q="track:" + track_name, type="track")
        items = results["tracks"]["items"]
    if len(items) > 0:
        track = (
            items
            if track_name.startswith("https://open.spotify.com/track")
            else items[0]
        )
        track_url = track["external_urls"]["spotify"]
        track_id = track_url.split("/")[-1]
        duration = track["duration_ms"] // 1000
        title = track["name"]
        performer = ", ".join([artist["name"] for artist in track["artists"]])

        download_url = f"https://api.spotifydown.com/download/{track_id}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "*/*",
            "Origin": "https://spotifydown.com",
            "Referer": "https://spotifydown.com/",
        }

        response = requests.get(download_url, headers=headers)

        if response.status_code == 200:
            download_data = response.json()
            download_link = download_data["link"]
            await send_song(e, download_link, duration, title, performer, eris)
        else:
            await eris.edit(
                f"`Failed to fetch download URL. Status code: {response.status_code}`"
            )
    else:
        await eris.edit(f"`No tracks found for: {track_name}`")


@ultroid_cmd(pattern="spot(?: |$)(.*)")
async def spot_command(e):
    args = e.pattern_match.group(1)
    if not args and e.is_reply:
        reply = await e.get_reply_message()
        if reply.text:
            args = reply.text.strip()

    await send_song_link(e, args.strip())
