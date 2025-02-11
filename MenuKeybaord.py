import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
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

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Create the persistent menu
    menu_buttons = [
        ["外卖", "换汇", "闲置", "求职"],
        ["滴滴", "签证", "代购", "红包"],
        ["充值", "收款", "转账", "我的"],
    ]
    reply_markup = ReplyKeyboardMarkup(menu_buttons, resize_keyboard=True, one_time_keyboard=False)
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

# Main function
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
