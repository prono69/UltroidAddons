# joke.py
# Ultroid plugin to get jokes using JokeAPI with shorthand categories
# Author: @NEOMATRIX90

import asyncio
from jokeapi import Jokes

CATEGORY_ALIASES = {
    "pro": "Programming",
    "d": "Dark",
    "m": "Misc",
    "p": "Pun",
    "s": "Spooky",
    "c": "Christmas",
    "a": "Any"
}

@ultroid_cmd(pattern="jk(?:\s+(\d+)?(?:\s+(.*))?)?")
async def _joke(event):
    await event.eor("🔍 __Fetching jokes...__")

    # Default values
    count = 1
    categories = ["Any"]

    args = event.pattern_match.group(1)
    extra_cats = event.pattern_match.group(2)

    if args:
        try:
            count = min(int(args), 10)  # Cap to 10
        except:
            pass

    if extra_cats:
        raw_cats = extra_cats.split()
        categories = []
        for cat in raw_cats:
            cat_lower = cat.lower()
            mapped = CATEGORY_ALIASES.get(cat_lower, cat.capitalize())
            if mapped not in categories:
                categories.append(mapped)

    try:
        j = await Jokes()
        data = await j.get_joke(category=categories, amount=count, joke_type='single')

        if data.get("error"):
            return await event.eor("❌ Failed to fetch jokes. Try different categories or count.", 7)

        # Normalize single joke vs multiple
        if "jokes" in data:
            jokes = data["jokes"]
        else:
            jokes = [data]

        if not jokes:
            return await event.eor("😢 **No jokes found.**", 7)

        text = ""
        for i, joke in enumerate(jokes, 1):
            text += f"**{i}. ({joke['category']})**\n__{joke['joke']}__\n\n"

        await event.eor(text.strip())

    except Exception as e:
        await event.eor(f"❌ Error:\n`{e}`")
