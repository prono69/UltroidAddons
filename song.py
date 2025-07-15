#    Ultroid - UserBot
#    Copyright 2020 (c)

# Lyrics ported from Dark Cobra
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ Commands Available -

• `{i}lyrics <search query>`
    __Get lyrics of song.__

• `{i}song <search query>`
    __Alternative song command.__

• `{i}llyr <search query>`
    __Get lyrics of song from API.__

• `{i}sspot <search query>`
    __Search songs from Spotify.__

• `{i}aplm <search query>`
    __Search songs from Apple Music.__
"""

import re

import requests
from lyricsgenius import Genius
from pyUltroid.fns.tools import post_to_telegraph
from telethon.errors.rpcerrorlist import (
    MessageTooLongError,
    UserAlreadyParticipantError,
)
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import InputMessagesFilterMusic as filtermus

from . import *

# API URLs
BASE_URL = "https://delirius-apiofc.vercel.app"
URL = f"{BASE_URL}/ia"
NEX_API = udB.get_key("NEX_API")


import requests


async def search_music(api_url, format_function, message, query, params=None):
    await message.eor("__Searching...__")
    url = f"{api_url}{query}"

    if params is None:
        params = {}

    try:
        response = requests.get(url, params=params)
        # Check if the response was successful
        if response.status_code == 200:
            try:
                data = response.json()

                if isinstance(data, list):
                    result = format_function(data)
                elif isinstance(data, dict) and "data" in data:
                    result = format_function(data["data"])
                else:
                    result = "No data found or unexpected format."

                await message.edit(result, parse_mode="md")
            except (ValueError, KeyError, TypeError) as e:
                await message.edit(
                    f"An error occurred while processing the data: {str(e)}"
                )
        else:
            await message.edit(f"API returned an error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        await message.edit(f"Failed to connect to the API: {str(e)}")


def format_lyrics_result(data):
    return f"🎵 **{data['fullTitle']}** by {data['artist']}\n\n__{data['lyrics']}__"


def format_spotify_result(data):
    result = ""
    for item in data[:15]:  # Limit to 15 results
        result += f"🎵 **{item['title']}** by {item['artist']}\n"
        result += f"Album: {item['album']}\n"
        result += f"Duration: {item['duration']}\n"
        result += f"Popularity: {item['popularity']}\n"
        result += f"Publish Date: {item['publish']}\n"
        result += f"[Listen on Spotify]({item['url']})\n\n"
    return result


def format_apple_music_result(data):
    result = ""
    for item in data[:15]:  # Limit to 15 results
        title = item.get("title", "Unknown Title")
        artists = item.get("artists", "Unknown Artist")
        music_type = item.get("type", "Track")
        url = item.get("url", "#")
        result += f"🎵 **{title}** by {artists}\n"
        result += f"Type: {music_type}\n"
        result += f"[Listen on Apple Music]({url})\n\n"
    return result


def format_deezer_result(data):
    result = ""
    for item in data[:15]:  # Limit to 15 results
        result += f"🎵 **{item['title']}** by {item['artist']}\n"
        result += f"Duration: {item['duration']}\n"
        result += f"Rank: {item['rank']}\n"
        result += f"[Listen on Deezer]({item['url']})\n\n"
    return result


@ultroid_cmd(pattern="lyrics ?(.*)$")
async def getlyrics(message):
    query = message.pattern_match.group(1)
    if not query:
        return await message.eor("__Provide a song name to fetch lyrics.__", 5)

    api = udB.get_key("LYRICS_API")
    if not api:
        return await message.eor("__Lyrics API not found.__")

    if "-" in query:
        artist, song = query.split("-")
    else:
        artist, song = "", query

    cat = await message.eor(f"🔎 __Searching 𝖫𝗒𝗋𝗂𝖼s__ `{query}`...")

    genius = Genius(
        api,
        verbose=False,
        remove_section_headers=True,
        skip_non_songs=True,
        excluded_terms=["(Remix)", "(Live)"],
    )

    song = genius.search_song(song, artist)
    if not song:
        return await message.eor("`No results found.`", 5)

    title = song.full_title
    image = song.song_art_image_url
    artist = song.artist
    lyrics = song.lyrics
    lyrics = re.sub(r"(?<!\n)\n(\[)", r"\n\n\1", lyrics)

    outStr = f"<b>{Symbols.anchor} Title:</b> <code>{title}</code>\n<b>{Symbols.anchor} Artist:</b> <code>{artist}</code>\n\n<code>{lyrics}</code>"
    try:
        await cat.edit(outStr, parse_mode="html", link_preview=False)
    except MessageTooLongError:
        content = f"<img src='{image}'/>\n\n{outStr}"
        url = post_to_telegraph(title, content)
        await cat.edit(
            f"**{Symbols.anchor} Title:** `{title}`\n**{Symbols.anchor} Artist:** `{artist}`\n\n**{Symbols.anchor} Lyrics:** [Click Here]({url})",
            link_preview=False,
        )


@ultroid_cmd(pattern="song ?(.*)")
async def _(event):
    ultroid_bot = event.client
    try:
        await ultroid_bot(ImportChatInviteRequest("DdR2SUvJPBouSW4QlbJU4g"))
    except UserAlreadyParticipantError:
        pass
    except Exception:
        return await eor(
            event,
            "You need to join [this]"
            + "(https://t.me/joinchat/DdR2SUvJPBouSW4QlbJU4g)"
            + "group for this module to work.",
        )
    args = event.pattern_match.group(1)
    if not args:
        return await event.eor("`Enter song name`", 5)
    okla = await event.eor("processing...")
    chat = -1001271479322
    current_chat = event.chat_id
    try:
        async for event in ultroid_bot.iter_messages(
            chat, search=args, limit=1, filter=filtermus
        ):
            await ultroid_bot.send_file(current_chat, event, caption=event.message)
        await okla.delete()
    except Exception:
        return await okla.eor("`Song not found.`")


@ultroid_cmd(pattern="llyr ?(.*)$")
async def lyrics_search(message):
    input = message.pattern_match.group(1)
    reply = await message.get_reply_message()
    query = input if input else reply.text
    if not query:
        await message.eor("Usage: lyrics <song name>", 7)
        return
    await search_music(
        f"{BASE_URL}/search/letra?query=", format_lyrics_result, message, query
    )


@ultroid_cmd(pattern="sspot ?(.*)$")
async def spotify_search(message):
    input = message.pattern_match.group(1)
    reply = await message.get_reply_message()
    query = input if input else reply.text
    if not query:
        await message.eor("Usage: spot <query>", 7)
        return
    await search_music(
        f"{BASE_URL}/search/spotify?q=", format_spotify_result, message, query
    )


@ultroid_cmd(pattern="aplm ?(.*)$")
async def applemusic_search(message):
    input = message.pattern_match.group(1)
    reply = await message.get_reply_message()
    query = input if input else reply.text
    if not query:
        await message.eor("Usage: applm <query>", 7)
        return
    await search_music(
        f"{BASE_URL}/search/applemusic?text=", format_apple_music_result, message, query
    )


@ultroid_cmd(pattern="deezer ?(.*)$")
async def deezer_search(message):
    input = message.pattern_match.group(1)
    reply = await message.get_reply_message()
    query = input if input else reply.text
    if not query:
        await message.eor("Usage: applm <query>", 7)
        return
    await search_music(
        f"{BASE_URL}/search/deezer?q=", format_deezer_result, message, query
    )
