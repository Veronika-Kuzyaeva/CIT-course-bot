# -*- coding: utf-8 -*-
import telebot
from telebot import types
import config
from classUser import *

bot = telebot.TeleBot(config.token)
global user

dic = {'ball':'Балы', 'business-events':'Бизнес', 'cinema':'Кино', 'circus':'Цирк',
        'comedy-club':'Comedy club', 'concert':'Концерты', 'dance-trainings':'Танцы',
        'discount':'Скидки', 'education': 'Знания', 'evening' : 'ART-вечер', 'exhibition' : 'Выставки',
        'quest' : 'Квесты', 'party' : 'Вечеринки', 'theater': 'Театр', 'games':'Игры' }

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global user
    user = User(message.chat.id)
    keyboard = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
    buttonCitySpb = types.KeyboardButton('СПб')
    buttonCityMsc = types.KeyboardButton('Москва')
    keyboard.add(buttonCitySpb, buttonCityMsc)
    m=bot.send_message(message.chat.id, 'Добро пожаловать! Выбери город!', reply_markup=keyboard)
    bot.register_next_step_handler(m, cityReaction)


#@bot.message_handler(regexp="СПб|Москва")
def cityReaction(message):
    global user
    keyboard_hider = types.ReplyKeyboardRemove()
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttonNext = types.KeyboardButton('Далее')
    if message.text == 'СПб':
        #добавить в бд + current_city
        user.current_city = 'spb'
        bot.send_message(message.chat.id, 'Вы выбрали '+message.text,reply_markup=keyboard_hider)
        keyboard.add(buttonNext)
        msg = bot.send_message(message.chat.id, 'Поправки в поиск внесены!', reply_markup=keyboard)
        bot.register_next_step_handler(msg, button)
    elif message.text == 'Москва':
        #добавить в бд + current_city
        user.current_city = 'msk'
        bot.send_message(message.chat.id, 'Вы выбрали ' + message.text, reply_markup=keyboard_hider)
        keyboard.add(buttonNext)
        msg = bot.send_message(message.chat.id, 'Поправки в поиск внесены!', reply_markup=keyboard)
        bot.register_next_step_handler(msg, button)
    else:
        msg = bot.send_message(message.chat.id, 'Выберите город')
        bot.register_next_step_handler(msg, cityReaction)



@bot.message_handler(commands=['button'])
def button(message):
    global dic
    keyboard_hider = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Выбор события', reply_markup=keyboard_hider)
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    keyboard.add(*{types.InlineKeyboardButton(text=dic[d], callback_data=d) for d in dic})

    '''
    keyboard.add(*{
                   types.InlineKeyboardButton(text='Мода', callback_data='fashion'),
                   types.InlineKeyboardButton(text='Фестивали', callback_data='festival'),
                   types.InlineKeyboardButton(text='Флешмобы', callback_data='flashmob'),
                   types.InlineKeyboardButton(text='Игры', callback_data='games'),
                   types.InlineKeyboardButton(text='В мире', callback_data='global'),
                   types.InlineKeyboardButton(text='Праздники', callback_data='holiday'),
                   types.InlineKeyboardButton(text='Детское ', callback_data='kids'),
                   types.InlineKeyboardButton(text='КВН', callback_data='kvn'),
                   types.InlineKeyboardButton(text='Магия', callback_data='magic'),
                   types.InlineKeyboardButton(text='Маскарады', callback_data='masquerade'),
                   types.InlineKeyboardButton(text='Встречи', callback_data='meeting'),
                   types.InlineKeyboardButton(text='Ночь', callback_data='night'),
                   types.InlineKeyboardButton(text='Разное', callback_data='other'),
                   types.InlineKeyboardButton(text='Вечеринки', callback_data='party'),
                   # types.InlineKeyboardButton(text='Постоянные выставки', callback_data='permanent-exhibitions'),
                   types.InlineKeyboardButton(text='Фотособытия', callback_data='photo'),
                   types.InlineKeyboardButton(text='Презентации', callback_data='presentation'),
                   types.InlineKeyboardButton(text='Квесты', callback_data='quest'),
                   types.InlineKeyboardButton(text='Романтика', callback_data='romance'),
                   types.InlineKeyboardButton(text='Распродажа', callback_data='sale'),
                   types.InlineKeyboardButton(text='Шопинг', callback_data='shopping'),
                   types.InlineKeyboardButton(text='Шоу', callback_data='show'),
                   # types.InlineKeyboardButton( text='Помощь',callback_data= 'social-activity'),
                   types.InlineKeyboardButton(text='Speed-dating', callback_data='speed-dating'),
                   types.InlineKeyboardButton(text='Спорт', callback_data='sport'),
                   types.InlineKeyboardButton(text='Стендап', callback_data='stand-up'),
                   types.InlineKeyboardButton(text='Акции', callback_data='stock'),
                   types.InlineKeyboardButton(text='Театр', callback_data='theater'),
                   types.InlineKeyboardButton(text='Экскурсии', callback_data='tour'),
                   types.InlineKeyboardButton(text='Ярмарки', callback_data='yarmarki-razvlecheniya-yarmarki'),
                   types.InlineKeyboardButton(text='Йога', callback_data='yoga'),
                   types.InlineKeyboardButton(text='Дни открытых дверей', callback_data='open')})
        '''
    msg=bot.send_message(message.chat.id, 'Что выберите?', reply_markup=keyboard)
    #bot.register_next_step_handler(msg, eventName)


