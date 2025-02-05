import json
import os
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Enable logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ JSON File to Store User IDs
USER_CHAT_IDS_FILE = "user_chat_ids.json"

# 🔹 Load user chat IDs from the JSON file
def load_user_chat_ids():
    """Load user IDs from a JSON file (persistent storage)."""
    if os.path.exists(USER_CHAT_IDS_FILE):
        try:
            with open(USER_CHAT_IDS_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []  # Return an empty list if the file is corrupted
    return []

# 🔹 Save user chat IDs to the JSON file
def save_user_chat_ids(user_chat_ids):
    """Save user IDs to a JSON file."""
    with open(USER_CHAT_IDS_FILE, "w") as file:
        json.dump(user_chat_ids, file)

# 🔹 Add User to JSON File
def add_user(chat_id):
    """Add a user to the JSON file if not already saved."""
    user_chat_ids = load_user_chat_ids()
    if chat_id not in user_chat_ids:
        user_chat_ids.append(chat_id)
        save_user_chat_ids(user_chat_ids)

# 🔹 Get All Users from JSON File
def get_all_users():
    """Retrieve all saved user IDs."""
    return load_user_chat_ids()

# ✅ /start Command
async def start(update: Update, context: CallbackContext) -> None:
    """Register users when they click /start (stored in JSON)."""
    chat_id = update.message.chat_id

    # Save user ID permanently in JSON
    add_user(chat_id)

    keyboard = [
        [KeyboardButton("✈ 落地接机"), KeyboardButton("🔖 证照办理"), KeyboardButton("🏤 房产凭租")],
        [KeyboardButton("🏩 酒店预订"), KeyboardButton("🍽️ 食堂信息"), KeyboardButton("📦 生活物资")],
        [KeyboardButton("🔔 后勤生活信息频道")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    await update.message.reply_text("欢迎使用机器人服务，请选择一个选项:", reply_markup=reply_markup)

# ✅ /broadcast Command
async def broadcast(update: Update, context: CallbackContext) -> None:
    """Send a broadcast message to all saved users."""
    user_chat_ids = get_all_users()
    
    if not user_chat_ids:
        await update.message.reply_text("⚠️ 没有已注册的用户，请确保用户已发送 /start 以注册。")
        return

    # ✨ Broadcast message content
    message_text = """🔥 **最新公告！宿舍/新居生活必备超值套装！** 🔥

💡 你是否刚搬进新宿舍？刚入住新公寓？还是在为日常生活物资发愁？不用担心！这套 **“生活必备大礼包”** 直接拯救你的日常所需！💪"""

    # 🖼️ Image file (stored locally)
    photo_path = "images/最新公告.jpg"

    # 🔘 Inline buttons
    buttons = [
        [InlineKeyboardButton("💬 在线客服", url="https://t.me/HQBGSKF"),
         InlineKeyboardButton("📦 生活物资详情", url="https://t.me/+A0W4dKUEyzM1ZDRl")]
    ]
    inline_markup = InlineKeyboardMarkup(buttons)

    sent_count = 0
    failed_count = 0

    # 📢 Send messages to all users
    for chat_id in user_chat_ids:
        try:
            with open(photo_path, "rb") as photo:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=message_text,
                    parse_mode="Markdown",
                    reply_markup=inline_markup
                )
            logger.info(f"✅ Sent message to {chat_id}")
            sent_count += 1
        except Exception as e:
            logger.error(f"❌ Failed to send message to {chat_id}: {e}")
            failed_count += 1

    # Notify the admin of the results
    await update.message.reply_text(
        f"✅ 广播消息已发送！\n📨 成功: {sent_count} 人\n⚠️ 失败: {failed_count} 人"
    )

# ✅ Auto-broadcast on bot restart
async def auto_broadcast(context: CallbackContext) -> None:
    """Auto-send a message to all users when the bot restarts."""
    user_chat_ids = get_all_users()
    message_text = "🔄 **机器人已重新启动！请查看最新信息！**"

    for chat_id in user_chat_ids:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message_text, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"❌ 发送失败: {chat_id}: {e}")

# ✅ Main Function
def main():
    token = "7100869336:AAH1khQ33dYv4YElbdm8EmYfARMNkewHlKs"  # 🔹 Replace with your actual bot token

    application = Application.builder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast))

    # Automatically send updates when the bot restarts
    application.job_queue.run_once(auto_broadcast, 10)  # Send after 10 seconds

    logger.info("Starting bot...")
    application.run_polling()

if __name__ == "__main__":
    main()
