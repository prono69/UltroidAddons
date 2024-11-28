import logging
import os

import requests

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Define the API URLs
VIDEO_API_URL = "https://deliriussapi-oficial.vercel.app/anime/hentaivid"

# Use a writable temporary directory
TEMP_DIR = "/tmp/telegram_videos"

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


async def fetch_videos():
    try:
        response = requests.get(VIDEO_API_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors
        videos = response.json()
        logging.debug(f"Fetched videos: {videos}")
        return videos
    except requests.RequestException as e:
        logging.error(f"Error fetching videos: {e}")
        return []


async def get_videos(number_of_videos):
    videos = await fetch_videos()
    if videos:
        logging.debug(f"Selected videos: {videos[:number_of_videos]}")
        return videos[:number_of_videos]
    return []


async def save_video_to_temp(video_url):
    try:
        response = requests.get(video_url)
        response.raise_for_status()

        video_data = response.content
        video_file_name = os.path.join(TEMP_DIR, "video.mp4")

        with open(video_file_name, "wb") as f:
            f.write(video_data)

        return video_file_name
    except requests.RequestException as e:
        logging.error(f"Error saving video: {e}")
        return None


async def delete_temp_video(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.debug(f"Deleted video file: {file_path}")
    except OSError as e:
        logging.error(f"Error deleting video file: {e}")


@ultroid_cmd(pattern="dhen")
async def fetch_and_upload_videos(message):
    command_args = message.text.split(maxsplit=1)
    if len(command_args) > 1:
        try:
            number_of_videos = int(command_args[1])
        except ValueError:
            await message.eor("Invalid number of videos specified.", 5)
            return
    else:
        number_of_videos = 1

    await message.edit("`Processing...`")

    videos = await get_videos(number_of_videos)
    if videos:
        for video in videos:
            video_url = video.get("video_1")

            if video_url:
                video_file_path = await save_video_to_temp(video_url)

                if video_file_path:
                    try:
                        await message.client.send_file(
                            message.chat_id,
                            file=video_file_path,
                            parse_mode="html",
                            reply_to=message.reply_to_msg_id,
                        )

                        await delete_temp_video(video_file_path)
                    except requests.RequestException as e:
                        await message.eor(f"Error sending video: {e}", 5)
    else:
        await message.eor("No videos available.", 5)

    await message.delete()
