import time
from help_func import string_converse
from help_func import send_message_tags_keyw
import threading
from telebot import types
from orders import order_start, order_start_filter, paged_orders_start
from bot.tag_key_w.tags_work import tag_filter_start, clear_tags, tag_window_delete
from bot.tag_key_w.keyword_work import keywords_filter_start, clear_keywords, keywords_window_delete
from bot.bot_init_form import bot, task_habr, vacancy_rabota

@bot.message_handler(commands=["help"])
def com_help(message):
    bot.send_message(message.from_user.id, "/start_track - Начать отслеживать freelance.habr.com и rabota.by")

@bot.message_handler(commands=["start_track"])
def tracking(message):
    bot.send_message(message.chat.id, "Начинаю отслеживать\nfreelance.habr.com и rabota.by")
    send_message_tags_keyw(message, bot)

    def loop(name_class, choose: str, timer: int, time_to_push: int) -> None:
        bot.send_message(message.chat.id, text=string_converse(name_class.get_first_info(), choose=choose))
        time_counter, collect_info_to_print = 0, []
        while True:
            print("col_info_print", collect_info_to_print)
            if name_class.search_new_info():
                collect_info_to_print.extend(name_class.get_new_many_info())
            match collect_info_to_print:
                case _ if time_counter >= time_to_push and len(collect_info_to_print) != 0:
                    bot.send_message(message.chat.id, text=string_converse(collect_info_to_print, choose=choose))
                    collect_info_to_print.clear()
                    time_counter = 0
                case _ if time_counter >= time_to_push and len(collect_info_to_print) == 0:
                    bot.send_message(message.chat.id,
                                     text=("В freelance.habr.com ничего нового нет..." if choose == "habr"
                                           else "В rabota.by ничего нового нет..."))
                    time_counter = 0
            time.sleep(timer)
            time_counter += (timer // 60)

    thread_habr = threading.Thread(target=loop, args=(task_habr, "habr", 300, 30), daemon=True)
    thread_rabota = threading.Thread(target=loop, args=(vacancy_rabota, "rabota", 600, 60), daemon=True)

    thread_habr.start()
    thread_rabota.start()

@bot.message_handler(commands=["launch"])
def launch(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but_start_track = types.KeyboardButton("Старт отслежки")
    but_orders = types.KeyboardButton("Заказы habr")
    but_tags = types.KeyboardButton("Тэги")
    but_keywords = types.KeyboardButton("Ключевые слова")
    markup.add(but_start_track, but_tags, but_keywords, but_orders)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

def orders(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but_orders = types.KeyboardButton("Заказы")
    but_paged_orders = types.KeyboardButton("Заказы по страницам")
    but_filter_orders = types.KeyboardButton("Фильтрованные заказы")
    markup.add(but_orders, but_paged_orders, but_filter_orders)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

@bot.message_handler(commands=["tags"])
def tag(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but_show = types.KeyboardButton("Все тэги")
    but_add = types.KeyboardButton("Добавить тэги")
    but_dell = types.KeyboardButton("Удалить все тэги")
    markup.add(but_show, but_add, but_dell)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

@bot.message_handler(commands=["keywords"])
def keywords_(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but_show = types.KeyboardButton("Все ключевые слова")
    but_add = types.KeyboardButton("Добавить ключевые слова")
    but_dell = types.KeyboardButton("Удалить все ключевые слова")
    markup.add(but_show, but_add, but_dell)
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
        case "Фильтрованные заказы":
            order_start_filter(message)


bot.polling(none_stop=True, interval=0)
