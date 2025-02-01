"""
❍ Commands Available -

• `{i}saz <reply to an audio file>`
    __Indentify about the replied song.__
"""
import os
from shazamio import Shazam

@ultroid_cmd(pattern="saz$")
async def identify_song(message):
    """Identify a song using Shazam."""
    audio = await message.get_reply_message()
    
    if not audio or not audio.media:
        return await message.eor("🎵 **Please reply to an audio file to identify the song!** 🎧", 5)
    
    processing_message = await message.eor("🎶 **Identifying the song... Hold on!** 🎧")
    audio_path = await audio.download_media()

    try:
        shazam = Shazam()
        result = await shazam.recognize_song(audio_path)
        
        # Parsing the response
        track = result.get("track", {})
        title = track.get("title", "Unknown")
        artist = track.get("subtitle", "Unknown Artist")
        album = next(
            (meta.get("text") for meta in track.get("sections", [])[0].get("metadata", []) if meta.get("title") == "Album"),
            "Unknown Album"
        )
        label = next(
            (meta.get("text") for meta in track.get("sections", [])[0].get("metadata", []) if meta.get("title") == "Label"),
            "Unknown Label"
        )
        release_date = next(
            (meta.get("text") for meta in track.get("sections", [])[0].get("metadata", []) if meta.get("title") == "Released"),
            "Unknown Release Date"
        )
        genre = track.get("genres", {}).get("primary", "Unknown Genre")
        url = track.get("share", {}).get("href", "No URL available")
        cover_art = track.get("images", {}).get("coverarthq", None)

        # Constructing the response message
        song_info = (
            f"🎵 **Song Identified:**\n"
            f"**🎤 Title:** `{title}`\n"
            f"**🎼 Artist:** `{artist}`\n"
            f"**💿 Album:** `{album}`\n"
            f"**🏷️ Label:** `{label}`\n"
            f"**📅 Released:** `{release_date}`\n"
            f"**🎙️ Genre:** `{genre}`\n"
            f"**🔗 Listen Here:** [Click Here]({url})"
        )

        # Sending the response with cover art if available
        if cover_art:
            await message.client.send_file(
                message.chat_id,
                cover_art,
                caption=song_info,
                reply_to =message.reply_to_msg_id
            )
            await processing_message.delete()
        else:
            await processing_message.edit(song_info)

    except Exception as e:
        await message.eor(f"❌ **An error occurred:** `{e}`", 5)

    finally:
        # Cleanup
        if os.path.exists(audio_path):
            os.remove(audio_path)