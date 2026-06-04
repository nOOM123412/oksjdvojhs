import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile

# Токен, который вы получили от @BotFather
BOT_TOKEN = "8687946018:AAGq59OQfV3PKInGTdZDyy69RBWar0w-qDc"

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Путь к вашему фото (название 'huy.jpg' в папке с проектом)
PHOTO_PATH = "huy.jpg"


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Проверяем, существует ли файл, чтобы бот не упал с ошибкой
    if os.path.exists(PHOTO_PATH):
        # Используем FSInputFile для отправки локального файла
        photo = FSInputFile(PHOTO_PATH)
        await message.answer_photo(photo, caption="Привет! Вот твое фото.")
    else:
        await message.answer(
            f"Ошибка: Файл {PHOTO_PATH} не найден в папке с проектом."
        )


async def main():
    print("Бот запущен и готов к работе...")
    # Запускаем поллинг (опрос серверов Telegram)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
