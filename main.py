import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot import types

# Установите ваш токен от BotFather
TOKEN = ''
bot = telebot.TeleBot(TOKEN)

# Список вопросов и вариантов ответов
questions = [
    ("Сколько раз Юрий Гагарин облетел земной шар?", ["1", "2","3"]),

    ("Кто первым вышел из корабля в открытый космос?", ["Алексей Леонов", "Юрий Гагарин","Нил Армстронг"]),

    ("Как называется наука, которая изучает Вселенную?", ["Астрономия", "География","Физика","Информатика"]),

    ("Что больше по размеру — Вселенная или Галактика?", ["Вселенная", "Галактика"]),

    ("Как называется камень, если он прилетел на планету из космоса?", ["Метеорит", "Комета","Камень","Звезда"]),

    ("Может ли звезда с неба упасть на ладонь?", ["Нет", "Да"]),

    ("Какую форму имеет планета Земля?", ["Геоид", "Эллипсоид", "Шар"]),

    ("Как называется наша галактика?", ["Млечный путь", "Андромеда", "Туманность Ориона"]),

    ("Сколько планет в нашей Солнечной системе?", ["8", "9", "7"]),

    ("Какая планета самая большая?", ["Юпитер", "Сатурн", "Земля"]),

    ("Какая планета самая близкая к Солнцу?", ["Меркурий", "Венера", "Марс"]),

    ("Как называется самый большой спутник Юпитера?", ["Ганимед", "Европа", "Ио"]),

    ("Какое количество планет в Солнечной системе не имеет атмосферы?", ["1", "3", "2"]),

    ("Какая планета самая горячая?", ["Венера", "Меркурий", "Марс"]),

    ("Как называется планета с кольцами?", ["Сатурн", "Юпитер", "Уран"]),

    ("Какая планета самая удаленная от Солнца?", ["Нептун", "Плутон", "Уран"]),

    ("Кто был первым человеком на Луне?", ["Нил Армстронг", "Юрий Гагарин", "Баз Олдрин"]),

    ("Сколько времени Гагарин провёл в космосе?", ["1,8 Часов", "2 Часа","38 минут"]),
]

# Словарь для отслеживания состояния пользователей
user_state = {}

# Функция для отправки вопросов и обработки ответов
def send_question(chat_id, question_num):
    if question_num < len(questions):
        question, options = questions[question_num]
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for option in options:
            markup.add(KeyboardButton(option))

        bot.send_message(chat_id, question, reply_markup=markup)
        user_state[chat_id] = {'question_num': question_num, 'answered': False}
    else:
        bot.send_message(chat_id, "Вы ответили на все вопросы! Спасибо за участие.")
        del user_state[chat_id]

# Обработка сообщений от пользователей
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который задаст тебе вопросы о космосе.")
    send_question(message.chat.id, 0)

@bot.message_handler(func=lambda message: message.chat.id in user_state and not user_state[message.chat.id]['answered'])
def handle_answer(message):
    chat_id = message.chat.id
    question_num = user_state[chat_id]['question_num']

    # Проверяем правильность ответа
    correct_answer = questions[question_num][1][0]
    if message.text == correct_answer:
        bot.send_message(chat_id, "Правильный ответ!")
    else:
        bot.send_message(chat_id, f"Неправильный ответ. Правильный ответ: {correct_answer}")

    # Переходим к следующему вопросу
    user_state[chat_id]['answered'] = True
    send_question(chat_id, question_num + 1)

# Обработка случая, если пользователь случайно отправит что-то не из списка вариантов
@bot.message_handler(func=lambda message: message.chat.id in user_state and message.text not in [btn.text for btn in message.reply_markup.keyboard[0]])
def handle_invalid(message):
    bot.send_message(message.chat.id, "Пожалуйста, выберите один из предложенных вариантов.")

bot.polling()
