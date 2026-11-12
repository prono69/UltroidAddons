"""
Dump Copier Plugin for Ultroid
Automatically copies leech bot's file uploads to a dump chat
"""

from telethon.events import NewMessage
from telethon.tl.types import MessageMediaDocument, MessageMediaVideo, MessageMediaPhoto, MessageMediaAudio
import logging

from ultroid import ultroid_cmd, eod, LOGS, ultroid_bot

logger = logging.getLogger(__name__)

# Configuration - can be set via plugin env vars
LEECH_BOT_ID = None
LEECH_DUMP_CHAT = None
MONITOR_CHATS = None  # None = all chats, or list of chat IDs
MONITORING_ENABLED = False


def has_media(message) -> bool:
    """Check if message has media attachment"""
    if not message.media:
        return False
    
    media_types = (
        MessageMediaDocument,
        MessageMediaVideo,
        MessageMediaPhoto,
        MessageMediaAudio,
    )
    return isinstance(message.media, media_types)


@ultroid_cmd(pattern="dump start", fullsudo=False)
async def dump_start(event):
    """Start monitoring leech bot and copying files to dump chat"""
    global LEECH_BOT_ID, LEECH_DUMP_CHAT, MONITOR_CHATS, MONITORING_ENABLED
    
    try:
        # Get config from command or use defaults
        # Usage: dump start <leech_bot_id> <dump_chat_id> [monitor_chat1,monitor_chat2]
        
        args = event.text.split()
        
        if len(args) < 3:
            return await eod(
                event,
                "❌ **Usage:** `dump start <leech_bot_id> <dump_chat_id> [monitor_chats]`\n\n"
                "**Example:**\n"
                "`dump start 1234567890 -1001234567890`\n"
                "`dump start 1234567890 -1001234567890 -1001111111111,-1002222222222`",
                parse_mode="md"
            )
        
        try:
            LEECH_BOT_ID = int(args[1])
            LEECH_DUMP_CHAT = int(args[2])
        except ValueError:
            return await event.eod("❌ Invalid bot ID or chat ID. Must be numbers.", parse_mode="md")
        
        # Parse monitor chats if provided
        if len(args) > 3:
            try:
                MONITOR_CHATS = [int(chat) for chat in args[3].split(",")]
            except ValueError:
                return await event.eod("❌ Invalid monitor chat IDs.", parse_mode="md")
        else:
            MONITOR_CHATS = None
        
        MONITORING_ENABLED = True
        
        monitoring_text = f"All chats" if MONITOR_CHATS is None else f"Chats: {MONITOR_CHATS}"
        
        await eod(
            event,
            f"✅ **Dump Copier Started**\n"
            f"🤖 Leech Bot ID: `{LEECH_BOT_ID}`\n"
            f"📂 Dump Chat: `{LEECH_DUMP_CHAT}`\n"
            f"🎯 Monitoring: {monitoring_text}",
            parse_mode="md"
        )
        
        LOGS.info(
            f"Dump Copier Started - Bot: {LEECH_BOT_ID}, "
            f"Dump: {LEECH_DUMP_CHAT}, Monitor: {monitoring_text}"
        )
        
    except Exception as e:
        await eod(event, f"❌ Error: {str(e)}", parse_mode="md")
        LOGS.error(f"Dump copier start error: {e}")


@ultroid_cmd(pattern="dump stop", fullsudo=False)
async def dump_stop(event):
    """Stop monitoring and copying files"""
    global MONITORING_ENABLED
    
    if not MONITORING_ENABLED:
        return await eod(event, "❌ Dump copier is not running.", parse_mode="md")
    
    MONITORING_ENABLED = False
    
    await eod(event, "✅ Dump copier stopped.", parse_mode="md")
    LOGS.info("Dump copier stopped")


@ultroid_cmd(pattern="dump status", fullsudo=False)
async def dump_status(event):
    """Check dump copier status"""
    global MONITORING_ENABLED, LEECH_BOT_ID, LEECH_DUMP_CHAT, MONITOR_CHATS
    
    if not MONITORING_ENABLED:
        status_text = "❌ **Status:** Stopped"
    else:
        monitoring_text = f"All chats" if MONITOR_CHATS is None else f"Chats: {MONITOR_CHATS}"
        status_text = (
            f"✅ **Status:** Running\n"
            f"🤖 Leech Bot ID: `{LEECH_BOT_ID}`\n"
            f"📂 Dump Chat: `{LEECH_DUMP_CHAT}`\n"
            f"🎯 Monitoring: {monitoring_text}"
        )
    
    await eod(event, status_text, parse_mode="md")


@ultroid_cmd(pattern="dump reset", fullsudo=False)
async def dump_reset(event):
    """Reset dump copier configuration"""
    global LEECH_BOT_ID, LEECH_DUMP_CHAT, MONITOR_CHATS, MONITORING_ENABLED
    
    LEECH_BOT_ID = None
    LEECH_DUMP_CHAT = None
    MONITOR_CHATS = None
    MONITORING_ENABLED = False
    
    await eod(event, "✅ Dump copier configuration reset.", parse_mode="md")
    LOGS.info("Dump copier reset")


@ultroid_bot.on(NewMessage())
async def handle_message(event):
    """Monitor messages and copy media from leech bot to dump chat"""
    global MONITORING_ENABLED, LEECH_BOT_ID, LEECH_DUMP_CHAT, MONITOR_CHATS
    
    # Check if monitoring is enabled
    if not MONITORING_ENABLED or not LEECH_BOT_ID or not LEECH_DUMP_CHAT:
        return
    
    try:
        # Skip if message is in DM or from a channel
        if event.is_private or event.is_channel:
            return
        
        # Check if message is from the leech bot
        if event.sender_id != LEECH_BOT_ID:
            return
        
        # Check if we're monitoring this chat
        if MONITOR_CHATS and event.chat_id not in MONITOR_CHATS:
            return
        
        # Skip if message is already in the dump chat
        if event.chat_id == LEECH_DUMP_CHAT:
            return
        
        # Check if message has media
        if not has_media(event.message):
            return
        
        # Copy message to dump chat
        try:
            await event.client.send_message(
                entity=LEECH_DUMP_CHAT,
                message=event.message
            )
            
            media_type = type(event.message.media).__name__.replace("MessageMedia", "").lower()
            logger.info(
                f"✓ Copied {media_type} from {event.chat_id} to dump chat {LEECH_DUMP_CHAT}"
            )
            
        except Exception as copy_error:
            logger.error(f"Failed to copy message to dump chat: {copy_error}")
            
    except Exception as e:
        logger.error(f"Dump copier handler error: {e}")
