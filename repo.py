"""
✘ Commands Available -

• `{i}rdl <repo url>`
   __Download the whole repo in a zip file.__
"""

import os
import re

import requests


@ultroid_cmd(pattern="rdl ?(.*)$")
async def github_repo(message):
    try:
        repo_input = message.pattern_match.group(1)
        if message.is_reply and not repo_input:
            reply = await message.get_reply_message()
            repo_input = reply.text
        if not repo_input:
            await message.eor(
                f"<b>Usage: </b><code>.repo [link/reply to link]</code>",
                parse_mode="html",
                time=5,
            )
            return
        user, repo = None, None
        match = re.search(
            r"github\.com(?:/|:)([\w.-]+)/([\w.-]+)(?:\.git)?", repo_input
        )
        if match:
            user, repo = match.groups()
        elif "/" in repo_input:
            user, repo = repo_input.split("/")

        if not user or not repo:
            await message.eor(
                "Could not parse the repository reference. Please provide a valid format.",
                5,
            )
            return

        api_url = f"https://api.github.com/repos/{user}/{repo}"
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            repo_details = response.json()
            description = repo_details.get("description", "No description")
            await message.eor(
                f"<b>Downloading Repository....\n\nRepository Name: {repo_details['name']}\nDescription: {description}</b>",
                parse_mode="html",
            )

            default_branch = repo_details.get("default_branch", "main")
        else:
            await message.eor("Failed to fetch repository details", 5)
            return

        download_url = f"https://codeload.github.com/{user}/{repo}/zip/{default_branch}"
        response = requests.get(download_url, headers=headers, allow_redirects=True)

        if response.status_code == 200:
            file_name = f"{repo}-{default_branch}.zip"
            with open(file_name, "wb") as file:
                file.write(response.content)
            await message.client.send_file(
                message.chat_id,
                file_name,
                caption=f"<b>Repository Name:</b> <a href='{repo_input}'>{repo_details['name']}</a>\n\n<b>Description:</b> <blockquote>{description}</blockquote>",
                parse_mode="html",
            )
            await message.delete()
            os.remove(file_name)
        else:
            await message.eor(
                f"Failed to download repository. HTTP Status: {response.status_code}", 5
            )
            return

    except Exception as e:
        await message.eor(
            f"<code>[{getattr(e, 'error_code', '')}: {getattr(e, 'error_details', '')}] - {e}</code>",
            parse_mode="html",
            time=5,
        )
