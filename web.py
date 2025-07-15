"""
web -- reply or type
"""

import re
from io import BytesIO

import aiohttp

from . import LOGS, get_string, ultroid_cmd


def html2md(text):
    pattern = r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)<\/a>'
    replacement = r"[\2](\1)"
    markdown_text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return markdown_text


async def fetch_data_from_api(question):
    url = "https://app-paal-chat-1003522928061.us-east1.run.app/api/chat/web"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {"prompt": question, "bid": "040d0481"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("answer")
            else:
                LOGS.warning(f"Failed to fetch data: {response.status}")
                return None


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

    try:
        response = await fetch_data_from_api(question)
        if not response:
            return await moi.edit("Failed to fetch the answer.")
    except Exception as exc:
        LOGS.warning(f"Error fetching data: {exc}", exc_info=True)
        return await moi.edit(f"Error: {exc}")

    response_markdown = html2md(response)
    out = f"**Query:**\n\n~ __{question}__\n\n**Answer:** \n__{response_markdown}__"

    if len(out) > 4096:
        with BytesIO(out.encode()) as outf:
            outf.name = "answer.txt"
            await e.respond(
                f"`{response_markdown}`", file=outf, reply_to=e.reply_to_msg_id
            )
        await moi.delete()
    else:
        await moi.edit(out)
