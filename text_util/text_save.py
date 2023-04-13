import pandas as pd


def create_csv_order(list_dict_orders: list[dict]):
    header = ('Задача', 'Ссылка', 'Время', 'Тэги')
    df = pd.DataFrame(list_dict_orders, )
    df.to_csv('D:\Programs\PyCharm 2021.3.3\PetPr Get data and push Tg bot\\text_util\\temp\habr_orders.csv',
              index=False, header=header, encoding='utf-8')
