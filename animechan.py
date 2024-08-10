# Ultroid - UserBot
#
# This file is a part of < https://github.com/TeamUltroid/UltroidAddons/>

"""
Fetch Random anime quotes

Command : `{i}aniq`
"""

from . import ultroid_cmd, async_searcher, udB


@ultroid_cmd(pattern="aniq")
async def _(ult):
    u = await ult.eor("...")
    getkey = udB.get_key("ANIQUOTE_TOKEN")
    if not getkey:
    	await eod(ult, "set ANIQUOTE_TOKEN first")
    	return
    try:
        headers={
            "Authorization": f"{getkey}",
        }
        resp = await async_searcher(
            "https://waifu.it/api/v4/quote", headers=headers, re_json=True
        )
        results = f"**{resp['quote']}**\n"
        results += f" — __{resp['author']} ({resp['anime']})__"
        return await u.edit(results)
    except Exception as e:
        await u.edit(f"Error:\n`{e}`")
