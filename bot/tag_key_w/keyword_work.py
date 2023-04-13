from bot.bot_init_form import bot
from telebot import types
from json_func import json_upload_tuple, json_clear_tag_keyword, json_del_tag_kyew, json_save_tag_kyew_add
import ast

def keywords_filter_start(message):
    msg_keyword = bot.send_message(message.chat.id, "Введите ключевые слова, по которым хотите фильтровать")
    bot.register_next_step_handler(msg_keyword, tag_filter_accept_keywords)

def tag_filter_accept_keywords(message):
    tags = message.text
    json_save_tag_kyew_add(tags.split(", "), "keywords")

def clear_keywords(message):
    bot.send_message(message.chat.id, 'Ключевые слова были очищены')
    json_clear_tag_keyword("keywords")

def keywords_window_delete(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Нет доступных ключевых слов" if len(json_upload_tuple()[1]) == 0
                     else "Список ключевых слов",
                     reply_markup=make_keyboard(json_upload_tuple()[1]),
                     parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def delete_keywords(call):
    if call.data.startswith("['keywords'"):
        callback_value = ast.literal_eval(call.data)[1]
        json_del_tag_kyew("keywords", callback_value)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Нет доступных ключевых слов" if len(json_upload_tuple()[1]) == 0
                              else "Список ключевых слов",
                              message_id=call.message.message_id,
                              reply_markup=make_keyboard(json_upload_tuple()[1]),
                              parse_mode='HTML')

def make_keyboard(json_list: list):
    markup = types.InlineKeyboardMarkup()
    match json_upload_tuple()[2]:
        case {"keywords": []}:
            pass
        case {"keywords": _}:
            for value in json_list:
                markup.add(types.InlineKeyboardButton(text=value, callback_data=value),)
    return markup
