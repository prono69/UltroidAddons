import os
from datetime import datetime

import google.generativeai as genai

from . import udB

# Configure generative AI with a API key
gemini_key = udB.get_key("GEMINI_KEY")
genai.configure(api_key=f"{gemini_key}")

# Available models
available_models = [
    "models/gemini-1.5-flash",
    "models/gemini-1.5-flash-latest",
    "models/gemini-1.0",
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-latest",
]
current_model_name = available_models[0]
model = genai.GenerativeModel(current_model_name)

# History dictionary to store user conversations
conversation_history = {}


@ultroid_cmd(pattern="bur ?(.*)")
async def gemini_handler(event):
    global conversation_history, model, current_model_name

    # Notify user that the bot is processing the query
    processing_message = await event.eor("⏳ **Processing...**")

    # Extract the command and query
    query = event.pattern_match.group(1)

    # Command: Clear history
    if query == "-c":
        conversation_history.clear()
        await processing_message.edit("🔄 **Conversation history cleared!**")
        return

    # Command: List available models
    if query == "-ls":
        models_list = "\n".join(f"🔹 {m}" for m in available_models)
        await processing_message.edit(
            f"📜 **Available Models:**\n`{models_list}`\n\n**Current Model:** `{current_model_name}`"
        )
        return

    # Command: Switch model
    if query.startswith("-m"):
        new_model_name = query.split("-m", maxsplit=1)[-1].strip()
        if new_model_name in available_models:
            current_model_name = new_model_name
            model = genai.GenerativeModel(current_model_name)
            await processing_message.edit(
                f"✅ **Model switched to:** {current_model_name}"
            )
        else:
            await processing_message.edit(
                "⚠️ **Invalid model name! Use `.gemini -ls` to view available models.**"
            )
        return

    # Handle reply to text or files
    replied_msg = await event.get_reply_message()
    gemini_input = []

    if replied_msg:
        # If replying to a text message
        if replied_msg.text:
            gemini_input.append(replied_msg.text)
        # If replying to a file
        elif replied_msg.file:
            try:
                file_path = await replied_msg.download_media()
                gemini_file = genai.upload_file(
                    path=file_path, display_name=replied_msg.file.name
                )
                gemini_input.append(gemini_file)
            except Exception as e:
                await processing_message.edit(f"⚠️ **Error processing file:** `{e}`")
                return
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)

    if query:
        gemini_input.insert(0, query)  # Add the user's query at the beginning

    # Add conversation history for context
    if conversation_history:
        gemini_input = list(conversation_history.values()) + gemini_input

    try:
        # Show typing action while generating response
        async with event.client.action(event.chat_id, "typing"):
            # Generate response from Gemini
            response = model.generate_content(gemini_input)

            # Store the current query and response in history
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conversation_history[timestamp] = (
                f"Q: {query or '(File Uploaded)'} | A: {response.text}"
            )

            await processing_message.edit(
                f"🤖 **Gemini's Reply:**\n__{response.text}__"
            )

    except Exception as e:
        await processing_message.edit(f"⚠️ **An error occurred:** {e}")
