import requests
from pyUltroid import udB

from . import run_async

cfac = udB.get_key("CFAC")
cfkey = udB.get_key("CFKEY")
cfm = udB.get_key("CFM")
API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{cfac}/ai/run/"
headers = {"Authorization": f"Bearer {cfkey}"}


@run_async
def run(model, inputs):
    input = {"messages": inputs}
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    resp = response.json()
    return resp["result"]["response"]


@ultroid_cmd(pattern="cfai ?(.*)")
async def cfai(e):
    query = e.pattern_match.group(1)
    if not query:
        return await e.eor("`Please provide a query to the command.`", 5)

    await e.eor("`Generating answer...`")

    inputs = [
        {
            "role": "system",
            "content": """You are a OpenAI New model o1. 
                        The OpenAI O1 model is an advanced AI language model capable of understanding and generating natural language text. 
                        It excels in tasks such as summarization, translation, content creation, and answering complex questions. 
                        With its ability to grasp context and nuances, O1 is widely used in various fields, including customer support, 
                        education, and research, providing valuable insights and enhancing productivity.""",
        },
        {"role": "user", "content": query},
    ]
    response = await run(f"{cfm}", inputs)

    if len(response) < 4095:
        return await e.eor(response)
    else:
        return await e.eor("Response too long. Please try a smaller query.")
