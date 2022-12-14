from bot.bot_init_form import bot, task_habr
from help_func import string_converse, send_message_tags_keyw
from telebot.apihelper import ApiTelegramException

def order_start(message):
    msg_orders = bot.send_message(message.chat.id, f"Введите количество заказов, которые хотите вывести, "
                                                   f"всего: {task_habr.get_count_tasks()}")
    bot.register_next_step_handler(msg_orders, accept_orders)


def accept_orders(message):
    orders = int(message.text)
    orders_info = task_habr.get_many_tasks(orders)
    bot.send_message(message.chat.id, text=string_converse(orders_info, choose="habr"))


def order_start_filter(message):
    send_message_tags_keyw(message, bot)
    msg_orders = bot.send_message(message.chat.id, f"Введите количество заказов, которые хотите вывести, "
                                                   f"всего: {task_habr.get_count_tasks()}")
    bot.register_next_step_handler(msg_orders, filter_accept_orders)


def filter_accept_orders(message):
    orders = int(message.text)
    orders_info = task_habr.get_many_tasks_filtered(orders)
    res_converse = string_converse(orders_info, choose="habr")
    if res_converse != "":
        bot.send_message(message.chat.id, text=res_converse)
    else:
        bot.send_message(message.chat.id, text="Не было обнаружено заказов с данными фильтрами")


def paged_orders_search_tags_start(message):
    msg_orders = bot.send_message(message.chat.id, f"Введите тэги, по которым хотите искать")
    bot.register_next_step_handler(msg_orders, accept_paged_search_tags_orders)


def accept_paged_search_tags_orders(message):
    tags = message.text.split(", ")  # сделать регулярку проверки ввода
    list_all_pages, num_pages = task_habr.search_by_tags_all_page(tags), [*range(1, task_habr.find_last_page() + 1)]
    for num_page, list_dicts in enumerate(list_all_pages):
        text_ = f"{num_pages[num_page]} страница\n"
        if len(list_dicts) != 0:
            bot.send_message(message.chat.id, text=text_ + string_converse(list_dicts, choose="habr"))
        else:
            bot.send_message(message.chat.id, text=text_ + "-- ничего не найдено")


def paged_orders_start(message):
    msg_orders = bot.send_message(message.chat.id, f"Введите промежуток страниц, которые хотите вывести, от 1 до "
                                                   f"{task_habr.find_last_page()}")
    bot.register_next_step_handler(msg_orders, accept_paged_orders)


def accept_paged_orders(message):
    first_page, last_page = [int(num) for num in message.text.split(", ")]  # сделать регулярку проверки ввода
    list_all_pages, num_pages = task_habr.get_tasks_all_page(first_page, last_page), [*range(first_page, last_page + 1)]
    for num_page, list_dicts in enumerate(list_all_pages):
        text_ = f"{num_pages[num_page]} страница\n"
        try:
            bot.send_message(message.chat.id, text=text_ + string_converse(list_dicts, choose="habr"))
        except ApiTelegramException:
            bot.send_message(message.chat.id, text="Не могу вывести сообщение, слишком большое")