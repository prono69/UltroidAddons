"""
**RANDOM GIRLS IMAGE**

❍ Commands Available -

• `{i}gal <thai, chi, indo, jap, vit, ko, mal>`
    __Random girls pic.__
"""
from random import choice
import requests

zenkey = choice(f"{udB.get_key('ZEN_API')}".split(" "))

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

        
        
@ultroid_cmd(pattern="ngal ?(.*)$")
async def girls(event):
    query = event.pattern_match.group(1).lower()
    base_url = "https://api.ouzen.xyz/api/morensfw/"
    
    # Mapping of queries to API endpoints
    country_map = {
        "asia": "Asian",
        "ar": "Argentina",
        "arab": "Arab",
        "babe": "Babe",
        "beach": "Beach",
        "beau": "Beautiful",
        "bik": "Bikini",
        "boob": "boobs",
        "braz": "Brazilian",
        "blon": "Blonde",
        "bj": "Blowjob",
        "col": "Colombian",
        "chi": "Chinese",
        "cos": "Cosplay",
        "cow": "Cowgirl",
        "curv": "Curvy",
        "cute": "Cute",
        "dress": "Dress",
        "ebo": "Ebony",
        "glass": "Glasses",
        "goth": "Goth",
        "gym": "Gym",
        "home": "Homemade",
        "ind": "Indian",
        "jap": "Japanese",
        "jen": "Jeans",
        "ko": "Korean",
        "lat": "Latina",
        "leg": "Legs",
        "pus": "Pussy",
        "rus": "Russian",
        "red": "Redhead",
        "school": "Schoolgirl",
        "sec": "Secretary",
        "sel": "Selfie",
        "shot": "Shorts",
        "show": "Shower",
        "sk": "Skirt",
        "sto": "Stockings",
        "teach": "Teacher",
        "teen": "Teen",
        "thai": "Thai",
        "tho": "Thong",
        "upsk": "Upskirt",
        "ven": "Venezuela",
        "wife": "Wife",
        "white": "White",
        "yoga": "Yoga",
        
    }
    
    if not query:
        query = choice(list(country_map.keys()))
        
    if query not in country_map:
        return await event.eor("__Invalid query__", time=5)
    
    url = base_url + country_map[query] + f"?apikey={zenkey}"
    kk_ = await event.eor(f"__Getting {country_map[query]}'s girls__")
    
    try:
        res = requests.get(url)
        res.raise_for_status()  # Check if the request was successful (status code 200)

        # Extract the picture URL
        pic = res.json().get("result", "https://http.cat/502")
        
        await event.client.send_file(event.chat_id, pic)
        await kk_.delete()
    
    except requests.exceptions.RequestException:
        await event.client.send_file(event.chat_id, file="https://http.cat/503")
        