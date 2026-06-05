import asyncio
from datetime import datetime
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

# Временная "база данных" для хранения даты регистрации пользователей (ID: datetime)
user_registration_dates = {}


# --- ФУНКЦИЯ ДЛЯ ПОИСКА ФОТО ---
def get_photo_path(filename: str):
    # Универсальный поиск файлов (huy.PNG, Nap.PNG, Pro.PNG, Set.PNG)
    possible_paths = [
        BASE_DIR / "Folder" / filename,
        BASE_DIR / "data" / filename,
        BASE_DIR / filename,
        Path(f"/app/Folder/{filename}"),
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

kb_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отправить", callback_data="start_anketa")]
    ]
)

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

kb_confirm = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отправить", callback_data="final_send"),
            InlineKeyboardButton(text="Заново", callback_data="final_restart"),
        ]
    ]
)

# Главное меню (по 2 в строку)
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

# Кнопки раздела "Направления" (по 1 в строку)
kb_directions = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Fake Н@рко", callback_data="dir_fake_narko")],
        [InlineKeyboardButton(text="iCloud", callback_data="dir_icloud")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_menu")],
    ]
)

# Кнопки подраздела "Fake Н@рко" (по 1 в строку)
kb_fake_narko = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать сеть", callback_data="fn_select_net")],
        [InlineKeyboardButton(text="Создать зеркало", callback_data="fn_mirror")],
        [InlineKeyboardButton(text="Назад", callback_data="menu_direct")],
    ]
)

# Кнопка Назад для Профиля
kb_back_only = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_to_menu")]
    ]
)

# Кнопки раздела "Настройки" (по 1 в строку)
kb_settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ранги", callback_data="set_ranks")],
        [InlineKeyboardButton(text="Выплаты", callback_data="set_payouts")],
        [InlineKeyboardButton(text="Режим", callback_data="set_mode")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_menu")],
    ]
)

# Кнопка Назад для Рангов (возвращает в Настройки)
kb_back_to_settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="menu_settings")]
    ]
)


# --- ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ ВЫЗОВА ГЛАВНОГО МЕНЮ ---
async def send_main_menu(message: types.Message):
    photo_path = get_photo_path("MM.png")
    if photo_path:
        photo = FSInputFile(photo_path)
        await message.answer_photo(
            photo, caption="Главное меню:", reply_markup=kb_main_menu
        )
    else:
        await message.answer(
            "Главное меню:\n(Фото huy.PNG не найдено)", reply_markup=kb_main_menu
        )


# --- ХЕНДЛЕРЫ АНКЕТЫ ---


@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()

    # Фиксируем дату регистрации, если пользователя еще нет в нашей "базе"
    if message.from_user.id not in user_registration_dates:
        user_registration_dates[message.from_user.id] = datetime.now()

    photo_path = get_photo_path("huy.jpeg")
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


@dp.callback_query(F.data == "start_anketa")
async def start_questionnaire(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        "Откуда Вы узнали о нас?", reply_markup=kb_source
    )
    await state.set_state(Questionnaire.source)
    await callback.answer()


