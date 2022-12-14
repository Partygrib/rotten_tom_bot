import telebot
from bs4 import BeautifulSoup
import requests
from telebot import types

# 5617127293:AAFNjtGv6hQfj4ohxJV3sOQLAXr9gEJeqjg

search = 'https://www.rottentomatoes.com/search?search='

def search_film(name):
    page = requests.get(search + name)
    print(page.status_code)
    soup = BeautifulSoup(page.text, "html.parser")
    onlyMoves = soup.find('search-page-result', type="movie")
    scraped = []

    if onlyMoves is None:
        scraped.append(['er', 'er', 'er', 'er'])
    else:
        movies = onlyMoves.findAll('search-page-media-row')
        for move in movies:
            year = move['releaseyear']
            link = move.a['href']
            names = move.findAll('a', class_='unset')
            cast = move['cast']
            scraped.append([names[1].text.strip(), year, link, cast])

    return scraped


# bot
bot = telebot.TeleBot("5617127293:AAFNjtGv6hQfj4ohxJV3sOQLAXr9gEJeqjg")


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/search':
        bot.send_message(message.from_user.id, "Какой фильм ты ищешь?")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, 'Напиши /search')


def get_name(message):
    global film
    film = search_film(message.text)

    if not film or film[0][0] == 'er':
        bot.send_message(message.from_user.id, 'Такого фильма не существует, попробуйте еще раз')
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, 'Выбери нужный фильм')
        get_var_names(message)


def get_var_names(message):
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура

    if len(film) < 5 and len(film) != 0:
        key1 = types.InlineKeyboardButton(text=film[0][0] + ' - ' + film[0][1], callback_data='1')
        keyboard.add(key1)
        question = 'Какой фильм?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    else:
        key1 = types.InlineKeyboardButton(text=film[0][0] + ' - ' + film[0][1], callback_data='1')
        keyboard.add(key1)
        key2 = types.InlineKeyboardButton(text=film[1][0] + ' - ' + film[1][1], callback_data='2')
        keyboard.add(key2)
        key3 = types.InlineKeyboardButton(text=film[2][0] + ' - ' + film[2][1], callback_data='3')
        keyboard.add(key3)
        key4 = types.InlineKeyboardButton(text=film[3][0] + ' - ' + film[3][1], callback_data='4')
        keyboard.add(key4)
        key5 = types.InlineKeyboardButton(text=film[4][0] + ' - ' + film[4][1], callback_data='5')
        keyboard.add(key5)
        question = 'Какой фильм?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


def get_prom(message):

    keyboard2 = types.InlineKeyboardMarkup()  # наша клавиатура
    key1 = types.InlineKeyboardButton(text='Выборочная информация', callback_data='14')
    keyboard2.add(key1)
    key2 = types.InlineKeyboardButton(text='Полная информация', callback_data='15')
    keyboard2.add(key2)
    key3 = types.InlineKeyboardButton(text='Назад к выбору фильма', callback_data='16')
    keyboard2.add(key3)
    key4 = types.InlineKeyboardButton(text='Поиск нового фильма', callback_data='17')
    keyboard2.add(key4)
    question = 'Что ты хочешь узнать об этом фильме?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard2)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global cor_film
    if call.data == "1":
        cor_film = film[0][2]
        bot.send_message(call.message.chat.id, film[0][2])
        bot.register_next_step_handler(call.message, get_prom)
        bot.send_message(call.message.chat.id, 'Чтобы перейти в следующее меню напиши любое сообщение :)')
    elif call.data == "2":
        bot.send_message(call.message.chat.id, film[1][2])
        cor_film = film[1][2]
        bot.register_next_step_handler(call.message, get_prom)
        bot.send_message(call.message.chat.id, 'Чтобы перейти в следующее меню напиши любое сообщение :)')
    elif call.data == "3":
        bot.send_message(call.message.chat.id, film[2][2])
        cor_film = film[2][2]
        bot.register_next_step_handler(call.message, get_prom)
        bot.send_message(call.message.chat.id, 'Чтобы перейти в следующее меню напиши любое сообщение :)')
    elif call.data == "4":
        bot.send_message(call.message.chat.id, film[3][2])
        cor_film = film[3][2]
        bot.register_next_step_handler(call.message, get_prom)
        bot.send_message(call.message.chat.id, 'Чтобы перейти в следующее меню напиши любое сообщение :)')
    elif call.data == "5":
        bot.send_message(call.message.chat.id, film[4][2])
        cor_film = film[4][2]
        bot.register_next_step_handler(call.message, get_prom)
        bot.send_message(call.message.chat.id, 'Чтобы перейти в следующее меню напиши любое сообщение :)')
    elif call.data == "16":
        bot.register_next_step_handler(call.message, get_var_names)
        bot.send_message(call.message.chat.id, 'Чтобы вернуться в предыдущее меню напиши любое сообщение :)')
    elif call.data == "17":
        bot.register_next_step_handler(call.message, get_name)
        bot.send_message(call.message.chat.id, 'Какой фильм ты ищешь?')


bot.polling()