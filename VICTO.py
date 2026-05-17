import urllib.request
import urllib.parse
import json
import time

TOKEN = "8838979890:AAE1cglbrlgwqd8g6xzI9zBZzb7QW51bBnI"
URL = f"https://api.telegram.org/bot{TOKEN}/"

# ==================================================
# ВОПРОСЫ
# ==================================================

quiz = {
    "Математика": [
        {"question": "7 × 8 = ?", "options": ["54", "56", "64", "48"], "answer": "56", "points": 100},
        {"question": "Корень из 81?", "options": ["7", "8", "9", "6"], "answer": "9", "points": 200},
        {"question": "5² = ?", "options": ["10", "15", "20", "25"], "answer": "25", "points": 300},
        {"question": "12 : 3 = ?", "options": ["2", "3", "4", "5"], "answer": "4", "points": 400},
        {"question": "Сколько сторон у треугольника?", "options": ["2", "3", "4", "5"], "answer": "3", "points": 500},
        {"question": "90 + 10 = ?", "options": ["80", "90", "100", "110"], "answer": "100", "points": 600},
    ],

    "Русский": [
        {"question": "Сколько букв в русском алфавите?", "options": ["31", "32", "33", "34"], "answer": "33", "points": 100},
        {"question": "Укажи существительное", "options": ["Бежать", "Красивый", "Стол", "Быстро"], "answer": "Стол", "points": 200},
        {"question": "Антоним слова 'день'", "options": ["Утро", "Свет", "Ночь", "Вечер"], "answer": "Ночь", "points": 300},
        {"question": "Сколько падежей?", "options": ["5", "6", "7", "8"], "answer": "6", "points": 400},
        {"question": "Какое слово — глагол?", "options": ["Играть", "Дом", "Яркий", "Красиво"], "answer": "Играть", "points": 500},
        {"question": "Главный член предложения?", "options": ["Предлог", "Союз", "Подлежащее", "Частица"], "answer": "Подлежащее", "points": 600},
    ],

    "Английский": [
        {"question": "Перевод слова cat", "options": ["Собака", "Кошка", "Мышь", "Птица"], "answer": "Кошка", "points": 100},
        {"question": "Hello =", "options": ["Пока", "Спасибо", "Привет", "Да"], "answer": "Привет", "points": 200},
        {"question": "red =", "options": ["Синий", "Красный", "Белый", "Чёрный"], "answer": "Красный", "points": 300},
        {"question": "I ___ a student", "options": ["am", "is", "are", "be"], "answer": "am", "points": 400},
        {"question": "school =", "options": ["Школа", "Книга", "Дом", "Окно"], "answer": "Школа", "points": 500},
        {"question": "book → мн. число", "options": ["book", "bookes", "books", "books'"], "answer": "books", "points": 600},
    ],

    "История": [
        {"question": "Первый космонавт?", "options": ["Гагарин", "Титов", "Королёв", "Леонов"], "answer": "Гагарин", "points": 100},
        {"question": "ВОВ началась в", "options": ["1939", "1940", "1941", "1945"], "answer": "1941", "points": 200},
        {"question": "Столица Древней Руси", "options": ["Москва", "Киев", "Минск", "Новгород"], "answer": "Киев", "points": 300},
        {"question": "Кто основал СПБ?", "options": ["Пётр I", "Ленин", "Екатерина II", "Иван Грозный"], "answer": "Пётр I", "points": 400},
        {"question": "Первый президент РФ?", "options": ["Путин", "Ельцин", "Медведев", "Горбачёв"], "answer": "Ельцин", "points": 500},
        {"question": "Богатыри были в", "options": ["Руси", "Риме", "Японии", "Греции"], "answer": "Руси", "points": 600},
    ],

    "Физика": [
        {"question": "Единица силы", "options": ["Ватт", "Ньютон", "Вольт", "Ампер"], "answer": "Ньютон", "points": 100},
        {"question": "Прибор температуры", "options": ["Весы", "Термометр", "Линейка", "Амперметр"], "answer": "Термометр", "points": 200},
        {"question": "Что быстрее света?", "options": ["Самолёт", "Звук", "Ничего", "Ракета"], "answer": "Ничего", "points": 300},
        {"question": "Сколько планет?", "options": ["7", "8", "9", "10"], "answer": "8", "points": 400},
        {"question": "Что притягивает к Земле?", "options": ["Ветер", "Гравитация", "Магнит", "Сила"], "answer": "Гравитация", "points": 500},
        {"question": "Единица напряжения", "options": ["Ом", "Ампер", "Вольт", "Ватт"], "answer": "Вольт", "points": 600},
    ],

    "Информатика": [
        {"question": "Главное устройство ПК", "options": ["Мышь", "Монитор", "Процессор", "Клавиатура"], "answer": "Процессор", "points": 100},
        {"question": "Сколько бит в байте?", "options": ["4", "8", "16", "32"], "answer": "8", "points": 200},
        {"question": "Что хранит файлы?", "options": ["Колонки", "Монитор", "Жёсткий диск", "Мышь"], "answer": "Жёсткий диск", "points": 300},
        {"question": "Python это", "options": ["Игра", "Браузер", "Язык программирования", "Сайт"], "answer": "Язык программирования", "points": 400},
        {"question": "Кнопка удаления символа", "options": ["Shift", "Enter", "Backspace", "Alt"], "answer": "Backspace", "points": 500},
        {"question": "Интернет это", "options": ["Монитор", "Программа", "Сеть", "Игра"], "answer": "Сеть", "points": 600},
    ]
}

