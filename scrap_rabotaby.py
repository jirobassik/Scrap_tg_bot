from bs4 import BeautifulSoup
import requests
import re


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

    def get_first_info(self):
        return [{"vacancy_text": self.soup.find("a", class_="serp-item__title").text,
                 "vacancy_text_href": self.soup.find("a", class_="serp-item__title").get("href"),
                 }]

    def get_new_many_info(self):
        list_dicts_vacancy = [{"vacancy_text": vac.find("a", class_="serp-item__title").text,
                               "vacancy_text_href": vac.find("a", class_="serp-item__title").get("href"), }
                              for vac in list(self.Vacancy)]
        print("list vacancy", list_dicts_vacancy)
        self.update_request_data()
        return list_dicts_vacancy

    def search_new_info(self):
        def get_id(vac_search):
            return re.search(r'(?<=/)[0-9]+', vac_search.find("a", class_="serp-item__title").get("href")).group()

        set_old_vacancy = set(get_id(task_text_1) for task_text_1 in self.allVacancy)
        print("set old vac", set_old_vacancy)
        self.update_request_data()

        new_vacancy = self.soup.findAll('div', class_='serp-item')
        set_new_vacancy = set(get_id(task_text_2) for task_text_2 in new_vacancy)
        print("set new vac", set_new_vacancy)

        diff_vacancy = set_new_vacancy.difference(set_old_vacancy)
        print("diff vac", diff_vacancy)
        if len(diff_vacancy) != 0:
            self.Vacancy = [parse_el for parse_el in new_vacancy
                            if get_id(parse_el) in diff_vacancy]
            return True
