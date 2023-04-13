import string
import re
from json_func import json_upload_tuple

def string_converse(list_dicts_: list, choose: str) -> str:
    res_string = ""
    match choose:
        case "habr":
            template = string.Template("$task_text\n"
                                       "$task_text_href\n"
                                       "Время обнаружения: $task_time_pub\n"
                                       f"Тэги: $tag_list\n")
        case "rabota":
            template = string.Template("$vacancy_text\n"
                                       "$vacancy_text_href\n")
    for dicts in list_dicts_:
        temp_res = template.substitute(dicts)
        res_string += temp_res + "\n"
    return res_string

def send_message_tags_keyw(message, bot) -> None:
    json_upl = json_upload_tuple()[2]
    tags = "Нет заданных тэгов"
    keywords = "Нет заданных ключевых слов"
    match json_upl:
        case {"tags": [], "keywords": []}:
            tags = "Нет заданных тэгов"
            keywords = "Нет заданных ключевых слов"
        case {"tags": tags, "keywords": []}:
            tags = "Заданные тэги: {x}".format(x=", ".join(tags))
            keywords = "Нет заданных ключевых слов"
        case {"tags": [], "keywords": keywords}:
            tags = "Нет заданных тэгов"
            keywords = "Заданные ключевые слова: {x}".format(x=", ".join(keywords))
        case {"tags": tags, "keywords": keywords}:
            tags = "Заданные тэги: {x}".format(x=", ".join(tags))
            keywords = "Заданные ключевые слова: {x}".format(x=", ".join(keywords))
    bot.send_message(message.chat.id, text=tags + "\n" + keywords)
