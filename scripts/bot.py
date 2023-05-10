import telebot

import misc
import make_data


location        = ''
deal_type       = ''
rooms           = ''
is_by_homeowner = 0
token           = misc.token
bot             = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    """Обработка команды start
    :param message: ответ пользователя на инициируемый ботом текст
    :return: ничего
    """

    bot.send_message(message.chat.id, 'Укажите населенный пункт:')
    bot.register_next_step_handler(message, get_location)


@bot.message_handler(content_types=['text'])
def get_rooms(message):
    """Получение типа квартиры
    :param message: ответ пользователя на инициируемый ботом текст
    :return: ничего
    """

    global rooms;
    rooms = message.text;

    keyboard = telebot.types.InlineKeyboardMarkup();
    key_yes  = telebot.types.InlineKeyboardButton(text="только от собственников",
                                                  callback_data="1");
    key_no   = telebot.types.InlineKeyboardButton(text="все",
                                                  callback_data="0");
    keyboard.add(key_yes);
    keyboard.add(key_no);

    question = 'Укажите, нужны ли все объявления или только от собственников:';
    bot.send_message(message.chat.id, text=question, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_location(message):
    """Получение населенного пункта
    :param message: ответ пользователя на инициируемый ботом текст
    :return: ничего
    """

    global location
    location = message.text

    keyboard      = telebot.types.InlineKeyboardMarkup();
    key_rent_long = telebot.types.InlineKeyboardButton(text="долгосрочная аренда",
                                                       callback_data="rent_long");
    key_sale      = telebot.types.InlineKeyboardButton(text="продажа",
                                                       callback_data="sale");
    keyboard.add(key_rent_long);
    keyboard.add(key_sale);

    question = 'Укажите тип объявлений:';
    bot.send_message(message.chat.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    """Получение is_by_homeowner или deal_type
    :param call: событие нажатия на кнопку
    :return: ничего
    """

    global deal_type, location, rooms, is_by_homeowner;

    if call.data.isdigit() :

        is_by_homeowner = call.data;
        bot.send_message(call.message.chat.id,
                         'location = ' + str(location) +
                         '; deal_type = ' + str(deal_type) +
                         '; rooms = ' + str(rooms) +
                         '; is_by_homeowner = ' + str(is_by_homeowner))
        bot.send_message(call.message.chat.id, 'Идет построение таблицы...')
        make_data.get_df(deal_type, location, rooms, is_by_homeowner)
        bot.send_message(call.message.chat.id, 'Таблица готова.')

    else :

        deal_type = call.data;
        bot.send_message(call.message.chat.id,
                        'Укажите через запятую интересующие типы квартиры: \n(1 - однокомнатная, \n 2 - двукомнатная, \n 3 - трехкомнатная, \n 4 - четырехкомнатная, \n studio - студия)');
        bot.register_next_step_handler(call.message, get_rooms);


if __name__ == '__main__':
    """Точка входа
    """

    bot.infinity_polling()
