from bs4 import BeautifulSoup
import requests
import time


class ParseHabr:
    url = "https://freelance.habr.com/tasks"

    def __init__(self):
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.text, "html.parser")
        self.allTasks = self.soup.findAll('li', class_='content-list__item')
        self.Task = self.soup.find('li', class_='content-list__item')

    def update_request_data(self):
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.text, "html.parser")
        self.allTasks = self.soup.findAll('li', class_='content-list__item')
        self.Task = self.soup.find('li', class_='content-list__item')

    def get_task(self):
        task_text = self.Task.find("a").text
        task_text_href = "https://freelance.habr.com" + self.Task.find("a").get("href")
        task_time_pub = self.Task.find("span", class_='params__published-at icon_task_publish_at').text
        tag_list = [li.text for li in self.Task.find('ul', class_='tags tags_short')]
        self.update_request_data()
        return {"task_text": task_text,
                "task_text_href": task_text_href,
                "task_time_pub": task_time_pub,
                "tag_list": tag_list,
                }

    def get_new_tasks(self):
        list_dicts_tasks = []
        for task in list(self.Task):
            task_text = task.find("a").text
            task_text_href = "https://freelance.habr.com" + task.find("a").get("href")
            task_time_pub = task.find("span", class_='params__published-at icon_task_publish_at').text
            tag_list = [li.text for li in task.find('ul', class_='tags tags_short')]
            list_dicts_tasks.append({"task_text": task_text,
                                     "task_text_href": task_text_href,
                                     "task_time_pub": task_time_pub,
                                     "tag_list": tag_list,
                                     })
            self.update_request_data()
        return list_dicts_tasks

    def get_many_tasks(self):
        self.Task = self.soup.findAll('li', class_='content-list__item', limit=10)
        self.get_new_tasks()

    def search_new_tasks(self):
        set_old_tasks = set(task_text.find("a").text for task_text in self.allTasks)
        self.update_request_data()
        new_data = self.soup.findAll('li', class_='content-list__item')
        set_new_tasks = set(task_text.find("a").text for task_text in new_data)
        new_tasks = set_new_tasks.difference(set_old_tasks)
        if len(new_tasks) != 0:
            self.Task = [parse_el for parse_el in new_data if parse_el.find("a").text in new_tasks]
            return True


a = ParseHabr()
print(a.get_task())
while True:
    if a.search_new_tasks():
        print("Есть инфа")
        print(a.get_new_tasks())
    else:
        print("Нет инфы")
    time.sleep(300)
