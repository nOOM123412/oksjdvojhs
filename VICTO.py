import urllib.request
import urllib.parse
import json
import time

TOKEN = "8838979890:AAE1cglbrlgwqd8g6xzI9zBZzb7QW51bBnI"
URL = f"https://api.telegram.org/bot{TOKEN}/"

quiz = {
    "Математика": [
        ("7 × 8 = ?", ["54", "56", "64", "48"], "56"),
        ("Корень из 81?", ["7", "8", "9", "6"], "9"),
        ("5² = ?", ["10", "15", "20", "25"], "25"),
        ("12 : 3 = ?", ["2", "3", "4", "5"], "4"),
        ("Сколько сторон у треугольника?", ["2", "3", "4", "5"], "3"),
        ("90 + 10 = ?", ["80", "90", "100", "110"], "100"),
    ],

    "Русский": [
        ("Сколько букв в русском алфавите?", ["31", "32", "33", "34"], "33"),
        ("Укажи существительное", ["Бежать", "Красивый", "Стол", "Быстро"], "Стол"),
        ("Антоним слова 'день'", ["Утро", "Свет", "Ночь", "Вечер"], "Ночь"),
        ("Сколько падежей?", ["5", "6", "7", "8"], "6"),
        ("Какое слово — глагол?", ["Играть", "Дом", "Яркий", "Красиво"], "Играть"),
        ("Главный член предложения?", ["Предлог", "Союз", "Подлежащее", "Частица"], "Подлежащее"),
    ],

    "Английский": [
        ("Перевод слова cat", ["Собака", "Кошка", "Мышь", "Птица"], "Кошка"),
        ("Hello =", ["Пока", "Спасибо", "Привет", "Да"], "Привет"),
        ("red =", ["Синий", "Красный", "Белый", "Чёрный"], "Красный"),
        ("I ___ a student", ["am", "is", "are", "be"], "am"),
        ("school =", ["Школа", "Книга", "Дом", "Окно"], "Школа"),
        ("book → мн. число", ["book", "bookes", "books", "books'"], "books"),
    ],

    "История": [
        ("Первый космонавт?", ["Гагарин", "Титов", "Королёв", "Леонов"], "Гагарин"),
        ("ВОВ началась в", ["1939", "1940", "1941", "1945"], "1941"),
        ("Столица Древней Руси", ["Москва", "Киев", "Минск", "Новгород"], "Киев"),
        ("Кто основал СПБ?", ["Пётр I", "Ленин", "Екатерина II", "Иван Грозный"], "Пётр I"),
        ("Первый президент РФ?", ["Путин", "Ельцин", "Медведев", "Горбачёв"], "Ельцин"),
        ("Богатыри были в", ["Руси", "Риме", "Японии", "Греции"], "Руси"),
    ],

    "Физика": [
        ("Единица силы", ["Ватт", "Ньютон", "Вольт", "Ампер"], "Ньютон"),
        ("Прибор температуры", ["Весы", "Термометр", "Линейка", "Амперметр"], "Термометр"),
        ("Что быстрее света?", ["Самолёт", "Звук", "Ничего", "Ракета"], "Ничего"),
        ("Сколько планет?", ["7", "8", "9", "10"], "8"),
        ("Что притягивает к Земле?", ["Ветер", "Гравитация", "Магнит", "Сила"], "Гравитация"),
        ("Единица напряжения", ["Ом", "Ампер", "Вольт", "Ватт"], "Вольт"),
    ],

    "Информатика": [
        ("Главное устройство ПК", ["Мышь", "Монитор", "Процессор", "Клавиатура"], "Процессор"),
        ("Сколько бит в байте?", ["4", "8", "16", "32"], "8"),
        ("Что хранит файлы?", ["Колонки", "Монитор", "Жёсткий диск", "Мышь"], "Жёсткий диск"),
        ("Python это", ["Игра", "Браузер", "Язык программирования", "Сайт"], "Язык программирования"),
        ("Кнопка удаления символа", ["Shift", "Enter", "Backspace", "Alt"], "Backspace"),
        ("Интернет это", ["Монитор", "Программа", "Сеть", "Игра"], "Сеть"),
    ]
}


users = {}

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

def answer_callback(callback_id, text=""):
    api("answerCallbackQuery", {
        "callback_query_id": callback_id,
        "text": text
    })


main_keyboard = [
    [{"text": "Начать"}],
    [{"text": "Правильные ответы"}],
    [{"text": "Создатель"}],
    [{"text": "Сбросить"}],
]

def init_user(user_id):

    if user_id not in users:

        users[user_id] = {
            "stage": None,
            "teams_count": 0,
            "team_names": [],
            "scores": {},
            "current_team": None,
            "solved": {},
            "current_question": None
        }

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


