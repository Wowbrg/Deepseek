import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

API_KEY = "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"  # Твой OpenRouter API ключ


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # Формируем запрос в OpenRouter
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "model": "gpt-3.5-turbo",  # Используем стандартную модель, чтобы проверить
            "messages": [{"role": "user", "content": user_message}]
        }

        # Отправка запроса в OpenRouter API
        async with httpx.AsyncClient() as client:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
            response_data = response.json()

        # Проверяем, что ответ содержит ключ 'choices'
        if "choices" in response_data:
            reply = response_data["choices"][0]["message"]["content"]
            await update.message.reply_text(reply)
        else:
            await update.message.reply_text("Error: Response does not contain 'choices'.")

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


if name == 'main':
    app = ApplicationBuilder().token("7813435123:AAFF2kaJRgeZxdHznkVbbU5l9y9iEJq4MDA").build()  # Токен Telegram-бота

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()