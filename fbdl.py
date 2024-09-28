import requests
import os

@ultroid_cmd(pattern="fbdl ?(.*)$")
async def fb_dl(event):
    # Extract the Facebook video URL from the user's input
    query = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not query and event.is_reply:
    	query = reply.text
    
    if not query:
        return await event.eor("__Please provide a valid Facebook video URL__", 5)

    url = "https://fbdown.online/wp-json/aio-dl/video-data/"

    headers = {
        "Connection": "keep-alive",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-platform": "Android",
        "sec-ch-ua-mobile": "?1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36",
        "content-type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Origin": "https://fbdown.online",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://fbdown.online/",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    data = {
        "url": query,
        "token": "36d935ff24a0c15593d056afa4dd8c067084ba2f2f950dc81d5de85aad6f1d33"
    }
    
    kk = await event.eor("__Fetching video...__")

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Check if the request was successful

        result = response.json()

        # Extract the video URL and thumbnail
        video_url = result.get("medias", [])[0].get("url")
        # thumbnail_url = result.get("thumbnail", "")
        
        if not video_url:
            return await kk.edit("__Failed to retrieve video. Please check the URL or try again later.__")
            
        video_response = requests.get(video_url)
        filename = "fb_video.mp4"
        with open(filename, 'wb') as f:
            f.write(video_response.content)
            
        await event.client.send_file(event.chat_id, file=filename)

        # Clean up the local video file
        os.remove(filename)
        await kk.delete()

    except requests.exceptions.RequestException as e:
        # Handle any request-related errors
        await kk.edit(f"Failed to fetch video: `{str(e)}`")

    except Exception as e:
        # Handle any other errors
        await kk.edit(f"An error occurred: `{str(e)}`")
        