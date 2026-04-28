# lastfm.py - Last.fm plugin for Ultroid
# Requires: pylast
# Variables: LASTFM_API_KEY, LASTFM_API_SECRET, LASTFM_USERNAME

from urllib.parse import quote_plus

from pyUltroid.fns.helper import inline_mention
from telethon.utils import get_display_name

from . import get_string, udB, ultroid_cmd


def _get_creds():
    return (
        udB.get_key("LASTFM_API_KEY"),
        udB.get_key("LASTFM_API_SECRET"),
        udB.get_key("LASTFM_USERNAME"),
    )


def _get_network():
    try:
        import pylast
    except ImportError:
        return None, None, "pylast not installed. Run: `pip install pylast`"

    api_key, api_secret, username = _get_creds()
    if not (api_key and api_secret and username):
        return None, None, (
            "❌ **Last.fm not configured!**\n\n"
            "Set these variables:\n"
            "• `LASTFM_API_KEY`\n"
            "• `LASTFM_API_SECRET`\n"
            "• `LASTFM_USERNAME`"
        )

    network = pylast.LastFMNetwork(
        api_key=api_key,
        api_secret=api_secret,
        username=username,
    )
    return network, username, None


@ultroid_cmd(
    pattern="np$",
)
async def now_playing(event):
    """Show currently playing (or last played) track from Last.fm."""
    msg = await event.eor("🎧 **Fetching your current song...**")

    network, username, err = _get_network()
    if err:
        return await msg.edit(err)

    try:
        user = network.get_user(username)
        track = user.get_now_playing()

        if track:
            status = "▶️ **Now Playing**"
        else:
            recent = user.get_recent_tracks(limit=1)
            if not recent:
                return await msg.edit("😶 **No listening history found.**")
            track = recent[0].track
            status = "⏹ **Last Played**"

        title = track.title
        artist = str(track.artist)

        try:
            track_url = track.get_url()
        except Exception:
            track_url = None

        try:
            artist_url = track.artist.get_url()
        except Exception:
            artist_url = None

        try:
            album_obj = track.get_album()
            album = album_obj.title if album_obj else "Unknown"
        except Exception:
            album_obj = None
            album = "Unknown"

        query = quote_plus(f"{title} {artist}")
        spotify_url = f"https://open.spotify.com/search/results/{query}"

        cover_url = None
        try:
            if album_obj:
                cover_url = album_obj.get_cover_image()
        except Exception:
            pass

        track_link = f"[{title}]({track_url})" if track_url else f"**{title}**"
        artist_link = f"[{artist}]({artist_url})" if artist_url else f"**{artist}**"

        caption = (
            f"🎵 **Last.fm Status**\n\n"
            f"{status}\n\n"
            f"**Track:** __{track_link}__\n"
            f"**Artist:** __{artist_link}__\n"
            f"**Album:** `{album}`\n\n"
            f"🎧 [Listen on Spotify]({spotify_url})\n\n"
            f"💿 Powered by Last.fm"
        )

        if cover_url:
            await event.client.send_file(
                event.chat_id,
                cover_url,
                caption=caption,
                reply_to=event.reply_to_msg_id or event.id,
                link_preview=False,
            )
            await msg.delete()
        else:
            await msg.edit(caption, link_preview=False)

    except Exception as e:
        await msg.edit(f"⚠️ **Error:** `{e}`")


@ultroid_cmd(
    pattern="lfm$",
)
async def lastfm_profile(event):
    """Show Last.fm profile stats."""
    msg = await event.eor("🔍 **Fetching Last.fm profile...**")

    network, username, err = _get_network()
    if err:
        return await msg.edit(err)

    try:
        user = network.get_user(username)
        playcount = user.get_playcount()
        profile_url = f"https://www.last.fm/user/{username}"

        avatar_url = None
        try:
            avatar_url = user.get_image()
        except Exception:
            pass

        caption = (
            f"👤 **Last.fm Profile**\n\n"
            f"**User:** `{username}`\n"
            f"**Total Scrobbles:** `{playcount:,}`\n\n"
            f"🔗 [View Profile]({profile_url})"
        )

        if avatar_url:
            await event.client.send_file(
                event.chat_id,
                avatar_url,
                caption=caption,
                reply_to=event.reply_to_msg_id or event.id,
                link_preview=False,
            )
            await msg.delete()
        else:
            await msg.edit(caption, link_preview=False)

    except Exception as e:
        await msg.edit(f"⚠️ **Error:** `{e}`")