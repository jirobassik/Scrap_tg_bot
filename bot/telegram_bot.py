from help_func import send_message_tags_keyw
from telebot import types
from orders import order_start, order_start_filter, paged_orders_start, paged_orders_search_tags_start
from bot.tag_key_w.tags_work import tag_filter_start, clear_tags, tag_window_delete
from bot.tag_key_w.keyword_work import keywords_filter_start, clear_keywords, keywords_window_delete
from bot.bot_init_form import bot, task_habr, vacancy_rabota, thread_habr, thread_rabota


@bot.message_handler(commands=["help"])
def com_help(message):
    bot.send_message(message.from_user.id, "/launch - Вывести основные кнопки\n"
                                           "/orders - Вывести кнопки для заказов habr\n"
                                           "/tags - Вывести кнопки для тэгов habr\n"
                                           "/keywords - Вывести кнопки для ключевых слов habr\n"
                                           "/start_track - Начать отслеживать freelance.habr.com и rabota.by\n"
                                           "/stop_track - Прекратить отслеживать freelance.habr.com и rabota.by\n")

@bot.message_handler(commands=["start_track"])
def tracking(message):
    if not thread_habr.get_status() and not thread_rabota.get_status():
        bot.send_message(message.chat.id, "Начинаю отслеживать\nfreelance.habr.com и rabota.by")
        send_message_tags_keyw(message, bot)
        thread_habr.init_thread(task_habr, "habr", 300, 30, message, bot)
        thread_rabota.init_thread(vacancy_rabota, "rabota", 600, 60, message, bot)
    else:
        bot.send_message(message.chat.id, "Уже отслеживаются\nfreelance.habr.com и rabota.by")

@bot.message_handler(commands=["stop_track"])
def stop_tracking(message):
    if thread_habr.get_status() and thread_rabota.get_status():
        thread_rabota.stop_thread(task_habr)
        thread_habr.stop_thread(vacancy_rabota)
        bot.send_message(message.chat.id, "Прекращаю отслеживать\nfreelance.habr.com и rabota.by")
    else:
        bot.send_message(message.chat.id, "Отслеживание нельзя прекратить, так как оно не начиналось")

@bot.message_handler(commands=["launch"])
def launch(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but_start_track = types.KeyboardButton("Старт отслежки")
    but_stop_track = types.KeyboardButton("Прекращение отслежки")
    but_orders = types.KeyboardButton("Заказы habr")
    but_tags = types.KeyboardButton("Тэги")
    but_keywords = types.KeyboardButton("Ключевые слова")
    markup.add(but_start_track, but_stop_track, but_tags, but_keywords, but_orders)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

@bot.message_handler(commands=["orders"])
def orders(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but_orders = types.KeyboardButton("Заказы")
    but_paged_orders = types.KeyboardButton("Заказы по страницам")
    but_paged_search_by_tags = types.KeyboardButton("Поиск заказов по тэгам")
    but_filter_orders = types.KeyboardButton("Фильтрованные заказы")
    but_main = types.KeyboardButton("Главная")
    markup.add(but_orders, but_paged_orders, but_paged_search_by_tags, but_filter_orders, but_main)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

@bot.message_handler(commands=["tags"])
def tag(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but_show = types.KeyboardButton("Все тэги")
    but_add = types.KeyboardButton("Добавить тэги")
    but_dell = types.KeyboardButton("Удалить все тэги")
    but_main = types.KeyboardButton("Главная")
    markup.add(but_show, but_add, but_dell, but_main)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

@bot.message_handler(commands=["keywords"])
def keywords_(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but_show = types.KeyboardButton("Все ключевые слова")
    but_add = types.KeyboardButton("Добавить ключевые слова")
    but_dell = types.KeyboardButton("Удалить все ключевые слова")
    but_main = types.KeyboardButton("Главная")
    markup.add(but_show, but_add, but_dell, but_main)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def tags_use(message):
    match message.text:
        case "Все тэги":
            tag_window_delete(message)
        case "Добавить тэги":
            tag_filter_start(message)
        case "Удалить все тэги":
            clear_tags(message)
        case "Все ключевые слова":
            keywords_window_delete(message)
        case "Добавить ключевые слова":
            keywords_filter_start(message)
        case "Удалить все ключевые слова":
            clear_keywords(message)
        case "Старт отслежки":
            tracking(message)
        case "Прекращение отслежки":
            stop_tracking(message)
        case "Тэги":
            tag(message)
        case "Ключевые слова":
            keywords_(message)
        case "Заказы habr":
            orders(message)
        case "Заказы":
            order_start(message)
        case "Заказы по страницам":
            paged_orders_start(message)
        case "Поиск заказов по тэгам":
            paged_orders_search_tags_start(message)
        case "Фильтрованные заказы":
            order_start_filter(message)
        case "Главная":
            launch(message)


bot.polling(none_stop=True, interval=0)
