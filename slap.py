# Ultroid - UserBot
# Copyright (C) 2023-2024 @TeamUltroid
#
# This file is a part of < https://github.com/ufoptg/UltroidAddons/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/ufoptg/UltroidBackup/blob/main/LICENSE/>.
# By @TrueSaiyan for Ultroid

"""
❍ Commands Available

• `{i}slap`
    reply to a user to slap them

• `{i}hug`
    reply to a user to hug them

• `{i}pat`
    reply to a user to pat them

"""

import html
import random

from telethon.utils import get_display_name

from pyUltroid.fns.helper import extract_user

from . import *

SLAP_TEMPLATES = (
    "{user2} was killed by magic.",
    "{user2} starved without pats.",
    "{user2} was knocked into the void by {user1}.",
    "{user2} fainted.",
    "{user2} is out of usable Pokemon! {user2} whited out!.",
    "{user2} is out of usable Pokemon! {user2} blacked out!.",
    "{user2} got rekt.",
    "{user2}'s melon was split by {user1}.",
    "{user2} was sliced and diced by {user1}.",
    "{user2} played hot-potato with a grenade.",
    "{user2} was knifed by {user1}.",
    "{user2} ate a grenade.",
    "{user2} is what's for dinner!",
    "{user2} was terminated by {user1}.",
    "{user1} spammed {user2}'s email.",
    "{user1} RSA-encrypted {user2} and deleted the private key.",
    "{user1} put {user2} in the friendzone.",
    "{user1} slaps {user2} with a DMCA takedown request!",
    "{user2} got a house call from Doctor {user1}.",
    "{user1} beheaded {user2}.",
    "{user2} got stoned...by an angry mob.",
    "{user1} sued the pants off {user2}.",
    "{user2} was one-hit KO'd by {user1}.",
    "{user1} sent {user2} down the memory hole.",
    "{user2} was a mistake. - '{user1}' ",
    "{user2} was made redundant.",
    "{user1} {hits} {user2} with a bat!.",
    "{user1} {hits} {user2} with a Taijutsu Kick!.",
    "{user1} {hits} {user2} with X-Gloves!.",
    "{user1} {hits} {user2} with a Jet Punch!.",
    "{user1} {hits} {user2} with a Jet Pistol!.",
    "{user1} {hits} {user2} with a United States of Smash!.",
    "{user1} {hits} {user2} with a Detroit Smash!.",
    "{user1} {hits} {user2} with a Texas Smash!.",
    "{user1} {hits} {user2} with a California Smash!.",
    "{user1} {hits} {user2} with a New Hampshire Smash!.",
    "{user1} {hits} {user2} with a Missouri Smash!.",
    "{user1} {hits} {user2} with a Carolina Smash!.",
    "{user1} {hits} {user2} with a King Kong Gun!.",
    "{user1} {hits} {user2} with a baseball bat - metal one.!.",
    "{user1} Serious punches {user2}*.",
    "{user1} Normal punches {user2}*.",
    "{user1} Consecutive Normal punches {user2}*.",
    "{user1} Two Handed Consecutive Normal Punches {user2}*.",
    "{user1} Ignores {user2} to let them die of embarassment*.",
    "{user1} points at {user2}* What's with this sassy... lost child?.",
    "{user1} {throws} a Fire Tornado at {user2} ",
    "{user1} pokes {user2} in the eye !",
    "{user1} pokes {user2} on the sides!",
    "{user1} pokes {user2}!",
    "{user1} pokes {user2} with a needle!",
    "{user1} pokes {user2} with a pen!",
    "{user1} pokes {user2} with a stun gun!",
    "{user2} is secretly a Furry!",
    "Hey Everybody! {user1} is asking me to be mean!",
    "( ･_･)ﾉ⌒●~* (･.･;) <-{user2}",
    "Take this {user2}\n(ﾉﾟДﾟ)ﾉ ))))●~* ",
    "Here {user2} hold this\n(｀・ω・)つ ●~＊",
    "( ・_・)ノΞ●~*  {user2}\nDieeeee!!.",
    "( ・∀・)ｒ鹵~<≪巛;ﾟДﾟ)ﾉ\n*Bug sprays {user2}*.",
    "( ﾟДﾟ)ﾉ占~<巛巛巛.\n-{user2} You pest!",
    "( う-´)づ︻╦̵̵̿╤── \\(˚☐˚”)/ {user2}.",
    "{user1} {hits} {user2} with a {item}.",
    "{user1} {hits} {user2} in the face with a {item}.",
    "{user1} {hits} {user2} around a bit with a {item}.",
    "{user1} {throws} a {item} at {user2}.",
    "{user1} grabs a {item} and {throws} it at {user2}'s face.",
    "{user1} launches a {item} in {user2}'s general direction.",
    "{user1} starts slapping {user2} silly with a {item}.",
    "{user1} pins {user2} down and repeatedly {hits} them with a {item}.",
    "{user1} grabs up a {item} and {hits} {user2} with it.",
    "{user1} ties {user2} to a chair and {throws} a {item} at them.",
    "{user1} gave a friendly push to help {user2} learn to swim in lava.",
    "{user1} bullied {user2}.",
    "{user1} ate {user2}'s leg. *nomnomnom*",
    "{user1} {throws} a master ball at {user2}, resistance is futile.",
    "{user1} hits {user2} with an action beam...bbbbbb (ง・ω・)ง ====*",
    "{user1} ara ara's {user2}.",
    "{user1} ora ora's {user2}.",
    "{user1} muda muda's {user2}.",
    "{user2} was turned into a Jojo reference!",
    "{user1} hits {user2} with {item}.",
    "Round 2!..Ready? .. FIGHT!!",
    "WhoPixel will oof {user2} to infinity and beyond.",
    "{user2} ate a bat and discovered a new disease.",
    "{user1} folded {user2} into a paper plane",
    "{user1} served {user2} some bat soup.",
    "{user2} was sent to his home, the planet of the apes.",
    "{user1} kicked {user2} out of a moving train.",
    "{user2} just killed John Wick’s dog.",
    "{user1} performed an Avada Kedavra spell on {user2}.",
    "{user1} subjected {user2} to a fiery furnace.",
    "Sakura Haruno just got more useful than {user2}",
    "{user1} unplugged {user2}'s life support.",
    "{user1} subscribed {user2}' to 5 years of bad internet.",
    "You know what’s worse than Dad jokes? {user2}!",
    "{user1} took all of {user2}'s cookies.",
    "{user2} wa mou.......Shindeiru! - {user1}.",
    "{user2} lost his race piece!",  # No game no life reference
    "Shut up {user2}, you are just {user2}.",  # No game no life reference
    "{user1} hits {user2} with Aka si anse!",  # No game no life reference
    "@NeoTheKitty scratches {user2}",  # Pixels pet cat - @NeoTheKitty
    "Majin buu ate {user2}",  # Dbz
    "Goblin slayer slays {user2}",  # Goblin Slayer
)

