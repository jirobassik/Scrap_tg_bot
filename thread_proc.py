import threading
import time
from help_func import string_converse


def loop_track(name_class, choose: str, timer: int, time_to_push: int, message, bot, event) -> None:
    bot.send_message(message.chat.id, text=string_converse(name_class.get_first_info(), choose=choose))
    time_counter, collect_info_to_print = 0, []
    while not event.is_set():
        if name_class.search_new_info():
            collect_info_to_print.extend(name_class.get_new_many_info())
        match collect_info_to_print:
            case _ if time_counter >= time_to_push and len(collect_info_to_print) != 0:
                bot.send_message(message.chat.id, text=string_converse(collect_info_to_print, choose=choose))
                collect_info_to_print.clear()
                time_counter = 0
            case _ if time_counter >= time_to_push and len(collect_info_to_print) == 0:
                bot.send_message(message.chat.id,
                                 text=("В freelance.habr.com ничего нового нет..." if choose == "habr"
                                       else "В rabota.by ничего нового нет..."))
                time_counter = 0
        time.sleep(timer)
        time_counter += (timer // 60)


class Thread_proc:
    def __init__(self):
        self.__thread_proc = None
        self.__status = False
        self.__event = threading.Event()

    def init_thread(self, name_class, choose: str, timer: int, time_to_push: int, message, bot):
        self.__status = True
        self.__thread_proc = threading.Thread(target=loop_track,
                                              args=(name_class, choose, timer,
                                                    time_to_push, message, bot, self.__event),
                                              daemon=True)
        self.__thread_proc.start()

    def stop_thread(self, name_class):
        self.__status = False
        self.__event.set()
        name_class.update_request_data()
        self.__thread_proc = None

    def get_status(self):
        return self.__status
