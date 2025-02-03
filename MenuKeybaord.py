from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging
from time import sleep

# Enable logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the start command handler
async def start(update: Update, context: CallbackContext) -> None:
    # Create a grid-like menu using ReplyKeyboardMarkup
    keyboard = [
        [KeyboardButton("✈ 落地接机"), KeyboardButton("🔖 证照办理"),KeyboardButton("🏤 房产凭租")],
        [KeyboardButton("🏩 酒店预订"), KeyboardButton("🍽️ 食堂信息"), KeyboardButton("📦 生活物资")],
        [KeyboardButton("🔔 后勤生活信息频道")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("欢迎使用机器人服务，请选择一个选项:", reply_markup=reply_markup)

# Define the menu handler
async def handle_menu_selection(update: Update, context: CallbackContext) -> None:
    try:
        user_input = update.message.text

        if user_input == "✈ 落地接机":
            # Inline buttons to display below the photo
            inline_keyboard = [
                [InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"),InlineKeyboardButton("✈ 接机频道", url="https://t.me/+pqM959ERihBkYTc9")],
            ]
            inline_markup = InlineKeyboardMarkup(inline_keyboard)

            # Send photo, caption, and buttons together
            await context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo="images/接机.jpg",  # Replace with your image path
                caption="🌟 欢迎加入【后勤接机】群 🌟\n\n"  # Caption for the photo
                            "📋 《须填的信息》"

                            "✈️ 落地签办理信息："
                            "时间：2025年01月02日（周四）"
                            "类型：落地商务签 + 接关"
                            "航班号：CA745"
                            "抵达时间：23:10（金边时间）"
                            "客户人数：1位"
                            "备注：鲁先生"
                            
                            "✅ 请核对以上信息，如有更改，请及时点击联系客服！ 😊",
                reply_markup=inline_markup
            )

        elif user_input == "🔖 证照办理":
            inline_keyboard = [
                [InlineKeyboardButton("客服", url="https://example.com/exchange")],
            ]
            inline_markup = InlineKeyboardMarkup(inline_keyboard)

            # Send photo, caption, and buttons together
            await context.bot.send_photo(
                chat_id=update.message.chat_id,
               photo="images/passport.jpg",  # Replace with your image path
                caption="换汇服务: 查看最新汇率或者联系客服。",  # Caption for the photo
                reply_markup=inline_markup
            )

        elif user_input == "🏤 房产凭租":
            inline_keyboard = [
                [InlineKeyboardButton("客服", url="https://example.com/exchange")],
            ]
            inline_markup = InlineKeyboardMarkup(inline_keyboard)

            # Send photo, caption, and buttons together
            await context.bot.send_photo(
                chat_id=update.message.chat_id,
               photo="images/resized-image.jpg",  # Replace with your image path
                caption="换汇服务: 查看最新汇率或者联系客服。",  # Caption for the photo
                reply_markup=inline_markup
            )

        elif user_input == "🏩 酒店预订":
            inline_keyboard = [
                [InlineKeyboardButton("客服", url="https://example.com/exchange")],
            ]
            inline_markup = InlineKeyboardMarkup(inline_keyboard)

            # Send photo, caption, and buttons together
            await context.bot.send_photo(
                chat_id=update.message.chat_id,
               photo="images/sofietel.jpg",  # Replace with your image path
                caption="换汇服务: 查看最新汇率或者联系客服。",  # Caption for the photo
                reply_markup=inline_markup
            )
        elif user_input == "🍽️ 食堂信息":
            inline_keyboard = [
                [InlineKeyboardButton("更多详情", url="https://example.com/办证")],
            ]
            inline_markup = InlineKeyboardMarkup(inline_keyboard)

            # Send photo, caption, and buttons together
            await context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo="images/sofietel.jpg",  # Replace with your image path
                caption="办证服务详情如下:",  # Caption for the photo
                reply_markup=inline_markup
            )

        elif user_input == "📦 生活物资":
            inline_keyboard = [
                [InlineKeyboardButton("立即转账", url="https://example.com/transfer")],
            ]
            inline_markup = InlineKeyboardMarkup(inline_keyboard)

            # Send photo, caption, and buttons together
            await context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo="images/接机.jpg",  # Replace with your image path
                caption="转账服务即将上线，敬请期待！",  # Caption for the photo
                reply_markup=inline_markup
            )

        elif user_input == "🔔 后勤生活信息频道":
            inline_keyboard = [
                [InlineKeyboardButton("进群", url="https://t.me/+QQ56RVTKshQxMDU1")],
            ]
            inline_markup = InlineKeyboardMarkup(inline_keyboard)

            # Send photo, caption, and buttons together
            await context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo="images/Screenshot 2025-02-03 173313.png",  # Replace with your image path
                caption="房产服务详情如下:",  # Caption for the photo
                reply_markup=inline_markup
            )

        
        else:
            await update.message.reply_text("未识别的选项，请选择菜单中的一个选项。")

    except Exception as e:
        logger.error(f"Error in menu selection: {e}")
        await update.message.reply_text("发生错误，请稍后再试。")

# Main function to keep the bot running
def main():
    token = "7100869336:AAH1khQ33dYv4YElbdm8EmYfARMNkewHlKs"

    # Create the bot application
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))

    while True:
        try:
            logger.info("Starting bot...")
            application.run_polling()
        except Exception as e:
            logger.error(f"Bot stopped unexpectedly: {e}. Restarting in 5 seconds...")
            sleep(5)  # Wait before restarting

if __name__ == "__main__":
    main()
