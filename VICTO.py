import asyncio
import os
from pathlib import Path
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile

BOT_TOKEN = "8687946018:AAGq59OQfV3PKInGTdZDyy69RBWar0w-qDc"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Получаем абсолютный путь к папке, где лежит этот бот
    current_dir = Path(__file__).parent.resolve()

    # Пробуем несколько вариантов путей
    possible_paths = [
        current_dir / "huy.PNG",  # Если картинка лежит в той же папке, что и bot.py
        current_dir / "Folder" / "huy.PNG",  # Если bot.py в app/, а картинка в Folder/
        current_dir
        / "app"
        / "Folder"
        / "huy.PNG",  # Если bot.py в корне, а картинка в app/Folder/
        Path("/app/Folder/huy.PNG"),  # Прямой жесткий путь на сервере Linux
    ]

    photo_path = None
    for p in possible_paths:
        if p.exists():
            photo_path = p
            break

    if photo_path:
        # Если файл найден, отправляем его
        photo = FSInputFile(photo_path)
        await message.answer_photo(
            photo, caption=f"Успешно найдено!\nПуть: {photo_path}"
        )
    else:
        # Если файл НЕ найден, собираем информацию о файлах для диагностики
        try:
            files_in_dir = os.listdir(current_dir)
            files_list = "\n".join([f"- {f}" for f in files_in_dir])
        except Exception as e:
            files_list = f"Не удалось прочитать папку: {e}"

        error_text = (
            f"❌ Фото не найдено.\n\n"
            f"📁 Текущая папка бота:\n`{current_dir}`\n\n"
            f"📄 Файлы в этой папке:\n{files_list if files_list else '- Папка пуста'}\n\n"
            f"Перезапустите бота, отправьте /start и пришлите мне то, что он ответит."
        )
        await message.answer(error_text, parse_mode="Markdown")


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
