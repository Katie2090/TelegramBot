import json
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

# ✅ Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Persistent Storage File
DATA_FOLDER = "data"
USER_CHAT_IDS_FILE = os.path.join(DATA_FOLDER, "user_chat_ids.json")

# ✅ Ensure the `data/` folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)

# 🔹 Load user chat IDs from the JSON file
def load_user_chat_ids():
    """Load saved user IDs from JSON (persistent storage)."""
    if os.path.exists(USER_CHAT_IDS_FILE):
        try:
            with open(USER_CHAT_IDS_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []  # Return an empty list if file is corrupted
    return []

# 🔹 Save user chat IDs to the JSON file
def save_user_chat_ids(user_chat_ids):
    """Save user IDs permanently in a JSON file."""
    with open(USER_CHAT_IDS_FILE, "w") as file:
        json.dump(user_chat_ids, file, indent=4)

# 🔹 Add a new user to the JSON file
def add_user(chat_id):
    """Add a user to the stored list if not already saved."""
    user_chat_ids = load_user_chat_ids()
    if chat_id not in user_chat_ids:
        user_chat_ids.append(chat_id)
        save_user_chat_ids(user_chat_ids)

# 🔹 Retrieve all saved users
def get_all_users():
    """Retrieve all saved user IDs."""
    return load_user_chat_ids()

# ✅ /start Command - Register Users Permanently
async def start(update: Update, context: CallbackContext) -> None:
    """Register users when they click /start (saved permanently)."""
    chat_id = update.message.chat_id
    add_user(chat_id)  # Save user permanently

    await update.message.reply_text("✅ 你已成功订阅广播！")

# ✅ /broadcast Command - Send Updated Message to All Users
async def broadcast(update: Update, context: CallbackContext) -> None:
    """Send the latest broadcast message, image, and buttons to all saved users."""
    user_chat_ids = get_all_users()

    if not user_chat_ids:
        await update.message.reply_text("⚠️ 没有已订阅的用户，请确保用户已发送 /start 以注册。")
        return

    # ✨ LATEST BROADCAST MESSAGE (Modify here!)
    message_text = """🔥 **最新促销活动！新用户专享 50% 折扣！** 🔥

💡 立即加入我们的服务，享受独家优惠！💪"""

    # 🖼️ Set the latest image (must exist in "images" folder)
    photo_path = "images/new_promotion.jpg"

    # 🔘 Define the latest buttons
    buttons = [
        [InlineKeyboardButton("🎉 立即领取优惠", url="https://t.me/join_sale"),
         InlineKeyboardButton("💬 客服咨询", url="https://t.me/HQBGSKF")]
    ]
    inline_markup = InlineKeyboardMarkup(buttons)

    sent_count = 0
    failed_count = 0

    # 📢 Send the latest message to all saved users
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

# ✅ Auto-Send Message on Bot Restart
async def auto_broadcast(context: CallbackContext) -> None:
    """Auto-send a message to all users when the bot restarts."""
    user_chat_ids = get_all_users()
    message_text = "🔄 **机器人已重新启动！请查看最新信息！**"

    for chat_id in user_chat_ids:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message_text, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"❌ 发送失败: {chat_id}: {e}")

# ✅ Main Function to Run the Bot
def main():
    token = "7100869336:AAH1khQ33dYv4YElbdm8EmYfARMNkewHlKs"  # Replace with your actual bot token

    application = Application.builder().token(token).build()

    # ✅ Initialize JobQueue properly
    job_queue = application.job_queue
    job_queue.run_once(auto_broadcast, when=10)  # Schedule auto-broadcast after 10 seconds

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast))

    logger.info("Starting bot...")
    application.run_polling()

if __name__ == "__main__":
    main()
