# main.py
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from aiogram import Bot
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Конфигурация логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_endpoint.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Инициализация FastAPI
app = FastAPI(title="RJ45")


# Модель данных для входящего запроса
class MessageRequest(BaseModel):
    message: str


# Конфигурация
BOT_TOKEN = "8127565713:AAEjTVsizesQWp58-rFECqsOARzfmaU9gmY"
CHAT_ID = "-4753969005"
PORT = 20121  # Выбранный порт из диапазона 10000-50000

# Инициализация бота
bot = Bot(token=BOT_TOKEN)


@app.post("/telegram")
async def send_telegram_message(request: MessageRequest):
    """
    Эндпоинт для отправки сообщения в Telegram чат
    """
    try:
        # Логирование входящего запроса
        logger.info(f"Received request: {request.message[:50]}...")

        # Отправка сообщения в Telegram
        message = await bot.send_message(
            chat_id=CHAT_ID,
            text=request.message,
            parse_mode="Markdown"
        )

        # Логирование успешной отправки
        logger.info(f"Message sent successfully. Message ID: {message.message_id}")

        return {"status": "success", "message_id": message.message_id}

    except Exception as e:
        # Логирование ошибки
        error_msg = f"Failed to send message: {str(e)}"
        logger.error(error_msg)

        # Возврат ошибки клиенту
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Ошибка отправки сообщения в Telegram",
                "details": str(e)
            }
        )


# Запуск приложения
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