@bot.callback_query_handler(func=lambda call: True )
def eventName(call):
    global user
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    invite = types.KeyboardButton('Популярные события')
    recomm = types.KeyboardButton('Рекомендации')
    backtocity = types.KeyboardButton('Вернуться к выбору города')

    keyboard.add(invite, recomm, backtocity)
    msg = bot.send_message(call.message.chat.id, 'Выберите режим просмотра', reply_markup=keyboard)

    if(call.data in dic):
        print('Mes:' + call.data)
        user.current_event = str(call.data)
        print(user.current_event)
        user.addEventClick(user.current_event)
        bot.register_next_step_handler(call.message, setEvent)
    else: bot.register_next_step_handler(call, eventName)


def setEvent(message):
    global user

    keyboard_hider = types.ReplyKeyboardRemove()
    if  message.text=='Популярные события':
        user.addActDigest()
        m = Next()
        bot.register_next_step_handler(m, InterestKeyboard)

    elif  message.text=='Рекомендации':
        user.addActRecomendation()
        m = Next()
        bot.register_next_step_handler(m, InterestKeyboard)
    elif  message.text=='Back to choose city':
        bot.send_message(message.chat.id,'Выбран back')
        #bot.register_next_step_handler(message, setEvent)


def setMark(message):
    flag = False
    if(message.text != 'Назад, к выбору события'):
        if (message.text == '&#10004 Интересует'):
            flag = True
        elif (message.text == '&#10008 Не интересует'):
            flag = False

        if ((len(user.usersActivity) - 1) == -1):
            bot.send_message(message.chat.id, 'Подборка завершена!')
            message = Next()
            bot.register_next_step_handler(message, button)
        else:
            if (flag == True):
                user.setMark(user.usersActivity[len(user.usersActivity)-1]['id'], 5)
                user.addInfoToDB()
            else:
                lenght = len(user.usersActivity)-1
                user.setMark(user.usersActivity[lenght]['id'], 1)
                user.addInfoToDB()

            h = user.usersActivity.popitem()

            InterestKeyboard(message)
    else:
        user.addInfoToDB()
        user.usersActivity = {}
        message = Next()
        bot.register_next_step_handler(message, button)


def Next():
    global user
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttonNext = types.KeyboardButton('Далее')
    keyboard.add(buttonNext)
    return bot.send_message(user.chat_id, 'Для продолжения нажмите ДАЛЕЕ', reply_markup=keyboard)

def InterestKeyboard(message):
    global user
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    likeButton = types.KeyboardButton('✔ Интересует')
    disLikeButton = types.KeyboardButton('✘ Не интересует')
    backToInline = types.KeyboardButton('Назад, к выбору события')
    keyboard.add(likeButton, disLikeButton, backToInline)

    if ((len(user.usersActivity) - 1) == -1):
        bot.send_message(user.chat_id, 'Подборка завершена!')
        message = Next()
        bot.register_next_step_handler(message, button)
    else:
        msg = bot.send_message(user.chat_id, user.usersActivity[len(user.usersActivity) - 1]['msg'],
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, setMark)

if __name__ == '__main__':
    bot.polling(none_stop=True)



'''
                   types.InlineKeyboardButton(text='Знания', callback_data='education'),
                   types.InlineKeyboardButton(text='ART-вечер', callback_data='evening'),
                   types.InlineKeyboardButton(text='Выставки', callback_data='exhibition'),
                   types.InlineKeyboardButton(text='Мода', callback_data='fashion'),
                   types.InlineKeyboardButton(text='Фестивали', callback_data='festival'),
                   types.InlineKeyboardButton(text='Флешмобы', callback_data='flashmob'),
                   types.InlineKeyboardButton(text='Игры', callback_data='games'),
                   types.InlineKeyboardButton(text='В мире', callback_data='global'),
                   types.InlineKeyboardButton(text='Праздники', callback_data='holiday'),
                   types.InlineKeyboardButton(text='Детское ', callback_data='kids'),
                   types.InlineKeyboardButton(text='КВН', callback_data='kvn'),
                   types.InlineKeyboardButton(text='Магия', callback_data='magic'),
                   types.InlineKeyboardButton(text='Маскарады', callback_data='masquerade'),
                   types.InlineKeyboardButton(text='Встречи', callback_data='meeting'),
                   types.InlineKeyboardButton(text='Ночь', callback_data='night'),
                   types.InlineKeyboardButton(text='Разное', callback_data='other'),
                   types.InlineKeyboardButton(text='Вечеринки', callback_data='party'),
                   # types.InlineKeyboardButton(text='Постоянные выставки', callback_data='permanent-exhibitions'),
                   types.InlineKeyboardButton(text='Фотособытия', callback_data='photo'),
                   types.InlineKeyboardButton(text='Презентации', callback_data='presentation'),
                   types.InlineKeyboardButton(text='Квесты', callback_data='quest'),
                   types.InlineKeyboardButton(text='Романтика', callback_data='romance'),
                   types.InlineKeyboardButton(text='Распродажа', callback_data='sale'),
                   types.InlineKeyboardButton(text='Шопинг', callback_data='shopping'),
                   types.InlineKeyboardButton(text='Шоу', callback_data='show'),
                   # types.InlineKeyboardButton( text='Помощь',callback_data= 'social-activity'),
                   types.InlineKeyboardButton(text='Speed-dating', callback_data='speed-dating'),
                   types.InlineKeyboardButton(text='Спорт', callback_data='sport'),
                   types.InlineKeyboardButton(text='Стендап', callback_data='stand-up'),
                   types.InlineKeyboardButton(text='Акции', callback_data='stock'),
                   types.InlineKeyboardButton(text='Театр', callback_data='theater'),
                   types.InlineKeyboardButton(text='Экскурсии', callback_data='tour'),
                   types.InlineKeyboardButton(text='Ярмарки', callback_data='yarmarki-razvlecheniya-yarmarki'),
                   types.InlineKeyboardButton(text='Йога', callback_data='yoga'),
                   types.InlineKeyboardButton(text='Дни открытых дверей', callback_data='open')}]
'''