@dp.callback_query(Questionnaire.source, F.data.startswith("src_"))
async def process_source(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    chosen_source = callback.data.split("_")[1]
    await state.update_data(source=chosen_source)
    await callback.message.answer(
        "Каков ваш опыт работы?", reply_markup=kb_experience
    )
    await state.set_state(Questionnaire.experience)
    await callback.answer()


@dp.callback_query(Questionnaire.experience, F.data.startswith("exp_"))
async def process_experience(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    chosen_exp = callback.data.split("_")[1]
    await state.update_data(experience=chosen_exp)
    await callback.message.answer(
        "Сколько времени вы уделяете работе?", reply_markup=kb_time
    )
    await state.set_state(Questionnaire.time)
    await callback.answer()


@dp.callback_query(Questionnaire.time, F.data.startswith("tm_"))
async def process_time(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
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


@dp.callback_query(Questionnaire.confirm, F.data == "final_restart")
async def process_restart(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer(
        "Откуда Вы узнали о нас?", reply_markup=kb_source
    )
    await state.set_state(Questionnaire.source)
    await callback.answer()


@dp.callback_query(Questionnaire.confirm, F.data == "final_send")
async def process_send(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()

    status_msg = await callback.message.answer(
        "Ваша заявка отправлена администрации!"
    )
    await callback.answer()

    await asyncio.sleep(9)

    try:
        await status_msg.delete()
    except Exception:
        pass

    await send_main_menu(callback.message)


# --- ХЕНДЛЕРЫ ГЛАВНОГО МЕНЮ И НАВИГАЦИИ ---

# Возврат в главное меню по кнопке Назад
@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    await send_main_menu(callback.message)
    await callback.answer()


# 1. Раздел Направления
@dp.callback_query(F.data == "menu_direct")
async def menu_directions(callback: types.CallbackQuery):
    await callback.message.delete()
    photo_path = get_photo_path("Nap.png")
    text = "Сейчас доступны 2 направления:"

    if photo_path:
        await callback.message.answer_photo(
            FSInputFile(photo_path), caption=text, reply_markup=kb_directions
        )
    else:
        await callback.message.answer(
            f"❌ Фото Nap.PNG не найдено\n\n{text}", reply_markup=kb_directions
        )
    await callback.answer()


# Подраздел Fake Н@рко
@dp.callback_query(F.data == "dir_fake_narko")
async def direction_fake_narko(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        'Мануал к данному направлению находится в разделе "О проекте"',
        reply_markup=kb_fake_narko,
    )
    await callback.answer()


# Заглушка для iCloud (при желании можно расширить)
@dp.callback_query(F.data == "dir_icloud")
async def direction_icloud(callback: types.CallbackQuery):
    await callback.answer("Направление iCloud в разработке", show_alert=True)


# Заглушки для кнопок внутри Fake Н@рко
@dp.callback_query(F.data.in_({"fn_select_net", "fn_mirror"}))
async def fake_narko_actions(callback: types.CallbackQuery):
    await callback.answer("В разработке...", show_alert=True)


# 2. Раздел Профиль
@dp.callback_query(F.data == "menu_profile")
async def menu_profile(callback: types.CallbackQuery):
    await callback.message.delete()

    # Получаем юзернейм или имя пользователя
    username = callback.from_user.username
    user_tag = f"@{username}" if username else callback.from_user.full_name

    # Считаем разницу дней с момента регистрации
    reg_date = user_registration_dates.get(
        callback.from_user.id, datetime.now()
    )
    days_in_team = (datetime.now() - reg_date).days

    profile_text = (
        f"Твой профиль\n\n"
        f"Статистика:\n"
        f" ┠ Твоя касса: 0 $\n"
        f" ┠ Кол-во профитов: 0 профитов\n"
        f" ┠ Место в топе: N/A\n\n"
        f"Информация и текущие настройки\n"
        f" ├ Тег в профитах: {user_tag}\n"
        f" ├ Статус: Воркер\n"
        f" ├ Ранг: 🎓 Студент\n\n"
        f"В команде: {days_in_team} дн."
    )

    photo_path = get_photo_path("Pro.png")
    if photo_path:
        await callback.message.answer_photo(
            FSInputFile(photo_path),
            caption=profile_text,
            reply_markup=kb_back_only,
        )
    else:
        await callback.message.answer(
            f"❌ Фото Pro.PNG не найдено\n\n{profile_text}",
            reply_markup=kb_back_only,
        )
    await callback.answer()


# 3. Раздел Настройки
@dp.callback_query(F.data == "menu_settings")
async def menu_settings(callback: types.CallbackQuery):
    await callback.message.delete()
    photo_path = get_photo_path("Set.PNG")
    text = "Это настройки, тут разбирайся сам"

    if photo_path:
        await callback.message.answer_photo(
            FSInputFile(photo_path), caption=text, reply_markup=kb_settings
        )
    else:
        await callback.message.answer(
            f"❌ Фото Set.PNG не найдено\n\n{text}", reply_markup=kb_settings
        )
    await callback.answer()


# Подраздел Настройки -> Ранги
@dp.callback_query(F.data == "set_ranks")
async def settings_ranks(callback: types.CallbackQuery):
    await callback.message.delete()
    ranks_text = (
        "Твоя касса: 0$\n\n"
        "Студент — от 0$\n"
        "Чемпион — от 1 000$\n"
        "Волк — от 3 000$\n"
        "Легенда — от 5 000$\n"
        "Босс — от 10 000$"
    )
    await callback.message.answer(ranks_text, reply_markup=kb_back_to_settings)
    await callback.answer()


# Заглушки для Выплат и Режима
@dp.callback_query(F.data.in_({"set_payouts", "set_mode"}))
async def settings_stubs(callback: types.CallbackQuery):
    await callback.answer("В разработке...", show_alert=True)


# 4. Раздел О проекте
@dp.callback_query(F.data == "menu_about")
async def menu_about(callback: types.CallbackQuery):
    await callback.message.delete()
    about_text = (
        "ℹ️ ИНФОРМАЦИЯ О ПРОЕКТЕ UDD TEAM\n\n"
        "🚀 Мы работаем с 01.03.2026, за это время сделаны 92 профитов на сумму 6,264 $\n\n"
        "💸 Выплаты\n"
        "┠ Прямой перевод - 85%\n"
        "┖ Сервисы - 75%\n\n"
        "⚡️ Состояние работы бота:\n"
        "Ворк"
    )

    photo_path = get_photo_path("huy.jpeg")  # Ищем картинку в папке проекта

    if photo_path:
        await callback.message.answer_photo(
            FSInputFile(photo_path), caption=about_text, reply_markup=kb_back_only
        )
    else:
        await callback.message.answer(
            f"❌ Фото для раздела 'О проекте' не найдено\n\n{about_text}",
            reply_markup=kb_back_only,
        )
    await callback.answer()


# --- ЗАПУСК БОТА ---
async def main():
    print("Бот успешно запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
