import json

def json_save_tag_kyew_add(list_tag_keyw: list, key_js: str) -> None:
    with open('../tags_keywords.json', encoding='utf-8') as file_json:
        data = json.load(file_json)
    data[key_js].extend(list_tag_keyw)
    with open('../tags_keywords.json', 'w', encoding='utf-8') as file_json:
        json.dump(data, file_json, indent=4, ensure_ascii=False)

def json_upload_tuple() -> tuple:
    with open('../tags_keywords.json', encoding='utf-8') as file_json:
        data = json.load(file_json)
    return data["tags"], data["keywords"], data

def json_clear_tag_keyword(key_js: str) -> None:
    with open('../tags_keywords.json') as file_json:
        data = json.load(file_json)
    data[key_js].clear()
    with open('../tags_keywords.json', 'w') as file_json:
        json.dump(data, file_json, indent=4, ensure_ascii=False)

def json_del_tag_kyew(key_js: str, name_to_del: str) -> None:
    with open('../tags_keywords.json', encoding='utf-8') as file_json:
        data = json.load(file_json)
    data[key_js].remove(name_to_del)
    with open('../tags_keywords.json', 'w', encoding='utf-8') as file_json:
        json.dump(data, file_json, indent=4, ensure_ascii=False)
