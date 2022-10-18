from bs4 import BeautifulSoup
import requests
import nums_from_string
from datetime import datetime


class ParseHabr:
    url = "https://freelance.habr.com/tasks"

    def __init__(self):
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.text, "html.parser")
        self.allTasks = self.soup.findAll('li', class_='content-list__item')
        self.Task = self.soup.find('li', class_='content-list__item')
        self.href = self.Task.find("a").get("href")

    def update_request_data(self):
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.text, "html.parser")
        self.allTasks = self.soup.findAll('li', class_='content-list__item')
        self.Task = self.soup.find('li', class_='content-list__item')

    def get_first_info(self) -> list:
        return [{"task_text": self.Task.find("a").text,
                 "task_text_href": "https://freelance.habr.com" + self.Task.find("a").get("href"),
                 "task_time_pub": datetime.now().strftime("%H:%M"),
                 "tag_list": ", ".join([li.text for li in self.Task.find('ul', class_='tags tags_short')]),
                 }]

    def get_new_many_info(self) -> list:
        print("get_new_task - self.Task - list", self.Task)
        list_dicts_tasks = [{"task_text": task.find("a").text,
                             "task_text_href": "https://freelance.habr.com" + task.find("a").get("href"),
                             "task_time_pub": datetime.now().strftime("%H:%M"),
                             "tag_list": ", ".join([li.text for li in task.find('ul', class_='tags tags_short')]), }
                            for task in list(self.Task)]
        print(list_dicts_tasks)
        self.update_request_data()
        return list_dicts_tasks

    def get_many_tasks(self):
        self.Task = self.soup.findAll('li', class_='content-list__item', limit=10)
        return self.get_new_many_info()

    def search_new_info(self) -> bool:
        def get_id(task_search: list) -> set:
            return set(nums_from_string.get_nums(task_text.find("a").get("href"))[0]
                       for task_text in task_search)

        set_old_tasks = get_id(self.allTasks)
        print("old", set_old_tasks)
        self.update_request_data()

        new_data = self.soup.findAll('li', class_='content-list__item')
        set_new_tasks = get_id(new_data)
        print("new", set_new_tasks)

        new_tasks = set_new_tasks.difference(set_old_tasks)
        print("dif", new_tasks)
        if len(new_tasks) != 0:
            print("new_task", new_tasks)
            self.Task = [parse_el for parse_el in new_data
                         if nums_from_string.get_nums(parse_el.find("a").get("href"))[0] in new_tasks
                         and "минут" in parse_el.find("span", class_='params__published-at icon_task_publish_at').text]
            return True