# ==================================================
# ПОЛЬЗОВАТЕЛИ
# ==================================================

users = {}

# ==================================================
# API
# ==================================================

def api(method, data=None):

    if data:
        data = urllib.parse.urlencode(data).encode()

    req = urllib.request.urlopen(URL + method, data=data)

    return json.loads(req.read().decode())

def send_message(chat_id, text, keyboard=None, inline=None):

    data = {
        "chat_id": chat_id,
        "text": text
    }

    markup = {}

    if keyboard:
        markup["keyboard"] = keyboard
        markup["resize_keyboard"] = True

    if inline:
        markup["inline_keyboard"] = inline

    if markup:
        data["reply_markup"] = json.dumps(markup)

    api("sendMessage", data)

def edit_message(chat_id, message_id, text, inline=None):

    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text
    }

    if inline:
        data["reply_markup"] = json.dumps({
            "inline_keyboard": inline
        })

    api("editMessageText", data)

def answer_callback(callback_id):

    api("answerCallbackQuery", {
        "callback_query_id": callback_id
    })

# ==================================================
# ГЛАВНОЕ МЕНЮ
# ==================================================

main_keyboard = [
    [{"text": "Начать"}],
    [{"text": "Правильные ответы"}],
    [{"text": "Создатель"}],
    [{"text": "Сбросить"}]
]

# ==================================================
# ПОЛЬЗОВАТЕЛЬ
# ==================================================

def init_user(user_id):

    if user_id not in users:

        users[user_id] = {
            "stage": None,
            "teams_count": 0,
            "team_names": [],
            "scores": {},
            "solved": {},
            "current_team": None,
            "current_subject": None,
            "current_question": None
        }

# ==================================================
# INLINE КНОПКИ
# ==================================================

def teams_inline(user_id):

    buttons = []

    for team in users[user_id]["team_names"]:

        score = users[user_id]["scores"][team]

        buttons.append([
            {
                "text": f"{team} ({score})",
                "callback_data": f"team|{team}"
            }
        ])

    return buttons

def subjects_inline():

    buttons = []

    for subject in quiz.keys():

        buttons.append([
            {
                "text": subject,
                "callback_data": f"subject|{subject}"
            }
        ])

    return buttons

def question_points_inline(user_id, subject):

    buttons = []

    solved = users[user_id]["solved"]

    if subject not in solved:
        solved[subject] = []

    for i, q in enumerate(quiz[subject]):

        if i not in solved[subject]:

            buttons.append([
                {
                    "text": f"{q['points']}",
                    "callback_data": f"pick|{subject}|{i}"
                }
            ])

    return buttons

def answers_inline():

    buttons = []

    for subject in quiz.keys():

        buttons.append([
            {
                "text": subject,
                "callback_data": f"answers|{subject}"
            }
        ])

    return buttons

# ==================================================
# ОСНОВНОЙ ЦИКЛ
# ==================================================

offset = 0

