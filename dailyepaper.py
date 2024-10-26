"""
✘ Commands Available -

• `{i}epaper`
    __Get daily news paper (english only).__
"""

import datetime
import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup as bs


now = datetime.datetime.now()
current_month = now.strftime("%b").lower()
current_year = now.year

WEBSITE = [
    "https://www.dailyepaper.in/the-tribune-epaper/",
    f"https://www.dailyepaper.in/economic-times-newspaper-{current_year}/",
    f"https://www.dailyepaper.in/times-of-india-epaper-pdf-{current_month}-{current_year}/#google_vignette",
    "https://www.dailyepaper.in/financial-express-newspaper/",
    "https://www.dailyepaper.in/telegraph-newspaper/",
    "https://www.dailyepaper.in/statesman-newspaper-today/",
]


async def scrape_data(msg):
    errors = ""
    text = ""
    async with aiohttp.ClientSession() as session:
        for url in WEBSITE:
            try:
                data = await session.get(url)
                soup = bs(await data.text(), "html.parser")
                title = soup.find("title").text
                # remove "in PDF download today | DailyEpaper.in" from title
                phrases_to_replace = [
                    "in PDF download today | DailyEpaper.in",
                    "in PDF Free Download Today | DailyEpaper.in",
                    "PDF Free Download Today | DailyEpaper.in",
                    "PDF Free Download | DailyEpaper.in",
                ]
                for phrase in phrases_to_replace:
                    title = title.replace(phrase, "").strip()
                title = title.replace("Today in", "Today").strip()
                title = re.sub(r"\s+", " ", title)
                source = soup.findAll("a", {"target": "_blank", "rel": "noopener"})
                drive_links = [
                    a["href"]
                    for a in source
                    if a["href"].startswith("https://drive.google.com/")
                ]

                if title and drive_links:
                    await msg.eor(
                        f"✅ Scraping from <b>{title}</b> was successful.", parse_mode="html"
                    )
                    text += f"<b>{title}</b> - {drive_links[0]}\n"

            except Exception as e:
                await msg.eor(f"❌ Scraping from <b>{url}</b> was unsuccessful.", parse_mode="html")
                errors += f"{url}: {repr(e)}\n\n"
            await asyncio.sleep(5)
    return text, errors


@ultroid_cmd(pattern="epaper$")
async def scrape_command(message):
    await message.eor("🔄 Starting to scrape data...")
    text, errors = await scrape_data(message)
    if text:
        await message.eor(f"✅ Scraping complete:\n\n{text}", parse_mode="html")
    if errors:
        await message.eor(f"⚠️ Errors encountered:\n\n{errors}", parse_mode="html")
