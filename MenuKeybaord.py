import os
import json
import logging
import firebase_admin
from firebase_admin import credentials, firestore
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Firebase credentials securely
firebase_credentials = os.getenv("FIREBASE_CREDENTIALS_JSON")  # Match GitHub secret name
if firebase_credentials:
    try:
        if firebase_credentials.startswith("{"):  # Detect JSON string
            cred_dict = json.loads(firebase_credentials)
            cred = credentials.Certificate(cred_dict)
        elif os.path.exists(firebase_credentials):  # If it's a file path
            cred = credentials.Certificate(firebase_credentials)
        else:
            raise ValueError("Invalid Firebase Credentials")

        firebase_admin.initialize_app(cred)
        db = firestore.client()
    except Exception as e:
        logger.error(f"❌ Firebase initialization failed: {e}")
        exit(1)
else:
    logger.error("❌ FIREBASE_CREDENTIALS_JSON environment variable not set.")
    exit(1)

# Load Telegram bot token securely
token = os.getenv("TELEGRAM_BOT_TOKEN")
if not token:
    logger.error("❌ TELEGRAM_BOT_TOKEN environment variable not set.")
    exit(1)

# Firestore collection names
USER_COLLECTION = "telegram_users"
MESSAGE_COLLECTION = "sent_messages"

# Save user chat ID in Firestore
def save_user_chat_id(chat_id):
    db.collection(USER_COLLECTION).document(str(chat_id)).set({"chat_id": chat_id})

# Load all registered user chat IDs from Firestore
def load_user_chat_ids():
    users = db.collection(USER_COLLECTION).stream()
    return [user.id for user in users]

# Save sent message ID for editing
def save_message_id(chat_id, message_id):
    db.collection(MESSAGE_COLLECTION).document(str(chat_id)).set({"message_id": message_id})

# Retrieve stored message ID
def get_message_id(chat_id):
    doc = db.collection(MESSAGE_COLLECTION).document(str(chat_id)).get()
    if doc.exists and doc.to_dict():
        return doc.to_dict().get("message_id")
    return None

# /start command - Register users and show menu
async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id
    save_user_chat_id(chat_id)

    keyboard = [
        [KeyboardButton("✈ 落地接机"), KeyboardButton("🔖 证照办理")],
        [KeyboardButton("🏤 房产租赁"), KeyboardButton("🏩 酒店预订")],
        [KeyboardButton("🍽️ 食堂信息"), KeyboardButton("📦 生活物资")],
        [KeyboardButton("🔔 后勤生活信息频道")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    await update.message.reply_text("✅ 你已成功注册，可接收最新公告！\n请选择一个服务：", reply_markup=reply_markup)

# Main function to run the bot
def main():
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))

    logger.info("🚀 机器人已启动...")
    application.run_polling()

if __name__ == "__main__":
    main()