while True:

    updates = api("getUpdates", {
        "offset": offset + 1,
        "timeout": 30
    })

    for update in updates["result"]:

        offset = update["update_id"]

        # ==================================================
        # CALLBACK
        # ==================================================

        if "callback_query" in update:

            call = update["callback_query"]

            data = call["data"]

            chat_id = call["message"]["chat"]["id"]

            message_id = call["message"]["message_id"]

            callback_id = call["id"]

            init_user(chat_id)

            parts = data.split("|")

            # ---------------- КОМАНДА ----------------

            if parts[0] == "team":

                team = parts[1]

                users[chat_id]["current_team"] = team

                edit_message(
                    chat_id,
                    message_id,
                    f"Команда: {team}\n\nВыберите предмет:",
                    subjects_inline()
                )

                answer_callback(callback_id)

            # ---------------- ПРЕДМЕТ ----------------

            elif parts[0] == "subject":

                subject = parts[1]

                edit_message(
                    chat_id,
                    message_id,
                    f"Предмет: {subject}\n\nВыберите стоимость вопроса:",
                    question_points_inline(chat_id, subject)
                )

                answer_callback(callback_id)

            # ---------------- ВОПРОС ----------------

            elif parts[0] == "pick":

                subject = parts[1]

                q_index = int(parts[2])

                users[chat_id]["current_subject"] = subject

                users[chat_id]["current_question"] = q_index

                q = quiz[subject][q_index]

                buttons = []

                for ans in q["options"]:

                    buttons.append([
                        {
                            "text": ans,
                            "callback_data": f"answer|{ans}"
                        }
                    ])

                text = (
                    f"Команда: {users[chat_id]['current_team']}\n"
                    f"Предмет: {subject}\n"
                    f"Стоимость: {q['points']}\n\n"
                    f"{q['question']}"
                )

                edit_message(
                    chat_id,
                    message_id,
                    text,
                    buttons
                )

                answer_callback(callback_id)

            # ---------------- ОТВЕТ ----------------

            elif parts[0] == "answer":

                user_answer = parts[1]

                subject = users[chat_id]["current_subject"]

                q_index = users[chat_id]["current_question"]

                q = quiz[subject][q_index]

                correct = q["answer"]

                points = q["points"]

                if user_answer == correct:

                    if subject not in users[chat_id]["solved"]:
                        users[chat_id]["solved"][subject] = []

                    users[chat_id]["solved"][subject].append(q_index)

                    team = users[chat_id]["current_team"]

                    users[chat_id]["scores"][team] += points

                    result_text = (
                        f"Верно!\n\n"
                        f"+{points} очков команде {team}\n"
                        f"Текущий счёт: {users[chat_id]['scores'][team]}"
                    )

                else:

                    result_text = (
                        f"Неверно.\n\n"
                        f"Правильный ответ: {correct}"
                    )

                score_text = "\n\nСчёт команд:\n"

                for t in users[chat_id]["team_names"]:
                    score_text += f"• {t}: {users[chat_id]['scores'][t]}\n"

                text = (
                    result_text +
                    score_text +
                    "\nВыберите следующую команду:"
                )

                edit_message(
                    chat_id,
                    message_id,
                    text,
                    teams_inline(chat_id)
                )

                answer_callback(callback_id)

            # ---------------- ОТВЕТЫ ----------------

            elif parts[0] == "answers":

                subject = parts[1]

                text = f"Ответы — {subject}\n\n"

                for q in quiz[subject]:
                    text += f"{q['points']} — {q['answer']}\n"

                edit_message(
                    chat_id,
                    message_id,
                    text,
                    answers_inline()
                )

                answer_callback(callback_id)

        # ==================================================
        # MESSAGE
        # ==================================================

        elif "message" in update:

            msg = update["message"]

            if "text" not in msg:
                continue

            text = msg["text"]

            chat_id = msg["chat"]["id"]

            init_user(chat_id)

            # ---------------- START ----------------

            if text == "/start":

                send_message(
                    chat_id,
                    "Добро пожаловать в викторину!",
                    keyboard=main_keyboard
                )

            # ---------------- СОЗДАТЕЛЬ ----------------

            elif text == "Создатель":

                send_message(
                    chat_id,
                    "Бота создал Сакевич В. 10Э"
                )

            # ---------------- НАЧАТЬ ----------------

            elif text == "Начать":

                users[chat_id]["stage"] = "teams_count"

                send_message(
                    chat_id,
                    "Введите количество команд:"
                )

            # ---------------- КОЛ-ВО КОМАНД ----------------

            elif users[chat_id]["stage"] == "teams_count":

                if text.isdigit():

                    count = int(text)

                    users[chat_id]["teams_count"] = count

                    users[chat_id]["team_names"] = []

                    users[chat_id]["scores"] = {}

                    users[chat_id]["stage"] = "team_names"

                    send_message(
                        chat_id,
                        "Введите название команды 1:"
                    )

            # ---------------- НАЗВАНИЯ КОМАНД ----------------

            elif users[chat_id]["stage"] == "team_names":

                users[chat_id]["team_names"].append(text)

                users[chat_id]["scores"][text] = 0

                current = len(users[chat_id]["team_names"])

                total = users[chat_id]["teams_count"]

                if current < total:

                    send_message(
                        chat_id,
                        f"Введите название команды {current + 1}:"
                    )

                else:

                    users[chat_id]["stage"] = None

                    send_message(
                        chat_id,
                        "Выберите первую команду:",
                        inline=teams_inline(chat_id)
                    )

            # ---------------- ПРАВИЛЬНЫЕ ОТВЕТЫ ----------------

            elif text == "Правильные ответы":

                send_message(
                    chat_id,
                    "Выберите предмет:",
                    inline=answers_inline()
                )

            # ---------------- СБРОС ----------------

            elif text == "Сбросить":

                users[chat_id]["scores"] = {}

                users[chat_id]["solved"] = {}

                users[chat_id]["team_names"] = []

                users[chat_id]["stage"] = None

                send_message(
                    chat_id,
                    "Все результаты сброшены."
                )

    time.sleep(1)
