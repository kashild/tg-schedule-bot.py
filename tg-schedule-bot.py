#добавляю нужные библеотеки
import telebot
from telebot import types
import json

TOKEN =  your_token_here

bot = telebot.TeleBot(TOKEN)

commands = [
    'ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ',
    '5', '6', '7', '8', '9', '10', '11',
    'А', 'Б', 'В', 'Г', 'Д',
    '/start', '/help',
    'Узнать расписание'
            ]

#руководство по использованию ботом для пользователя
@bot.message_handler(commands=['start', 'help'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Узнать расписание')
    markup.add(btn1)
    text = 'Привет, что бы начать пользоваться ботом нажми "Узнать расписание"'
    bot.send_message(message.chat.id, text.format(message.from_user), reply_markup=markup)


#'условия' словарь через который проверяются возвращающиеся значения из бота: день класс и номер класса
conditions = {
    'day' : ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ'],
    'class' : ['5', '6', '7', '8', '9', '10', '11'],
    'number' : ['А', 'Б', 'В', 'Г', 'Д']
    }

#функция для загрузки данных из JSON файла(файл с расписанием)
def load_schedule():
    with open('schedule.json', 'r', encoding='utf-8') as file:
        return json.load(file)

# Загрузка данных(файл с расписанием)
SCHEDULE = load_schedule()

#словарь для сохранения данных вернувшихся от бота
day_class_number = {
    'day' : '',
    'class' : '',
    'number' : ''
}

#Три последущие функции нужны для создания URL кнопок на каждом этапе: 1-выбрать день. 2-выбрать класс. 3-выбрать номер класса
@bot.message_handler(regexp='keyboard1')
def keyboard1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('ПН')
    btn2 = types.KeyboardButton('ВТ')
    btn3 = types.KeyboardButton('СР')
    btn4 = types.KeyboardButton('ЧТ')
    btn5 = types.KeyboardButton('ПТ')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    text = 'Расписание на какой день вы хотите узнать? '
    bot.send_message(message.chat.id, text.format(message.from_user), reply_markup=markup)


@bot.message_handler(regexp='keyboard2')
def keyboard2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('5')
    btn2 = types.KeyboardButton('6')
    btn3 = types.KeyboardButton('7')
    btn4 = types.KeyboardButton('8')
    btn5 = types.KeyboardButton('9')
    btn6 = types.KeyboardButton('10')
    btn7 = types.KeyboardButton('11')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    text = 'Расписание для какого класса вы хотите узнать? '
    bot.send_message(message.chat.id, text.format(message.from_user), reply_markup=markup)

@bot.message_handler(regexp='keyboard3')
def keyboard3(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('А')
    btn2 = types.KeyboardButton('Б')
    btn3 = types.KeyboardButton('В')
    btn4 = types.KeyboardButton('Г')
    btn5 = types.KeyboardButton('Д')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    text = 'Номер какого класса вам нужен? '
    bot.send_message(message.chat.id, text.format(message.from_user), reply_markup=markup)

#функция, которая проверяет входящее сообщение и если оно является ключом в словаре "conditions" записывает его в словарь "day_class_number"
def check(message):
    if message in conditions['day']:
        day_class_number['day'] = message
    elif message in conditions['class']:
        day_class_number['class'] = message
    elif message in conditions['number']:
        day_class_number['number'] = message

# #функция, которая принимает, сохраняет значения для словаря "day_class_number" и выводит конечный результат
@bot.message_handler(content_types=['text'])
def schedule(message):
    if message.text == 'Узнать расписание':
        keyboard1(message)
    check(message.text)
    if message.text in conditions['day']:
        keyboard2(message)
    check(message.text)
    if message.text in conditions['class']:
        keyboard3(message)
    check(message.text)
    if len(day_class_number['number']) != 0:
        #сокращаю для читаемости кода и что бы легче было ипссользовать как индексы
        x = day_class_number['day'] #day
        y = day_class_number['class'] #class
        z = day_class_number['number']  # number
        text = SCHEDULE[x][y][z]
        bot.send_message(message.chat.id, text)
        day_class_number['day'] = ''
        day_class_number['class'] = ''
        day_class_number['number'] = ''
        start(message)
    if message.text not in commands:
        bot.send_message(message.chat.id, 'Неправильная команда. Пожалуйста, введите /help для начала.')
        start(message)



bot.polling(non_stop=True)