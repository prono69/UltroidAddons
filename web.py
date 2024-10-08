"""
web -- reply or type
"""

from io import BytesIO

import aiohttp

from . import LOGS, check_filename, get_string, run_async, udB, ultroid_cmd


async def fetch_data_from_api(question):
    url = "https://bot-management-4tozrh7z2a-ue.a.run.app/chat/web"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {"prompt": question, "bid": "040d0481"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            data = await response.json()
            return data.get("answer")


@ultroid_cmd(pattern="web ?(.*)")
async def ask_bot(e):
    moi = await e.eor(get_string("com_1"))
    reply = await e.get_reply_message()
    question = e.pattern_match.group(1)

    if not question:
        if reply and reply.text:
            question = reply.message
    if not question:
        return await moi.eor("`Please provide a question to ask the bot.`")

    # moi = await b.eor(f"**Question ✅**\n\n`{question}`\n\n`Answer❌❌ `\n""Fetching the answer...")
    try:
        response = await fetch_data_from_api(question)
        if not response:
            return await moi.edit("Failed to fetch the answer.")
    except Exception as exc:
        LOGS.warning(exc, exc_info=True)
        return await moi.edit(f"Error: {exc}")

    out = f"Question ✅\n\n{question}\n\nAnswer 👇`\n{response}"
    if len(out) > 4096:
        out = f"Question ✅\n\n{question}\n\nAnswer 👇`\n{response}"
        with BytesIO(out.encode()) as outf:
            outf.name = "answer.txt"
            await e.respond(f"`{response}`", file=outf, reply_to=e.reply_to_msg_id)
        await moi.delete()
    else:
        out = f"<b>Question</b> ✅\n\n<code>{question}</code>\n\n<b>Answer</b> 👇\n{response}"
        await moi.edit(out, parse_mode="html")
