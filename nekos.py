from pyUltroid.fns import nsfw as useless
from pyUltroid.fns.misc import unsavegif


@ultroid_cmd(pattern="ne ?(.*)")
async def neko(event):
    "Search images from nekos"
    choose = event.pattern_match.group(1)
    if choose not in useless.nekos():
        return await event.eor(
            f"**Wrong catagory!! Choose from here:**\n\n{useless.nsfw(useless.nekos())}",
            15,
        )
    try:
        catevent = await event.eor("__Processing Nekos...__")
        target = useless.nekos(choose)
        await catevent.delete()
        nohorny = await event.client.send_file(
            event.chat_id,
            file=target,
            caption=f"__{choose}__",
            reply_to=event.reply_to_msg_id,
        )

    except Exception as e:
        await event.eor(f"`{e}`", 5)

    try:
        await unsavegif(event, nohorny)
    except Exception:
        pass
