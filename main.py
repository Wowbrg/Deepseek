import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

API_KEY = "свой"  # OpenRouter API Key
BOT_TOKEN = "свой"  # Telegram Bot Token

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/YourBotUsername",  # Замени на ссылку на своего бота
        "X-Title": "DeepseekTelegramBot"
    }

    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [{"role": "user", "content": user_message}]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            response_data = response.json()

        if "choices" in response_data:
            reply = response_data["choices"][0]["message"]["content"]
            await update.message.reply_text(reply)
        else:
            await update.message.reply_text("Ошибка: в ответе нет ключа 'choices'.")

    except httpx.HTTPStatusError as e:
        await update.message.reply_text(f"HTTP ошибка: {e.response.status_code} {e.response.text}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()