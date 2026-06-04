import asyncio
import os
from pathlib import Path
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile

# Токен, который вы получили от @BotFather
BOT_TOKEN = "8687946018:AAGq59OQfV3PKInGTdZDyy69RBWar0w-qDc"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Исправленный путь: ищем huy.PNG в текущей папке, либо в app/Folder
# Проверим оба варианта, чтобы наверняка сработало на вашем хостинге
BASE_DIR = Path(__file__).parent

# Вариант 1: Если бот уже запущен внутри app/Folder
PATH_1 = BASE_DIR / "huy.PNG"
# Вариант 2: Если бот запущен в корне, а фото в app/Folder
PATH_2 = BASE_DIR / "app" / "Folder" / "huy.PNG"


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Выбираем тот путь, который реально существует
    if PATH_1.exists():
        photo_path = PATH_1
    elif PATH_2.exists():
        photo_path = PATH_2
    else:
        photo_path = None

    if photo_path:
        photo = FSInputFile(photo_path)
        await message.answer_photo(photo, caption="Вот фото с хостинга!")
    else:
        # Если снова не найдет, бот напишет в чат, где именно он искал файл
        await message.answer(
            f"Ошибка! Файл не найден.\n"
            f"Бот искал его здесь:\n"
            f"1) {PATH_1.resolve()}\n"
            f"2) {PATH_2.resolve()}"
        )


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
