"""
✘ Commands Available -

• `{i}ifsc <reply or query>`
    __Get details of an IFSC code.__
"""

import requests

API_BASE_URL = "https://ifsc.razorpay.com/"


@ultroid_cmd(pattern="ifsc ?(.*)$")
async def fetch_ifsc_details(m):
    try:
        ifsc_code = m.pattern_match.group(1)
        reply = await m.get_reply_message()
        if not ifsc_code and m.is_reply:
            isfc_code = reply.text
        kk_ = await m.edit("`Getting IFSC information...`")
        response = requests.get(f"{API_BASE_URL}{ifsc_code}")
        response.raise_for_status()
        data = response.json()

        if "IFSC" in data:
            details = [
                f"<b>Bank:</b> <code>{data.get('BANK', 'N/A')}</code>",
                f"<b>Bank Code:</b> <code>{data.get('BANKCODE', 'N/A')}</code>",
                f"<b>IFSC:</b> <code>{data.get('IFSC', 'N/A')}</code> | <b>MICR:</b> <code>{data.get('MICR', 'N/A')}</code>",
                f"<b>State:</b> <code>{data.get('STATE', 'N/A')}</code>",
                f"<b>District:</b> <code>{data.get('DISTRICT', 'N/A')}</code>",
                f"<b>City:</b> <code>{data.get('CITY', 'N/A')}</code>",
                f"<b>Branch:</b> <code>{data.get('BRANCH', 'N/A')}</code>",
                f"<b>Address:</b> <code>{data.get('ADDRESS', 'N/A')}</code>",
                f"<b>Contact:</b> <code>{data.get('CONTACT', 'N/A')}</code>",
                f"<b>UPI:</b> <code>{data.get('UPI', 'N/A')}</code> | <b>ISO3166:</b> <code>{data.get('ISO3166', 'N/A')}</code>",
                f"<b>NEFT:</b> <code>{data.get('NEFT', 'N/A')}</code> | <b>IMPS:</b> <code>{data.get('IMPS', 'N/A')}</code>",
                f"<b>RTGS:</b> <code>{data.get('RTGS', 'N/A')}</code> | <b>Swift:</b> <code>{data.get('SWIFT', 'N/A')}</code>",
            ]
            info = "<b>Detailed Info</b>:\n\n" + "\n".join(details)

            await m.eor(info, parse_mode="html")
        else:
            await m.eor("__Invalid IFSC Code 😕 __", 5)
    except requests.exceptions.RequestException:
        await m.eor("Please provide valid IFSC Code", 5)
    except IndexError:
        await m.eor("Please provide an IFSC Code", 5)
