from bs4 import BeautifulSoup
import requests
import nums_from_string
from json_func import json_upload_tuple
from help_func import search_task_keyword
from datetime import datetime


class ParseHabr:
    url = "https://freelance.habr.com/tasks"

    def __init__(self):
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.text, "html.parser")
        self.allTasks = [filtered for filtered in self.soup.findAll('li', class_='content-list__item')
                         if filtered != "\n"]
        self.Task_list = [filtered for filtered in self.soup.findAll('li', class_='content-list__item')
                          if filtered != "\n"]
        self.Task = self.soup.find('li', class_='content-list__item')

    def update_request_data(self):
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.text, "html.parser")
        self.allTasks = [filtered for filtered in self.soup.findAll('li', class_='content-list__item')
                         if filtered != "\n"]
        self.Task_list = [filtered for filtered in self.soup.findAll('li', class_='content-list__item')
                          if filtered != "\n"]
        self.Task = self.soup.find('li', class_='content-list__item')

    def get_first_info(self) -> list:
        return [{"task_text": self.Task.find("a").text,
                 "task_text_href": "https://freelance.habr.com" + self.Task.find("a").get("href"),
                 "task_time_pub": datetime.now().strftime("%H:%M"),
                 "tag_list": ", ".join([li.text for li in self.Task.find('ul', class_='tags tags_short')]),
                 }]

    def get_new_many_info(self) -> list:
        list_dicts_tasks = [{"task_text": task.find("a").text,
                             "task_text_href": "https://freelance.habr.com" + task.find("a").get("href"),
                             "task_time_pub": datetime.now().strftime("%H:%M"),
                             "tag_list": ", ".join([li.text for li in task.find('ul', class_='tags tags_short')]), }
                            for task in self.Task_list]
        self.update_request_data()
        return list_dicts_tasks

    @staticmethod
    def get_new_many_info_page_turning(tasks) -> list:
        list_dicts_tasks = [{"task_text": task.find("a").text,
                             "task_text_href": "https://freelance.habr.com" + task.find("a").get("href"),
                             "task_time_pub": datetime.now().strftime("%H:%M"),
                             "tag_list": ", ".join([li.text for li in task.find('ul', class_='tags tags_short')]), }
                            for task in tasks]
        return list_dicts_tasks

    def get_many_tasks_filtered(self, lim: int):
        self.Task_list = self.soup.findAll('li', class_='content-list__item', limit=lim)
        self.filter_tasks()
        return self.get_new_many_info()

    def get_many_tasks(self, lim: int):
        self.Task_list = self.soup.findAll('li', class_='content-list__item', limit=lim)
        return self.get_new_many_info()

    def find_last_page(self) -> int:
        list_pages = self.soup.find("div", class_='pagination')
        last_page = max([int(nums.text) for nums in list_pages.findAll("a") if nums.text.isnumeric()])
        return last_page

    def get_tasks_all_page(self, first_page: int, last_page: int):
        page_url = "https://freelance.habr.com/tasks?page={}"
        res_list = []
        for page in range(first_page, last_page + 1):
            soup = BeautifulSoup(requests.get(page_url.format(page)).text, "html.parser")
            tasks = [filtered for filtered in soup.findAll('li', class_='content-list__item')
                     if filtered != "\n"]
            res_list.append(self.get_new_many_info_page_turning(tasks))
        return res_list

    def filter_tasks(self) -> None:
        json_upl = json_upload_tuple()[2]
        for task in reversed(self.Task_list):
            list_tags = [li.text for li in task.find('ul', class_='tags tags_short')]
            text = task.find("a").text
            match json_upl:
                case {"tags": [], "keywords": []}:
                    pass
                case {"tags": tags, "keywords": []}:
                    if len(set(tags).intersection(list_tags)) == 0:
                        self.Task_list.remove(task)
                case {"tags": [], "keywords": keywords} if not search_task_keyword(keywords, text):
                    if not search_task_keyword(keywords, text):
                        self.Task_list.remove(task)
                case {"tags": tags, "keywords": keywords}:
                    if not search_task_keyword(keywords, text) or len(set(tags).intersection(list_tags)) == 0:
                        self.Task_list.remove(task)

    def search_new_info(self) -> bool:  # не очень
        def get_id(task_search: list) -> set:
            return set(nums_from_string.get_nums(task_text.find("a").get("href"))[0]
                       for task_text in task_search)

        set_old_tasks = get_id(self.allTasks)
        self.update_request_data()

        new_data = self.soup.findAll('li', class_='content-list__item')
        set_new_tasks = get_id(new_data)

        new_tasks = set_new_tasks.difference(set_old_tasks)
        if len(new_tasks) != 0:
            print("new_task", new_tasks, new_data)
            self.Task_list = [parse_el for parse_el in new_data
                              if nums_from_string.get_nums(parse_el.find("a").get("href"))[0] in new_tasks
                              and "минут" in parse_el.find("span",
                                                           class_='params__published-at icon_task_publish_at').text]
            self.filter_tasks()
            if len(self.Task_list) != 0:
                return True

    # def filtered(self, new_tasks_id, new_data):
    #     self.Task_list = [parse_el for parse_el in new_data
    #                       if nums_from_string.get_nums(parse_el.find("a").get("href"))[0] in new_tasks_id
    #                       and "минут" in parse_el.find("span",
    #                                                    class_='params__published-at icon_task_publish_at').text]
    #     self.filter_tasks()


a = ParseHabr()

print(a.get_tasks_all_page(1, 5))
