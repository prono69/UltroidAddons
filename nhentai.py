"""
✘ Commands Available -

• `{i}nhen <reply or horny code>`
    __Get details of Doujin from nhentai.__
"""

from telethon.errors import BotResponseTimeoutError

TARGET_BOT = '@nPDFBot'

@ultroid_cmd(pattern="nhen ?(.*)$")
async def pdfbot_handler(event):
    query = event.pattern_match.group(1).strip()
    if not query and event.is_reply:
    	reply = await event.get_reply_message()
    	query = reply.text

    if not query:
        return await event.eor("`Give a code to search the Doujin, Pervert!`", 5)

    try:
        # Start a conversation with the bot
        async with event.client.conversation(TARGET_BOT) as conv:
            kk = await event.eor(f"__Sending {query}...__")
            # Send query to the bot
            await conv.send_message(query)
            await event.client.send_read_acknowledge(conv.chat_id)
            
            response = await conv.get_response(timeout=10)
            cap = f"{response.text}\n**Link:** __https://nhentai.net/g/{query}__"
            if response.media:
            	await event.client.send_file(event.chat_id, response.media, caption=cap, reply_to=event.reply_to_msg_id)
            	await kk.delete()
            else:
            	await event.eor(cap)
            await event.client.send_read_acknowledge(conv.chat_id)
            
            
    
    except BotResponseTimeoutError:
        await event.eor("`Took too long to respond. Please try again later.`", 5)
    except Exception as e:
        await event.eor(f"__An error occurred:__\n>> `{str(e)}`", 5)

        