import os
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# -----------------------------
# SMALL CAPS FONT FUNCTION
# -----------------------------
def small(text):
    normal = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    smallcaps = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ" + "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ"
    return text.translate(str.maketrans(normal, smallcaps))


# -----------------------------
# ENV VARIABLES
# -----------------------------
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

OWNER_ID = os.getenv("OWNER_ID")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
MOVIE_GROUP = os.getenv("MOVIE_GROUP")
START_IMAGE = os.getenv("START_IMAGE")

app = Client(
    "RenameBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# -----------------------------
# START COMMAND
# -----------------------------
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):

    caption = small(
        "👋 HEY THERE!\n\n"
        "I AM A POWERFUL RENAME + CONVERT BOT WITH PREMIUM FEATURES ⚡\n\n"
        "⭐ RENAME ANY FILE IN SECONDS\n"
        "🎥 AUTO VIDEO RECODE / CONVERT\n"
        "🖼️ CUSTOM THUMBNAIL SUPPORT\n"
        "🚀 SUPER FAST UPLOAD SPEED\n"
        "🔐 PRIVATE CHAT ONLY — SAFE & SECURE"
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(small("👑 OWNER"), url=f"https://t.me/{OWNER_ID}")],
        [InlineKeyboardButton(small("📢 CHANNEL"), url=f"https://t.me/{CHANNEL_USERNAME}")],
        [InlineKeyboardButton(small("🎬 MOVIE GROUP"), url=f"https://t.me/{MOVIE_GROUP}")]
    ])

    await message.reply_photo(
        START_IMAGE,
        caption=caption,
        reply_markup=buttons
    )


# -----------------------------
# MEDIA INFO HANDLER
# -----------------------------
@app.on_message(filters.private & (filters.document | filters.video))
async def media_info(client, message):

    media = message.document or message.video
    file_name = media.file_name
    file_size = f"{round(media.file_size/1024/1024,2)} Mʙ" if media.file_size < 1024**3 else f"{round(media.file_size/1024/1024/1024,2)} Gʙ"
    mime = media.mime_type
    dc_id = media.dc_id

    info = small(
        f"ᴍᴇᴅɪᴀ ɪɴꜰᴏ:\n\n"
        f"◈ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: {file_name}\n"
        f"◈ ᴇxᴛᴇɴꜱɪᴏɴ: {mime.split('/')[-1].upper()}\n"
        f"◈ ꜰɪʟᴇ ꜱɪᴢᴇ: {file_size}\n"
        f"◈ ᴍɪᴍᴇ ᴛʏᴘᴇ: {mime}\n"
        f"◈ ᴅᴄ ɪᴅ: {dc_id}\n\n"
        "ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ ᴀɴᴅ ʀᴇᴘʟʏ ᴛʜɪs ᴍᴇssᴀɢᴇ...."
    )

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(small("📄 DOCUMENT"), callback_data="doc"),
            InlineKeyboardButton(small("🎬 VIDEO"), callback_data="vid")
        ]
    ])

    await message.reply_text(info, reply_markup=buttons, quote=True)


# -----------------------------
# STORE DOC/VIDEO CHOICE
# -----------------------------
user_choice = {}

@app.on_callback_query()
async def cb_handler(client, query):

    if query.data == "doc":
        user_choice[query.from_user.id] = "document"
        await query.answer(small("DOCUMENT SELECTED ✔"))
        await query.message.reply(small("ENTER NEW FILENAME WITH EXTENSION…"), quote=True)

    if query.data == "vid":
        user_choice[query.from_user.id] = "video"
        await query.answer(small("VIDEO SELECTED ✔"))
        await query.message.reply(small("ENTER NEW FILENAME WITH EXTENSION…"), quote=True)


# -----------------------------
# PROGRESS BAR FUNCTION
# -----------------------------
async def progress(current, total, message, start):
    now = time.time()
    speed = current / (now - start) if (now - start) > 0 else 0
    percent = current * 100 / total if total > 0 else 0
    eta = (total - current) / speed if speed > 0 else 0

    bar = "▢" * int(percent / 5)

    text = small(
        f"Download Started...\n\n"
        f"{bar}\n\n"
        f"╭━━━━❰ST BOTS PROCESSING...❱━➣\n"
        f"┣⪼ 🗃️ ꜱɪᴢᴇ: {round(current/1024/1024,2)} Mʙ | {round(total/1024/1024/1024,2)} Gʙ\n"
        f"┣⪼ ⏳️ ᴅᴏɴᴇ : {round(percent,2)}%\n"
        f"┣⪼ 🚀 ꜱᴩᴇᴇᴅ: {round(speed/1024/1024,2)} Mʙ/s\n"
        f"┣⪼ ⏰️ ᴇᴛᴀ: {int(eta//60)}ᴍ, {int(eta%60)}ꜱ\n"
        f"╰━━━━━━━━━━━━━━━➣"
    )

    try:
        await message.edit(text)
    except:
        pass


# -----------------------------
# RENAME HANDLER
# -----------------------------
@app.on_message(filters.private & filters.reply)
async def rename_handler(client, message):

    if not message.reply_to_message:
        return

    media = message.reply_to_message.document or message.reply_to_message.video
    new_name = message.text

    processing = await message.reply(small("Download Started..."))

    start = time.time()

    temp_path = f"/tmp/{new_name}"

    downloaded = await client.download_media(
        message.reply_to_message,
        file_name=temp_path,
        progress=progress,
        progress_args=(processing, start)
    )

    file_type = user_choice.get(message.from_user.id, "document")

    if file_type == "video":
        await message.reply_video(downloaded)
    else:
        await message.reply_document(downloaded)

    os.remove(downloaded)
    await processing.edit(small("✔ DONE! FILE UPLOADED SUCCESSFULLY"))


# -----------------------------
# START BOT
# -----------------------------
app.run()
