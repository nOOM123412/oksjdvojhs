import asyncio
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

# Токен от @BotFather
BOT_TOKEN = "8687946018:AAGq59OQfV3PKInGTdZDyy69RBWar0w-qDc"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Базовая папка, где лежит VICTO.py (то есть /app)
BASE_DIR = Path(__file__).parent.resolve()


# Функция для поиска фото (логика не менялась)
def get_photo_path():
    possible_paths = [
        BASE_DIR / "Folder" / "huy.PNG",
        BASE_DIR / "data" / "huy.PNG",
        BASE_DIR / "huy.PNG",
        Path("/app/Folder/huy.PNG"),
    ]
    for p in possible_paths:
        if p.exists():
            return p
    return None


# Определяем состояния анкеты
class Questionnaire(StatesGroup):
    source = State()
    experience = State()
    time = State()
    confirm = State()


# --- КНОПКИ (КЛАВИАТУРЫ) ---

# 1. Кнопка "Отправить заявку"
kb_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отправить", callback_data="start_anketa")]
    ]
)

# 2. Кнопки "Откуда узнали" (по 2 в строку)
kb_source = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="От друга", callback_data="src_От друга"),
            InlineKeyboardButton(
                text="Из Рекламы", callback_data="src_Из Рекламы"
            ),
        ],
        [
            InlineKeyboardButton(text="В поиске", callback_data="src_В поиске"),
            InlineKeyboardButton(text="Другое", callback_data="src_Другое"),
        ],
    ]
)

# 3. Кнопки "Опыт работы" (по 2 в ряд)
kb_experience = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="~2 Года", callback_data="exp_~2 Года"),
            InlineKeyboardButton(text="~1 Год", callback_data="exp_~1 Год"),
        ],
        [
            InlineKeyboardButton(
                text="~6 Месяцев", callback_data="exp_~6 Месяцев"
            ),
            InlineKeyboardButton(text="Нет опыта", callback_data="exp_Нет опыта"),
        ],
    ]
)

# 4. Кнопки "Время работы" (по 2 в ряд)
kb_time = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="8+ Часов", callback_data="tm_8+ Часов"),
            InlineKeyboardButton(text="6-8 Часов", callback_data="tm_6-8 Часов"),
        ],
        [
            InlineKeyboardButton(text="3-6 Часов", callback_data="tm_3-6 Часов"),
            InlineKeyboardButton(text="1-2 Часа", callback_data="tm_1-2 Часа"),
        ],
    ]
)

# 5. Кнопки подтверждения (в одну строчку)
kb_confirm = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отправить", callback_data="final_send"),
            InlineKeyboardButton(text="Заново", callback_data="final_restart"),
        ]
    ]
)

# 6. Кнопки Главного меню (по 2 в строку)
kb_main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Направления", callback_data="menu_direct"),
            InlineKeyboardButton(text="Профиль", callback_data="menu_profile"),
        ],
        [
            InlineKeyboardButton(text="Настройки", callback_data="menu_settings"),
            InlineKeyboardButton(text="О проекте", callback_data="menu_about"),
        ],
    ]
)


# --- ХЕНДЛЕРЫ ---


# Команда /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    photo_path = get_photo_path()
    caption_text = (
        "Добро пожаловать в UDD TEAM!\nДля продолжения отправьте заявку"
    )

    if photo_path:
        photo = FSInputFile(photo_path)
        await message.answer_photo(
            photo, caption=caption_text, reply_markup=kb_start
        )
    else:
        await message.answer(
            f"❌ Фото huy.PNG не найдено, но вы можете продолжить:\n\n{caption_text}",
            reply_markup=kb_start,
        )


# Нажатие на кнопку "Отправить" под первой картинкой
@dp.callback_query(F.data == "start_anketa")
async def start_questionnaire(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()  # Удаляем прошлое сообщение (картинку приветствия)

    await callback.message.answer(
        "Откуда Вы узнали о нас?", reply_markup=kb_source
    )
    await state.set_state(Questionnaire.source)
    await callback.answer()


# Шаг 1: Обработка источника
@dp.callback_query(Questionnaire.source, F.data.startswith("src_"))
async def process_source(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()  # Удаляем вопрос "Откуда узнали"

    chosen_source = callback.data.split("_")[1]
    await state.update_data(source=chosen_source)

    await callback.message.answer(
        "Каков ваш опыт работы?", reply_markup=kb_experience
    )
    await state.set_state(Questionnaire.experience)
    await callback.answer()


# Шаг 2: Обработка опыта
@dp.callback_query(Questionnaire.experience, F.data.startswith("exp_"))
async def process_experience(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()  # Удаляем вопрос "Каков ваш опыт"

    chosen_exp = callback.data.split("_")[1]
    await state.update_data(experience=chosen_exp)

    await callback.message.answer(
        "Сколько времени вы уделяете работе?", reply_markup=kb_time
    )
    await state.set_state(Questionnaire.time)
    await callback.answer()


# Шаг 3: Вывод анкеты
@dp.callback_query(Questionnaire.time, F.data.startswith("tm_"))
async def process_time(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()  # Удаляем вопрос "Сколько времени"

    chosen_time = callback.data.split("_")[1]
    await state.update_data(time=chosen_time)

    user_data = await state.get_data()
    summary_text = (
        f"Ваша заявка выглядит так:\n"
        f"{user_data['source']}\n"
        f"{user_data['experience']}\n"
        f"{user_data['time']}\n\n"
        f"Отправить?"
    )

    await callback.message.answer(summary_text, reply_markup=kb_confirm)
    await state.set_state(Questionnaire.confirm)
    await callback.answer()


# Шаг 4: Если нажали "Заново"
@dp.callback_query(Questionnaire.confirm, F.data == "final_restart")
async def process_restart(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()  # Удаляем сообщение с проверкой анкеты
    await state.clear()

    await callback.message.answer(
        "Откуда Вы узнали о нас?", reply_markup=kb_source
    )
    await state.set_state(Questionnaire.source)
    await callback.answer()


# Шаг 4: Если нажали "Отправить"
@dp.callback_query(Questionnaire.confirm, F.data == "final_send")
async def process_send(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()  # Удаляем сообщение с проверкой анкеты
    await state.clear()

    # Отправляем уведомление
    status_msg = await callback.message.answer(
        "Ваша заявка отправлена администрации!"
    )
    await callback.answer()

    # Ждем 9 секунд
    await asyncio.sleep(9)

    # Удаляем уведомление об отправке, чтобы чат остался чистым перед меню
    try:
        await status_msg.delete()
    except Exception:
        pass

    # Отправка Главного меню с фото и 4 кнопками
    photo_path = get_photo_path()
    if photo_path:
        photo = FSInputFile(photo_path)
        await callback.message.answer_photo(
            photo, caption="Главное меню:", reply_markup=kb_main_menu
        )
    else:
        await callback.message.answer(
            "Главное меню:\n(Фото huy.PNG не найдено)", reply_markup=kb_main_menu
        )


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
