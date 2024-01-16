# events.set_path("C:/Users/toto_/OneDrive/Рабочий стол/test/events/")
# QRs.set_path("C:/Users/toto_/OneDrive/Рабочий стол/test/QRs/")

# made by ROFLMAOL0L https://github.com/ROFLMAOL0L and lolevone https://github.com/lolevone
import telebot
import time
import os
from telebot import types

import QRs
import events


def clean(text):
    while "\n\n" in text:
        text = text.replace("\n\n", "\n")
    return text


print(time.ctime(time.time()), '\n', 'Gut_mero_bot started')
f = open("token.txt", 'r', encoding='utf-8')
professors_bot_token = f.readline()[:-1]
f.close()
# os.mkdir(str(os.getcwd()) + '/GUT_MERO_QRS/')
# os.mkdir(str(os.getcwd()) + '/GUT_MERO_TEXTS/')
qrs_path = str(os.getcwd()) + '/GUT_MERO_QRS/'
events_path = str(os.getcwd()) + '/GUT_MERO_TEXTS/'
events.set_path(events_path)
QRs.set_path(qrs_path)
bot = telebot.TeleBot(professors_bot_token)


# Создать мероприятие
@bot.message_handler(commands=['create_event'])
def create_event(message):
    bot.send_message(message.chat.id, "Введите название мероприятия")
    bot.register_next_step_handler(message, create_event_2)


def create_event_2(message):
    delta = 0
    for event_file in os.listdir(events_path):
        if event_file[:len(str(message.chat.id))] == str(message.chat.id):
            delta += 1
    event_title = str(message.chat.id) + '_' + str(delta)
    events.new_event(event_title)
    events.set_title(event_title, message.text)
    bot.reply_to(message, "Мероприятие успешно создано. Используйте команду /get_list_menu чтобы уточнить время, "
                          "количество студентов, описание и номер аудитории")


# Меню выбора мероприятия
@bot.message_handler(commands=['get_list_menu'])
def get_list_menu(message):
    events_list = events.get_list()
    temp_markup = types.InlineKeyboardMarkup()
    for i in range(len(events_list)):
        temp_markup.add(
            types.InlineKeyboardButton(
                text=events.get_title(events_list[i]),
                callback_data='edit/' + events_list[i])
        )
    bot.send_message(message.chat.id, "Выберите мероприятие", reply_markup=temp_markup)


# Кнопки изменения мероприятия
@bot.callback_query_handler(func=lambda call: call.data.split('/')[0] == 'edit')
def edit_event(call):
    temp_markup = types.InlineKeyboardMarkup()
    temp_markup.add(
        types.InlineKeyboardButton(
            text='Указать время и дату',
            callback_data='set_time/' + call.data.split('/')[1]
        )
    )
    temp_markup.add(
        types.InlineKeyboardButton(
            text='Указать аудиторию',
            callback_data='set_audience_number/' + call.data.split('/')[1]
        )
    )
    temp_markup.add(
        types.InlineKeyboardButton(
            text='Указать максимальное количество посетителей',
            callback_data='set_number_of_visitors/' + call.data.split('/')[1]
        )
    )
    temp_markup.add(
        types.InlineKeyboardButton(
            text='Написать описание',
            callback_data='set_description/' + call.data.split('/')[1]
        )
    )
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Выберите действие',
                          reply_markup=temp_markup)


