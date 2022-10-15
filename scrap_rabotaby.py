from bs4 import BeautifulSoup
import requests
import time


class ParseRabota:
    url = "https://rabota.by/vacancies/programmist_python/bez_opyta_raboty"

    def __init__(self):
        self.page = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        self.soup = BeautifulSoup(self.page.text, "html.parser")
        self.allVacancy = self.soup.findAll("div", class_="serp-item")
        self.Vacancy = self.soup.find('div', class_='serp-item')

    def update_request_data(self):
        self.page = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        self.soup = BeautifulSoup(self.page.text, "html.parser")
        self.allVacancy = self.soup.findAll("div", class_="serp-item")
        self.Vacancy = self.soup.find('div', class_='serp-item')

    def get_vacancy(self):
        vacancy_text = self.soup.find("a", class_="serp-item__title").text
        vacancy_text_href = self.soup.find("a", class_="serp-item__title").get("href")
        self.update_request_data()
        return {"vacancy_text": vacancy_text,
                "vacancy_text_href": vacancy_text_href,
                }

    def get_new_vacancy(self):
        list_dicts_tasks = []
        for vacancy in list(self.allVacancy):
            vacancy_text = vacancy.find("a", class_="serp-item__title").text
            vacancy_text_href = vacancy.find("a", class_="serp-item__title").get("href")
            list_dicts_tasks.append({"vacancy_text": vacancy_text,
                                     "vacancy_text_href": vacancy_text_href,
                                     })
            self.update_request_data()
        return list_dicts_tasks

    def search_new_vacancy(self):
        set_old_vacancy = set(task_text.find("a", class_='serp-item__title').text for task_text in self.allVacancy)
        self.update_request_data()
        new_vacancy = self.soup.findAll('div', class_='serp-item')
        set_new_vacancy = set(task_text.find("a", class_='serp-item__title').text for task_text in new_vacancy)
        new_vacancy = set_new_vacancy.difference(set_old_vacancy)
        if len(new_vacancy) != 0:
            self.Vacancy = [parse_el for parse_el in new_vacancy
                            if parse_el.find("a", class_="serp-item__title").text in new_vacancy]
            return True


a = ParseRabota()
print(a.get_vacancy())
while True:
    if a.search_new_vacancy():
        print("Есть инфа")
        print(a.get_new_vacancy())
    else:
        print("Нет инфы")
    time.sleep(300)
