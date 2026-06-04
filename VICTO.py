import asyncio
import os
from pathlib import Path
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile

# Токен, который вы получили от @BotFather
BOT_TOKEN = "8687946018:AAGq59OQfV3PKInGTdZDyy69RBWar0w-qDc"

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Строим относительный путь: app/Folder/huy.jpg
# Path(__file__).parent берет папку, в которой лежит этот скрипт bot.py
PHOTO_PATH = Path(__file__).parent / "app" / "Folder" / "huy.png"


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Проверяем, существует ли файл по указанному пути
    if PHOTO_PATH.exists():
        # Передаем объект Path в FSInputFile
        photo = FSInputFile(PHOTO_PATH)
        await message.answer_photo(photo, caption="Вот фото из папки app/Folder!")
    else:
        await message.answer(
            f"Ошибка: Файл не найден по пути: {PHOTO_PATH.resolve()}"
        )


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
