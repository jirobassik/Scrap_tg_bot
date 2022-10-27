from bot.bot_init_form import bot
from telebot import types
from json_func import json_upload_tuple, json_clear_tag_keyword, json_del_tag_kyew, json_save_tag_kyew_add
import ast

def tag_filter_start(message):
    msg_tag = bot.send_message(message.chat.id, "Введите тэги, по которым хотите фильтровать")
    bot.register_next_step_handler(msg_tag, tag_filter_accept_tag)

def tag_filter_accept_tag(message):
    tags = message.text
    json_save_tag_kyew_add(tags.split(", "), "tags")

def clear_tags(message):
    bot.send_message(message.chat.id, 'Тэги были очищены')
    json_clear_tag_keyword("tags")

def tag_window_delete(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Нет доступных тэгов" if len(json_upload_tuple()[0]) == 0
                     else "Список тэгов",
                     reply_markup=make_keyboard(json_upload_tuple()[0]),
                     parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def delete_tag(call):
    if call.data.startswith("['key'"):
        callback_value = ast.literal_eval(call.data)[1]
        json_del_tag_kyew("tags", callback_value)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Нет доступных тэгов" if len(json_upload_tuple()[0]) == 0
                              else "Список тэгов",
                              message_id=call.message.message_id,
                              reply_markup=make_keyboard(json_upload_tuple()[0]),
                              parse_mode='HTML')

def make_keyboard(json_list: list):
    cross_icon = u"\u274C"
    markup = types.InlineKeyboardMarkup()
    match json_upload_tuple()[2]:
        case {"tags": []}:
            pass
        case {"tags": _}:
            for value in json_list:
                markup.add(types.InlineKeyboardButton(text=value, callback_data=value),
                           types.InlineKeyboardButton(text=cross_icon, callback_data="['key', '" + value + "']"))
    return markup
