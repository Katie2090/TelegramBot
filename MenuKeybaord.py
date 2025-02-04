from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging
import json
import asyncio
from telegram import InputMediaPhoto, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import os
import logging

# Enable logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# File to store user chat IDs
USER_CHAT_IDS_FILE = "user_chat_ids.json"

# Load user chat IDs from file
def load_user_chat_ids():
    try:
        with open(USER_CHAT_IDS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save user chat IDs to file
def save_user_chat_ids(user_chat_ids):
    with open(USER_CHAT_IDS_FILE, "w") as file:
        json.dump(user_chat_ids, file)

# /start command handler
async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_chat_ids = load_user_chat_ids()

    # Store new user chat_id
    if chat_id not in user_chat_ids:
        user_chat_ids.append(chat_id)
        save_user_chat_ids(user_chat_ids)

    keyboard = [
        [KeyboardButton("✈ 落地接机"), KeyboardButton("🔖 证照办理"), KeyboardButton("🏤 房产凭租")],
        [KeyboardButton("🏩 酒店预订"), KeyboardButton("🍽️ 食堂信息"), KeyboardButton("📦 生活物资")],
        [KeyboardButton("🔔 后勤生活信息频道")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    await update.message.reply_text("欢迎使用机器人服务，请选择一个选项:", reply_markup=reply_markup)

# Handle menu button clicks
async def handle_menu_selection(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text

    # 落地接机
    if user_input == "✈ 落地接机":
        inline_keyboard = [[InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"),
                            InlineKeyboardButton("✈ 接机频道", url="https://t.me/+pqM959ERihBkYTc9")]]
        inline_markup = InlineKeyboardMarkup(inline_keyboard)

        await update.message.reply_photo(
            photo="images/接机.jpg",
            caption="🌟 欢迎加入【后勤接机】群 🌟\n\n"
                    "📋 《须填的信息》\n"
                    "✈️ 落地签办理信息：\n"
                    "时间：2025年01月02日（周四）\n"
                    "类型：落地商务签 + 接关\n"
                    "航班号：CA745\n"
                    "抵达时间：23:10（金边时间）\n"
                    "客户人数：1位\n"
                    "备注：鲁先生\n\n"
                    "✅ 请核对以上信息，如有更改，请及时点击联系客服！ 😊",
            reply_markup=inline_markup
        )

    # 证照办理
    elif user_input == "🔖 证照办理":
        inline_keyboard = [[InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"),
                           InlineKeyboardButton("🔖 证件办理频道", url="https://t.me/+sINSVji28vM4ZDJl")]]
        inline_markup = InlineKeyboardMarkup(inline_keyboard)

        await update.message.reply_photo(
            photo="images/passport.jpg",
            caption="📋 证照办理服务：\n\n"
                    "✔️ 提供快速办理签证、护照及其他相关证件的服务。\n"
                    "📞 点击客服咨询更多详情。",
            reply_markup=inline_markup
        )

    # 房产凭租
    elif user_input == "🏤 房产凭租":
        inline_keyboard = [[InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"),
                            InlineKeyboardButton("🏤 房产信息频道", url="https://t.me/+8i7xQLV_UiY2NTY1")]]
        inline_markup = InlineKeyboardMarkup(inline_keyboard)

        await update.message.reply_photo(
            photo="images/resized-image.jpg",
            caption="🏤 房产租赁信息：\n\n"
                    "✔️ 提供房产出租和购房服务，涵盖各类房型。\n"
                    "🔍 点击下方按钮了解更多。",
            reply_markup=inline_markup
        )

    # 酒店预订
    elif user_input == "🏩 酒店预订":
        inline_keyboard = [[InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"),
                            InlineKeyboardButton("🏩 酒店详情频道", url="https://t.me/+M5Q_hf4xyG00YzRl")]]
        inline_markup = InlineKeyboardMarkup(inline_keyboard)

        await update.message.reply_photo(
            photo="images/sofietel.jpg",
            caption="🏨高端酒店预订代办服务| 索菲特 & 瑰丽酒店 |🏨\n\n"
            "✨ 奢华体验，优惠价格，预订更省心！ ✨\n\n"
            "📞 联系我们，轻松享受高端住宿！\n",
            reply_markup=inline_markup
        )

    # 食堂信息
    elif user_input == "🍽️ 食堂信息":
        inline_keyboard = [[InlineKeyboardButton("🧑🏻‍💻 餐厅客服", url="https://t.me/DINGCHUANG001"),
                           InlineKeyboardButton("查看食堂详情", url="https://t.me/+M0su9kfTZHk2ODU1")]]
        inline_markup = InlineKeyboardMarkup(inline_keyboard)

        await update.message.reply_photo(
            photo="images/食堂.jpg",
            caption="本食堂致力于为员工和学生提供健康、营养、美味的餐食。\n"
                    "我们拥有宽敞舒适的就餐环境、丰富的菜品选择，以及严格的食品安全管理，确保每位顾客都能享受到高质量的餐饮服务。\n"
                    "提供多样化的菜品，以满足不同口味和需求。",
            reply_markup=inline_markup
        )

    # 生活物资
    elif user_input == "📦 生活物资":
        inline_keyboard = [[InlineKeyboardButton("🧑🏻‍💻 在线客服", url="https://t.me/HQBGSKF"),
                            InlineKeyboardButton("📦 生活物资详情", url="https://t.me/+A0W4dKUEyzM1ZDRl")]]
        inline_markup = InlineKeyboardMarkup(inline_keyboard)

        await update.message.reply_photo(
            photo="images/生活用品.jpg",
            caption="🔥 强烈推荐！宿舍/新居生活必备超值套装！🔥\n\n"
                    "💡 你是否刚搬进新宿舍？刚入住新公寓？还是在为日常生活物资发愁？不用担心！这套 “生活必备大礼包” 直接拯救你的日常所需！💪\n"
                    "📢 赶紧入手！让你的生活从第一天起就井井有条，舒适自在！ 💯\n",
            reply_markup=inline_markup
        )
    
    # 后勤生活信息频道
    elif user_input == "🔔 后勤生活信息频道":
        inline_keyboard = [[InlineKeyboardButton("🔔 详细了解", url="https://t.me/+QQ56RVTKshQxMDU1")]]
        inline_markup = InlineKeyboardMarkup(inline_keyboard)

        await update.message.reply_photo(
            photo="images/logistic.png",
            caption=" 主要提供各种后勤管理和生活服务，确保用户能够方便、高效地获取信息和帮助。\n\n"
                    "🚀 为什么选择 🔔 后勤生活信息频道？\n"
                    "✅ 一站式后勤服务：省时省力，所有需求一键获取！\n"
                    "✅ 信息透明 & 实时更新：随时查看最新房产、酒店、食堂、证照办理等信息！\n"
                    "✅ 高效便捷：提供在线咨询、快速反馈，解决问题更迅速！\n"
                    "✅ 支持定制化服务：根据不同需求提供个性化支持，如VIP接待、特殊证件办理等！\n\n"
                    "📢 无论是住宿、出行、餐饮，还是证件办理、渠道合作，后勤生活信息频道都能为你提供全方位的服务支持！ 🎯💼\n"
                    "📌 立即加入，体验高效便捷的后勤服务！ ✅",
            reply_markup=inline_markup
        )
    # elif user_input == "🔔 后勤生活信息频道":
    #     await update.message.reply_text(
    #         "🔔 后勤生活信息频道：\n\n"
    #         "💡 关注后勤信息，获取最新服务资讯。\n"
    #         "📢 请加入我们的频道：https://t.me/example-channel"
    #     )

    else:
        await update.message.reply_text("未识别的选项，请选择菜单中的一个选项。")

# /broadcast command handler (always sends the latest message)
async def broadcast(update: Update, context: CallbackContext) -> None:
    """Send a broadcast message with the latest content defined in the code."""
    user_chat_ids = load_user_chat_ids()
    
    if not user_chat_ids:
        await update.message.reply_text("⚠️ 没有已注册的用户，请确保用户已发送 /start 以注册。")
        return

    # ✨ Define the latest broadcast message here! ✨
    message_text = """🔥 强烈推荐！宿舍/新居生活必备超值套装！ 🔥

💡 你是否刚搬进新宿舍？刚入住新公寓？还是在为日常生活物资发愁？不用担心！这套 “生活必备大礼包” 直接拯救你的日常所需！ 💪"""

    # 🖼️ Define the latest image here! (Local path or URL)
    photo_path = "images/工卡.jpg"  # Ensure the file exists in the folder

    # 🔘 Define inline buttons here!
    buttons = [
        [InlineKeyboardButton("💬 在线客服", url="https://t.me/HQBGSKF"),
         InlineKeyboardButton("📦 生活物资详情", url="https://t.me/+A0W4dKUEyzM1ZDRl")]
    ]
    inline_markup = InlineKeyboardMarkup(buttons)

    sent_count = 0
    failed_count = 0

    for chat_id in user_chat_ids:
        try:
            with open(photo_path, "rb") as photo:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=message_text,
                    reply_markup=inline_markup
                )
            logger.info(f"✅ Sent message to {chat_id}")
            sent_count += 1
        except Exception as e:
            logger.error(f"❌ Failed to send message to {chat_id}: {e}")
            failed_count += 1

    # Confirmation message for sender
    await update.message.reply_text(
        f"✅ 广播消息已发送！\n📨 成功: {sent_count} 人\n⚠️ 失败: {failed_count} 人"
    )

# /update command handler
async def update_message_command(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 3:
        await update.message.reply_text("⚠️ 格式错误！请使用：\n\n/update <chat_id> <message_id> <新内容>")
        return

    chat_id = int(context.args[0])
    message_id = int(context.args[1])
    new_message = " ".join(context.args[2:])

    await update_message(context, chat_id, message_id, new_message)
    await update.message.reply_text("✅ 消息已更新。")

# Main function to run the bot
def main():
    token = "7100869336:AAH1khQ33dYv4YElbdm8EmYfARMNkewHlKs"  # Replace with your bot token

    application = Application.builder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_selection))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("update", update_message_command))

    logger.info("Starting bot...")
    application.run_polling()

if __name__ == "__main__":
    main()
