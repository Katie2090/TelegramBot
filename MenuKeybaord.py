import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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
    keyboard = [
        [InlineKeyboardButton("外卖", callback_data="takeaway")],
        [InlineKeyboardButton("换汇", callback_data="exchange")],
        [InlineKeyboardButton("闲置", callback_data="secondhand")],
        [InlineKeyboardButton("求职", callback_data="job")],
        [InlineKeyboardButton("滴滴", callback_data="didi")],
        [InlineKeyboardButton("签证", callback_data="visa")],
        [InlineKeyboardButton("代购", callback_data="shopping")],
        [InlineKeyboardButton("红包", callback_data="redpacket")],
        [InlineKeyboardButton("充值", callback_data="recharge")],
        [InlineKeyboardButton("收款", callback_data="collect")],
        [InlineKeyboardButton("转账", callback_data="transfer")],
        [InlineKeyboardButton("我的", callback_data="profile")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("欢迎使用亚太·亚通机器人！请选择一个选项：", reply_markup=reply_markup)

# Handle button clicks
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "takeaway":
        await query.edit_message_text(
            text="外卖服务信息...",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("返回", callback_data="back")]])
        )
    elif query.data == "exchange":
        await query.edit_message_text(
            text="换汇服务信息...",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("返回", callback_data="back")]])
        )
    # Add more conditions for other buttons
    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("外卖", callback_data="takeaway")],
            [InlineKeyboardButton("换汇", callback_data="exchange")],
            [InlineKeyboardButton("闲置", callback_data="secondhand")],
            [InlineKeyboardButton("求职", callback_data="job")],
            [InlineKeyboardButton("滴滴", callback_data="didi")],
            [InlineKeyboardButton("签证", callback_data="visa")],
            [InlineKeyboardButton("代购", callback_data="shopping")],
            [InlineKeyboardButton("红包", callback_data="redpacket")],
            [InlineKeyboardButton("充值", callback_data="recharge")],
            [InlineKeyboardButton("收款", callback_data="collect")],
            [InlineKeyboardButton("转账", callback_data="transfer")],
            [InlineKeyboardButton("我的", callback_data="profile")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("欢迎回来！请选择一个选项：", reply_markup=reply_markup)

# Command: /broadcast
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_ids = load_user_ids()
    message = " ".join(context.args)
    if not message:
        await update.message.reply_text("用法: /broadcast <消息>")
        return

    for user_id in user_ids:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}: {e}")

    await update.message.reply_text("广播消息已发送给所有用户！")

# Main function
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(CommandHandler("broadcast", broadcast))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