def get_question(user_id, subject):

    solved = users[user_id]["solved"]

    if subject not in solved:
        solved[subject] = []

    for i, q in enumerate(quiz[subject]):

        if i not in solved[subject]:
            return i, q

    return None, None

offset = 0

while True:

    updates = api("getUpdates", {
        "offset": offset + 1,
        "timeout": 30
    })

    for update in updates["result"]:

        offset = update["update_id"]

        # ================= CALLBACK =================

        if "callback_query" in update:

            call = update["callback_query"]

            data = call["data"]
            chat_id = call["message"]["chat"]["id"]
            message_id = call["message"]["message_id"]

            callback_id = call["id"]

            init_user(chat_id)

            parts = data.split("|")

            # ===== ВЫБОР ПРЕДМЕТА =====

            if parts[0] == "subject":

                subject = parts[1]

                users[chat_id]["current_subject"] = subject

                index, q = get_question(chat_id, subject)

                if q is None:

                    edit_message(
                        chat_id,
                        message_id,
                        "Все вопросы этого предмета решены."
                    )

                else:

                    users[chat_id]["current_question"] = index

                    buttons = []

                    for ans in q[1]:

                        buttons.append([
                            {
                                "text": ans,
                                "callback_data": f"answer|{ans}"
                            }
                        ])

                    text = (
                        f"Команда: {users[chat_id]['current_team']}\n"
                        f"Предмет: {subject}\n\n"
                        f"{q[0]}"
                    )

                    edit_message(
                        chat_id,
                        message_id,
                        text,
                        buttons
                    )

                answer_callback(callback_id)

            # ===== ВЫБОР КОМАНДЫ =====

            elif parts[0] == "team":

                team = parts[1]

                users[chat_id]["current_team"] = team

                edit_message(
                    chat_id,
                    message_id,
                    f"Команда выбрана: {team}\n\nВыберите предмет:",
                    subjects_inline()
                )

                answer_callback(callback_id)

            # ===== ОТВЕТ =====

            elif parts[0] == "answer":

                user_answer = parts[1]

                subject = users[chat_id]["current_subject"]

                index = users[chat_id]["current_question"]

                q = quiz[subject][index]

                correct = q[2]

                if user_answer == correct:

                    users[chat_id]["solved"][subject].append(index)

                    team = users[chat_id]["current_team"]

                    users[chat_id]["scores"][team] += 1

                    text = (
                        "Верно!\n\n"
                        f"Очки команды {team}: "
                        f"{users[chat_id]['scores'][team]}"
                    )

                else:

                    text = (
                        "Неверно.\n\n"
                        f"Правильный ответ: {correct}"
                    )

                edit_message(
                    chat_id,
                    message_id,
                    text,
                    subjects_inline()
                )

                answer_callback(callback_id)

            # ===== ОТВЕТЫ =====

            elif parts[0] == "answers":

                subject = parts[1]

                txt = f"Ответы: {subject}\n\n"

                for i, q in enumerate(quiz[subject], start=1):
                    txt += f"{i}. {q[2]}\n"

                edit_message(
                    chat_id,
                    message_id,
                    txt,
                    answers_inline()
                )

                answer_callback(callback_id)

        # ================= MESSAGE =================

        elif "message" in update:

            msg = update["message"]

            if "text" not in msg:
                continue

            text = msg["text"]
            chat_id = msg["chat"]["id"]

            init_user(chat_id)

            # ===== START =====

            if text == "/start":

                send_message(
                    chat_id,
                    "Добро пожаловать в викторину!",
                    keyboard=main_keyboard
                )

            # ===== СОЗДАТЕЛЬ =====

            elif text == "Создатель":

                send_message(
                    chat_id,
                    "Бота создал Сакевич В. 10Э"
                )

            # ===== НАЧАТЬ =====

            elif text == "Начать":

                users[chat_id]["stage"] = "teams_count"

                send_message(
                    chat_id,
                    "Введите количество команд:"
                )

            # ===== КОЛ-ВО КОМАНД =====

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

            # ===== НАЗВАНИЯ КОМАНД =====

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
                        "Выберите команду:",
                        inline=teams_inline(chat_id)
                    )

            # ===== ПРАВИЛЬНЫЕ ОТВЕТЫ =====

            elif text == "Правильные ответы":

                send_message(
                    chat_id,
                    "Выберите предмет:",
                    inline=answers_inline()
                )

            # ===== СБРОС =====

            elif text == "Сбросить":

                users[chat_id]["scores"] = {}

                users[chat_id]["solved"] = {}

                users[chat_id]["team_names"] = []

                send_message(
                    chat_id,
                    "Все результаты сброшены."
                )

    time.sleep(1)