ITEMS = (
    "cast iron skillet",
    "angry meow",
    "cricket bat",
    "wooden cane",
    "shovel",
    "toaster",
    "book",
    "laptop",
    "rubber chicken",
    "spiked bat",
    "heavy rock",
    "chunk of dirt",
    "ton of bricks",
    "rasengan",
    "spirit bomb",
    "100-Type Guanyin Bodhisattva",
    "rasenshuriken",
    "Murasame",
    "ban",
    "chunchunmaru",
    "Kubikiribōchō",
    "rasengan",
    "spherical flying kat",
)

THROW = (
    "throws",
    "flings",
    "chucks",
    "hurls",
    "tosses",
)

HIT = (
    "hits",
    "whacks",
    "slaps",
    "smacks",
    "beshes",
    "pimp slaps",
    "pats",
)

HUG_TEMPLATES = (
    "{user1} {hug} {user2}.",
    "{user1} {hug} {user2} warmly.",
    "{user1} {hug} {user2} with a love. 💘",
    "{user1} {hug} {user2} with kindness.",
)

HUG = ("hugs", "hugged", "kissed", "pinches")

PAT_TEMPLATES = (
    "{user1} pats {user2} on the head.",
    "*gently rubs {user2}'s head*.",
    "*{user1} mofumofus {user2}'s head*",
    "*{user1} messes up {user2}'s head*",
    "*{user1} intensly rubs {user2}'s head*",
    "*{user2}'s waifu pats their head*",
    "*{user2}'s got free headpats*",
    "No pats for {user2}!",
    "Oh no! We are all out of pats.",
    "This is a designated no pat zone!",
    "No pats for {user2}!",
    "{user1} spoils {user2} with headpats!",
    "{user2} received one free headpat!",
    "{user1} headpats {user2} whilst giving a lap pillow",
    "{user1} aggressively pats {user2}",
    "{user1} gently strokes {user2}'s head",
    "Pat, pat, pat, pat",
    "{user2} could not escape {user1}'s headpats",
    "{user2}.exe has stopped working",
    "{user1} rubs {user2} on the neck",
    "Must... extort... HEADPATS",
    "{user1} headpats {user2}'s head with a pat",
    "{user1} pats {user2} unexpectedly",
    "{user1} pats {user2} with consent, maybe?",
    "Pat pat, {user2} honto kawaii ne!",
    "{user1} headpats {user2} at 420apm",
    "{user1} bellyrubs {user2}",
    "{user1} pats {user2} friendlily",
    "(*´ω´(*｀ω｀)",
    "(ｏ・_・)ノ”(ᴗ_ ᴗ。)",
    "(*￣▽￣)ノ”(- -*)",
    "(っ´ω`)ﾉ(╥ω╥)",
    "( ´Д｀)ﾉ(´･ω･`) ﾅﾃﾞﾅﾃﾞ",
)


