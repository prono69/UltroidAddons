"""
❍ Commands Available -
 
• `{i}trand <country name>`
    __Get X(Twitter) trends from given country.__
    
"""

from bs4 import BeautifulSoup
import aiohttp
import random

# Function to get a random user agent (optional but recommended)
def get_ua():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    ]
    return random.choice(user_agents)

# Define the function to get trending hashtags
async def get_trendings(country):
    base_url = "https://getdaytrends.com"
    if country:
        url = f"{base_url}/{country}"
    else:
        url = base_url
    headers = {"user-agent": get_ua()}
 
    def get_result(data):
        tags = data.table.find_all("tr")
        results = []
        for tr in tags:
            src = tr.td
            title = src.get_text()
            link = base_url + src.a.get("href")
            results.append({"title": title, "url": link})
        return results
 
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    return {"error": response.reason}
                content = await response.text()
                soup = BeautifulSoup(content, "html.parser")
                tables = soup.select("div[class^='inset']")
                return {
                    "now_hashtags": get_result(tables[0]),
                    "today_hashtags": get_result(tables[1]),
                    "top_hashtags": get_result(tables[2]),
                }
        except Exception as e:
            return {"error": str(e)}



@ultroid_cmd(pattern="trand ?(.*)")
async def trend_command(message):
    country = message.pattern_match.group(1)
    
    await message.eor("**Getting X(Twitter) Trends...**")	
    trends = await get_trendings(country)
    
    if 'error' in trends:
        await message.eor(f"Error: {trends['error']}", 7)
        return
        
    response = (
        f"**Trending Hashtags {country.upper() if country else 'Worldwide'}**\n\n"
    )
    
    response += "**Now Trending:**\n"
    for tag in trends['now_hashtags']:
        response += f"- [{tag['title']}]({tag['url']})\n"

    response += "\n**Today Trending:**\n"
    for tag in trends['today_hashtags']:
        response += f"- [{tag['title']}]({tag['url']})\n"

    response += "\n**Top Hashtags:**\n"
    for tag in trends['top_hashtags']:
        response += f"- [{tag['title']}]({tag['url']})\n"

    await message.eor(response, link_preview=False)

