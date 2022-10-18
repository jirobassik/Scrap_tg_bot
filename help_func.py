import string

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
