import os
import logging
import mysql.connector
import dotenv
from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Database Connection
def connect_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
    )

# ✅ Initialize Database Table
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (
            chat_id BIGINT PRIMARY KEY
        )"""
    )
    conn.commit()
    conn.close()

# ✅ Save User to MySQL
def add_user(chat_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (chat_id) VALUES (%s) ON DUPLICATE KEY UPDATE chat_id=VALUES(chat_id)", (chat_id,))
    conn.commit()
    conn.close()

# ✅ Get All Users
def get_all_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM users")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users

# ✅ Remove Failed Users
def remove_user(chat_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE chat_id=%s", (chat_id,))
    conn.commit()
    conn.close()

# ✅ Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ /start Command - Register Users
async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    add_user(chat_id)  # Save user ID to MySQL

    keyboard = [
        [KeyboardButton("✈ 落地接机"), KeyboardButton("🔖 证照办理"), KeyboardButton("🏤 房产凭租")],
        [KeyboardButton("🏩 酒店预订"), KeyboardButton("🍽️ 食堂信息"), KeyboardButton("📦 生活物资")],
        [KeyboardButton("🔔 后勤生活信息频道")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    await update.message.reply_text("✅ 你已成功订阅广播消息！", reply_markup=reply_markup)

# ✅ /broadcast Command - Send Message to All Users
async def broadcast(update: Update, context: CallbackContext) -> None:
    user_chat_ids = get_all_users()
    
    if not user_chat_ids:
        await update.message.reply_text("⚠️ 没有已注册的用户，请确保用户已发送 /start 以注册。")
        return

    # ✨ Broadcast message content
    message_text = """🔥 **最新公告！宿舍/新居生活必备超值套装！** 🔥

💡 你是否刚搬进新宿舍？刚入住新公寓？还是在为日常生活物资发愁？不用担心！这套 **“生活必备大礼包”** 直接拯救你的日常所需！💪"""

    # 🖼️ Image file
    photo_path = "images/工卡.jpg"

    # 🔘 Inline buttons
    buttons = [
        [InlineKeyboardButton("💬 在线客服", url="https://t.me/HQBGSKF"),
         InlineKeyboardButton("📦 生活物资详情", url="https://t.me/+A0W4dKUEyzM1ZDRl")]
    ]
    inline_markup = InlineKeyboardMarkup(buttons)

    sent_count = 0
    failed_count = 0
    failed_users = []

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
            failed_users.append(chat_id)  # Mark user as failed

    # Remove failed users from MySQL
    for failed_user in failed_users:
        remove_user(failed_user)

    await update.message.reply_text(
        f"✅ 广播消息已发送！\n📨 成功: {sent_count} 人\n⚠️ 失败: {failed_count} 人"
    )

# ✅ Auto-broadcast on bot restart
async def auto_broadcast(context: CallbackContext) -> None:
    user_chat_ids = get_all_users()
    message_text = "🔄 **机器人已重新启动！请查看最新信息！**"

    for chat_id in user_chat_ids:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message_text, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"❌ 发送失败: {chat_id}: {e}")

# ✅ Main Function with JobQueue
def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")  # 🔹 Use .env variable for security

    application = Application.builder().token(token).build()

    # ✅ Initialize MySQL Table
    init_db()

    # ✅ Initialize JobQueue properly
    job_queue = application.job_queue
    job_queue.run_once(auto_broadcast, when=10)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast))

    logger.info("Starting bot...")
    application.run_polling()

if __name__ == "__main__":
    main()
