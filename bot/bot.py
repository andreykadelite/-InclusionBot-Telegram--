import json
import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

load_dotenv()

DATA_DIR = Path("data")
USERS_FILE = DATA_DIR / "users.json"
REQUESTS_FILE = DATA_DIR / "requests.json"

DATA_DIR.mkdir(exist_ok=True)

# Utility functions

def load_json(path):
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Handlers

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Здравствуйте, {user.first_name}! Используйте /help для списка команд.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/register - регистрация и паспорт доступности\n"
        "/request - оставить заявку\n"
        "/knowledge - база знаний")

# Registration conversation
NAME, NEEDS = range(2)

async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите ваше ФИО:")
    return NAME

async def register_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Опишите ваши особые потребности:")
    return NEEDS

async def register_needs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    needs = update.message.text
    user_id = str(update.effective_user.id)
    users = load_json(USERS_FILE)
    users[user_id] = {
        'name': context.user_data.get('name'),
        'needs': needs
    }
    save_json(USERS_FILE, users)
    await update.message.reply_text("Спасибо! Ваши данные сохранены.")
    return ConversationHandler.END

async def register_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Регистрация отменена.")
    return ConversationHandler.END

# Request conversation
REQUEST_MSG = range(1)

async def request_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Опишите вашу проблему или вопрос:")
    return REQUEST_MSG

async def request_save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = str(update.effective_user.id)
    requests = load_json(REQUESTS_FILE)
    requests.setdefault(user_id, []).append(text)
    save_json(REQUESTS_FILE, requests)

    admin_chat_id = os.getenv("ADMIN_CHAT_ID")
    if admin_chat_id:
        await context.bot.send_message(chat_id=admin_chat_id,
                                       text=f"Новая заявка от {user_id}: {text}")

    await update.message.reply_text("Заявка отправлена. Спасибо!")
    return ConversationHandler.END

async def request_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Заявка отменена.")
    return ConversationHandler.END

# Knowledge base

async def knowledge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "База знаний:\n"
        "- Горячие клавиши Windows для скринридеров\n"
        "- Настройка контрастности экрана\n"
        "- Подбор ассистивных технологий"
    )
    await update.message.reply_text(text)


def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise RuntimeError("Необходимо установить переменную окружения TELEGRAM_TOKEN")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    register_conv = ConversationHandler(
        entry_points=[CommandHandler('register', register_start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_name)],
            NEEDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_needs)],
        },
        fallbacks=[CommandHandler('cancel', register_cancel)],
    )

    request_conv = ConversationHandler(
        entry_points=[CommandHandler('request', request_start)],
        states={
            REQUEST_MSG: [MessageHandler(filters.TEXT & ~filters.COMMAND, request_save)],
        },
        fallbacks=[CommandHandler('cancel', request_cancel)],
    )

    application.add_handler(register_conv)
    application.add_handler(request_conv)
    application.add_handler(CommandHandler("knowledge", knowledge))

    application.run_polling()

if __name__ == '__main__':
    main()
