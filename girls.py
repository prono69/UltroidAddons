"""
**RANDOM GIRLS IMAGE**

❍ Commands Available -

• `{i}gal <thai, chi, indo, jap, vit, ko, mal>`
    __Random girls pic.__
"""
from random import choice
import requests

@ultroid_cmd(pattern="gal ?(.*)$")
async def girls(event):
    query = event.pattern_match.group(1).lower()
    base_url = "https://api.agatz.xyz/api/"
    
    # Mapping of queries to API endpoints
    country_map = {
        "chi": "china",
        "indo": "indonesia",
        "jap": "Japan",
        "vit": "vietnam",
        "ko": "korea",
        "mal": "malaysia",
        "thai": "thailand"
    }
    
    if not query:
        query = choice(list(country_map.keys()))
        
    if query not in country_map:
        return await event.eor("__Invalid query__", time=5)
    
    url = base_url + country_map[query]
    kk_ = await event.eor(f"__Getting {country_map[query]}'s girls__")
    
    try:
        res = requests.get(url)
        res.raise_for_status()  # Check if the request was successful (status code 200)

        # Extract the picture URL
        pic = res.json().get("data", {}).get("url", "https://http.cat/502")
        
        await event.client.send_file(event.chat_id, pic)
        await kk_.delete()
    
    except requests.exceptions.RequestException:
        await event.client.send_file(event.chat_id, file="https://http.cat/503")
