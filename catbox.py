# Catbox Uploader Made by @NeoMatrix90
"""
❍ Commands Available -
 
• `{i}catb <reply to media>`
    Upload image to catbox or envs
    
"""

import os
import requests
from . import ultroid_cmd, udB
from pyUltroid.fns.misc import CatboxUploader

userhash = udB.get_key("CATBOX") if udB.get_key("CATBOX") else ""
uploader = CatboxUploader(userhash)

def upload_to_envs(file_path):
    url = 'https://envs.sh'
    with open(file_path, 'rb') as f:
        files = {
            'file': f
        }
        response = requests.post(url, files=files)
        if response.status_code == 200:
            response_text = response.text
            url_ = response_text.split(' ')[-1]
            return url_
        else:
            return f"Error: {response.status_code} - {response.text}"
            

def upload_to_qu(file_path, url="https://qu.ax/upload.php"):
    files = {'files[]': open(file_path, 'rb')}
    response = requests.post(url, files=files)
    
    # Check if the response is in JSON format
    try:
        response_json = response.json()
        file_url = response_json.get('files', [{}])[0].get('url', 'URL not found')
        return file_url
    except ValueError:
        print("Response is not in JSON format")

    return None

            
@ultroid_cmd(pattern="catb ?(.*)$")
async def handler(event):
    reply = await event.get_reply_message()
    flag = event.pattern_match.group(1)
    if event.is_reply and reply.media:
        kk = await event.eor("`Uploading...`")
        file_path = await reply.download_media()
        
        if flag == "e":
            upload_link = upload_to_envs(file_path)
            server = "Envs"
        elif flag == "q":
        	upload_link = upload_to_qu(file_path)
        	server = "Qu"
        else:
            upload_link = uploader.upload_file(file_path)
            server = "Catbox"
        
        if upload_link and not upload_link.startswith("Error"):
            await kk.edit(f"✘ **File Uploaded to {server}!** \n>> __{upload_link}__")
        else:
            await kk.edit(f"__Failed to upload the file: {upload_link}__")
        
        os.remove(file_path)  # Clean up
    else:
        await event.eor("__Please send a file along with the command.__", 5)
