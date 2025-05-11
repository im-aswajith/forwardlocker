from telegram import Update, InputFile
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)
import tempfile
import os

# Your bot token
BOT_TOKEN = "TELEGRAM-BOT-API"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! Send me any text, photo, file, or video and I’ll send it back to you — with the original filename and a spoiler if needed."
    )

# Handle images
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()

    temp_filename = "image.jpg"
    file_path = os.path.join(tempfile.gettempdir(), temp_filename)
    await file.download_to_drive(file_path)

    with open(file_path, "rb") as img:
        await update.message.reply_photo(
            photo=InputFile(img, filename=temp_filename),
            has_spoiler=True
        )

    os.remove(file_path)

# Handle documents
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    file = await document.get_file()

    filename = document.file_name
    file_path = os.path.join(tempfile.gettempdir(), filename)
    await file.download_to_drive(file_path)

    with open(file_path, "rb") as doc:
        await update.message.reply_document(document=InputFile(doc, filename=filename))

    os.remove(file_path)

# Handle videos with spoiler
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video
    file = await video.get_file()

    filename = video.file_name or "video.mp4"
    file_path = os.path.join(tempfile.gettempdir(), filename)
    await file.download_to_drive(file_path)

    with open(file_path, "rb") as vid:
        await update.message.reply_video(
            video=InputFile(vid, filename=filename),
            has_spoiler=True
        )

    os.remove(file_path)

# Handle text messages
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📨 You said: {update.message.text}")

# Main entry
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    print("🤖 Bot is running...")
    app.run_polling()