async def mention_user(user_id):
    # Fetch the entity (user) based on the provided user_id
    entity = await ultroid_bot.get_entity(user_id)

    # Get the display name and escape it for HTML
    mention = get_display_name(entity)
    escaped_mention = html.escape(mention)

    # Create the permalink
    permalink = f"<a href='tg://user?id={entity.id}'>{escaped_mention}</a>"

    # Return the permalink
    return permalink


@ultroid_cmd(pattern=r"slap(.*)")
async def slap(event):
    reply_message = await event.get_reply_message()
    # Extract the arguments from the pattern
    args = event.pattern_match.group(1).split()
    await event.get_chat()

    reply_message.text if reply_message else event.message.text
    if hasattr(
        event.message.to_id, "user_id"
    ):  # Check if 'to_id' attribute is present and is a user ID
        curr_user_id = event.message.to_id.user_id
    else:
        curr_user_id = (await ultroid_bot.get_me()).id

    # Await the extract_user function call
    user_id = await extract_user(event.message, args)

    if user_id:
        user1 = await mention_user((await ultroid_bot.get_me()).id)
        user2 = await mention_user(user_id)
    else:
        user1 = await mention_user((await ultroid_bot.get_me()).id)
        user2 = await mention_user(curr_user_id)

    temp = random.choice(SLAP_TEMPLATES)
    item = random.choice(ITEMS)
    hit = random.choice(HIT)
    throw = random.choice(THROW)

    reply = temp.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw)

    await event.message.edit(reply, parse_mode="html")


@ultroid_cmd(pattern=r"hug(.*)")
async def hug(event):
    reply_message = await event.get_reply_message()
    # Extract the arguments from the pattern
    args = event.pattern_match.group(1).split()
    await event.get_chat()

    reply_message.text if reply_message else event.message.text
    if hasattr(
        event.message.to_id, "user_id"
    ):  # Check if 'to_id' attribute is present and is a user ID
        curr_user_id = event.message.to_id.user_id
    else:
        curr_user_id = (await ultroid_bot.get_me()).id

    # Await the extract_user function call
    user_id = await extract_user(event.message, args)

    if user_id:
        user1 = await mention_user((await ultroid_bot.get_me()).id)
        user2 = await mention_user(user_id)
    else:
        user1 = await mention_user((await ultroid_bot.get_me()).id)
        user2 = await mention_user(curr_user_id)

    temp = random.choice(HUG_TEMPLATES)
    hug = random.choice(HUG)

    reply = temp.format(user1=user1, user2=user2, hug=hug)

    await event.message.edit(reply, parse_mode="html")


@ultroid_cmd(pattern=r"pat(.*)")
async def pat(event):
    reply_message = await event.get_reply_message()
    # Extract the arguments from the pattern
    args = event.pattern_match.group(1).split()
    await event.get_chat()

    reply_message.text if reply_message else event.message.text
    if hasattr(
        event.message.to_id, "user_id"
    ):  # Check if 'to_id' attribute is present and is a user ID
        curr_user_id = event.message.to_id.user_id
    else:
        curr_user_id = (await ultroid_bot.get_me()).id

    # Await the extract_user function call
    user_id = await extract_user(event.message, args)

    if user_id:
        user1 = await mention_user((await ultroid_bot.get_me()).id)
        user2 = await mention_user(user_id)
    else:
        user1 = await mention_user((await ultroid_bot.get_me()).id)
        user2 = await mention_user(curr_user_id)

    temp = random.choice(PAT_TEMPLATES)

    reply = temp.format(user1=user1, user2=user2)

    await event.message.edit(reply, parse_mode="html")