# Изменение времени мероприятия
@bot.callback_query_handler(func=lambda call: call.data.split('/')[0] == 'set_time')
def set_event_time(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Введите время и дату')
    bot.register_next_step_handler(call.message, lambda m: set_event_time_2(m, call.data.split('/')[1]))


def set_event_time_2(message, event_name):
    events.set_time(event_name, clean(message.text))
    bot.send_message(message.chat.id, "Изменения успешно сохранены.")


# Изменение аудитории
@bot.callback_query_handler(func=lambda call: call.data.split('/')[0] == 'set_audience_number')
def set_audience_number(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Введите номер аудитории в формате "425/2"')
    bot.register_next_step_handler(call.message, lambda m: set_audience_number_2(m, call.data.split('/')[1]))


def set_audience_number_2(message, event_name):
    events.set_audience_number(event_name, clean(message.text))
    bot.send_message(message.chat.id, "Изменения успешно сохранены.")


# Изменение числа посетителей
@bot.callback_query_handler(func=lambda call: call.data.split('/')[0] == 'set_number_of_visitors')
def set_number_of_visitors(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Введите максимальное количество посетителей')
    bot.register_next_step_handler(call.message, lambda m: set_number_of_visitors_2(m, call.data.split('/')[1]))


def set_number_of_visitors_2(message, event_name):
    events.set_max_number_of_visitors(event_name, clean(message.text))
    bot.send_message(message.chat.id, "Изменения успешно сохранены.")


# Указать описание set_description
@bot.callback_query_handler(func=lambda call: call.data.split('/')[0] == 'set_description')
def set_number_of_visitors(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Введите описание мероприятия')
    bot.register_next_step_handler(call.message, lambda m: set_description_2(m, call.data.split('/')[1]))


def set_description_2(message, event_name):
    events.set_description(event_name, clean(message.text))
    bot.send_message(message.chat.id, "Изменения успешно сохранены.")


# Просмотреть все мероприятия
@bot.message_handler(commands=['mero_list'])
def create_event(message):
    events_list = events.get_list()
    temp_markup = types.InlineKeyboardMarkup()
    for i in range(len(events_list)):
        if events.get_numbers_of_visitors(events_list[i])[0] < events.get_numbers_of_visitors(events_list[i])[1]:
            temp_markup.add(
                types.InlineKeyboardButton(
                    text=events.get_title(events_list[i]),
                    callback_data='peek/' + events_list[i])
            )
    bot.send_message(message.chat.id, "Выберите мероприятие", reply_markup=temp_markup)


# Указать описание и дать возможность забронить меро
@bot.callback_query_handler(func=lambda call: call.data.split('/')[0] == 'peek')
def set_number_of_visitors(call):
    event_name = call.data.split('/')[1]
    temp_markup = types.InlineKeyboardMarkup()
    if str(call.message.chat.id) not in events.get_visitors_list(event_name):
        temp_markup.add(
            types.InlineKeyboardButton(
                text='Пойду!',
                callback_data='book/' + call.data.split('/')[1])
        )
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=str(events.get_title(event_name)) + '\n' + 'Аудитория ' +
                               str(events.get_audience_number(event_name)) + '\n' + 'Время и дата: ' +
                               str(events.get_time(event_name)) + '\n' + 'Количество посетителей: ' +
                               str(events.get_numbers_of_visitors(event_name)[0]) + '/' +
                               str(events.get_numbers_of_visitors(event_name)[1]) + '\n' +
                               str(events.get_description(event_name)),
                          reply_markup=temp_markup)


@bot.callback_query_handler(func=lambda call: call.data.split('/')[0] == 'book')
def book_event(call):
    event_name = call.data.split('/')[1]
    QRs.new_qr(str(event_name), str(call.message.chat.id))
    bot.send_photo(call.message.chat.id, photo=open(qrs_path + str(call.message.chat.id) + '.png', 'rb'))
    QRs.remove_qr(str(call.message.chat.id))
    events.add_visitor(event_name, str(call.message.chat.id))
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Вы успешно записаны на мероприятие "' + str(events.get_title(event_name)) + '"!' + '\n' +
                               'Вот QR-код к нему, покажите его на входе на мероприятие.')


# Проверка пользователя
@bot.message_handler(commands=['check_visitor'])
def check_visitor(message):
    events_list = events.get_list()
    temp_markup = types.InlineKeyboardMarkup()
    for i in range(len(events_list)):
        temp_markup.add(
            types.InlineKeyboardButton(
                text=events.get_title(events_list[i]),
                callback_data='check_visitor/' + events_list[i])
        )
    bot.send_message(message.chat.id, 'Выберите мероприятие, для которого проверяется билет', reply_markup=temp_markup)


@bot.callback_query_handler(func=lambda call: call.data.split('/')[0] == 'check_visitor')
def check_visitor_1(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Введите текст, распознанный камерой при наведении на QR-код посетителя')
    bot.register_next_step_handler(call.message, lambda m: check_visitor_2(m, call.data.split('/')[1]))


def check_visitor_2(message, event_name):
    visitor_id = QRs.decipher_qr(event_name, message.text)
    if visitor_id == '':
        bot.send_message(message.chat.id, 'Посетитель не найден. (неверный QR-код, не то мероприятие'
                                          ' или посетитель под таким QR-кодом уже прошел)')
    else:
        visitors_list = events.get_visitors_list(event_name)
        if visitor_id in visitors_list:
            events.mark_visitor(event_name, visitor_id)
            bot.send_message(message.chat.id, 'Посетитель найден в списках!')
        else:
            bot.send_message(message.chat.id, 'Посетитель не найден. (неверный QR-код, не то мероприятие'
                                              ' или посетитель под таким QR-кодом уже прошел)')


# Удалить мероприятие
@bot.message_handler(commands=['delete_mero'])
def delete_mero(message):
    events_list = events.get_list()
    temp_markup = types.InlineKeyboardMarkup()
    for i in range(len(events_list)):
        temp_markup.add(
            types.InlineKeyboardButton(
                text=events.get_title(events_list[i]),
                callback_data='delete/' + events_list[i])
        )
    bot.send_message(message.chat.id, "Выберите мероприятие которое хотите удалить", reply_markup=temp_markup)


@bot.callback_query_handler(func=lambda call: call.data.split('/')[0] == 'delete')
def set_number_of_visitors(call):
    event_name = call.data.split('/')[1]
    events.remove_event(event_name)
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Мероприятие удалено.')


# Старт, вопросы и помощь
@bot.message_handler(commands=['start', 'faq', 'help'])
def txt_file_reply(message):
    bot.reply_to(message, "Привет!")


bot.infinity_polling()
