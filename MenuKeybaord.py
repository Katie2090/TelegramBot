import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store user IDs in a file
USER_DATA_FILE = "user_ids.txt"

# Load user IDs from file
def load_user_ids():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return set(file.read().splitlines())
    return set()

# Save user IDs to file
def save_user_ids(user_ids):
    with open(USER_DATA_FILE, "w") as file:
        for user_id in user_ids:
            file.write(f"{user_id}\n")

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    user_ids = load_user_ids()
    user_ids.add(user_id)
    save_user_ids(user_ids)

    # Create menu buttons
    menu_buttons = [
        ["外卖", "换汇", "闲置", "求职"],
        ["滴滴", "签证", "代购", "红包"],
        ["充值", "收款", "转账", "我的"],
    ]
    reply_markup = ReplyKeyboardMarkup(menu_buttons, resize_keyboard=True)
    await update.message.reply_text("欢迎使用亚太·亚通机器人！请选择一个选项：", reply_markup=reply_markup)

# Handle menu button clicks
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "外卖":
        await update.message.reply_text("外卖服务信息...")
    elif text == "换汇":
        await update.message.reply_text("换汇服务信息...")
    elif text == "闲置":
        await update.message.reply_text("闲置物品信息...")
    elif text == "求职":
        await update.message.reply_text("求职信息...")
    elif text == "滴滴":
        await update.message.reply_text("滴滴服务信息...")
    elif text == "签证":
        await update.message.reply_text("签证服务信息...")
    elif text == "代购":
        await update.message.reply_text("代购服务信息...")
    elif text == "红包":
        await update.message.reply_text("红包服务信息...")
    elif text == "充值":
        await update.message.reply_text("充值服务信息...")
    elif text == "收款":
        await update.message.reply_text("收款服务信息...")
    elif text == "转账":
        await update.message.reply_text("转账服务信息...")
    elif text == "我的":
        await update.message.reply_text("个人信息...")

# Command: /broadcast
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_ids = load_user_ids()
    args = context.args

    if not args:
        await update.message.reply_text("用法: /broadcast <消息> [图片URL] [按钮文本|按钮URL]")
        return

    # Extract messages, photos, and buttons from args
    messages = []
    photos = []
    buttons = []

    # Parse arguments
    i = 0
    while i < len(args):
        if args[i].startswith("http"):  # Assume it's a photo URL
            photos.append(args[i])
        elif "|" in args[i]:  # Assume it's a button (text|url)
            button_text, button_url = args[i].split("|")
            buttons.append(InlineKeyboardButton(button_text, url=button_url))
        else:  # Assume it's a message
            messages.append(args[i])
        i += 1

    # Create inline keyboard if buttons exist
    reply_markup = None
    if buttons:
        reply_markup = InlineKeyboardMarkup([buttons])

    # Send messages, photos, and buttons to all users
    for user_id in user_ids:
        try:
            # Send messages
            for message in messages:
                await context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup)

            # Send photos
            if photos:
                media_group = [InputMediaPhoto(photo) for photo in photos]
                await context.bot.send_media_group(chat_id=user_id, media=media_group)
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}: {e}")

    await update.message.reply_text("广播消息已发送给所有用户！")

# Main function
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
