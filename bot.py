# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types
from db_src import db_reg

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    db_reg.addUser(({"id": chat_id}))
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonCitySpb = types.KeyboardButton('СПб')
    buttonCityMsc = types.KeyboardButton('Москва')
    keyboard.add(buttonCitySpb, buttonCityMsc)

    bot.send_message(message.chat.id, 'Добро пожаловать! Выбери город!', reply_markup=keyboard)
    bot.register_next_step_handler(message, setInlineKeyboard)

#@bot.message_handler(commands=['event'])
def setInlineKeyboard(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(text = name, callback_data = name) for name in ['Балет','Опера']])
    msg = bot.send_message(message.chat.id, 'Что выбираешь?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, eventName)

@bot.callback_query_handler(func=lambda call: True )
def eventName(call):
    if call.data == "Балет":
        bot.send_message(call.message.chat.id, text='Выбран балет')
    elif call.data=="Опера":
        bot.send_message(call.message.chat.id, text='Выбран опера')

    '''
    if m.text == 'Балет':
        bot.send_message(m.chat.id, 'Выбран балет')
    elif m.text == 'Опера':
        bot.send_message(m.chat.id, 'Выбрана опера')
    else:
        bot.send_message(m.chat.id, 'Something wrong')
        '''

@bot.message_handler(regexp="СПб|Москва")
def cityReaction(message):
    bot.send_message(message.chat.id, 'Поправки в поиск внесены!')
    if message.text == 'СПб':
        db_reg.addCityToUser(message.chat.id, 'spb')
    elif message.text == 'Москва':
        db_reg.addCityToUser(message.chat.id, 'msk')
    bot.send_message(message.chat.id, message)

'''
def start(m):
    bot.send_message(m.chat.id, 'Кого выбираешь?',
        reply_markup=keyboard)
    bot.send_message(m.chat.id, 'Отличный выбор')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def start_dialog(message):
    start(message)
'''

if __name__ == '__main__':
    bot.polling(none_stop=True)

