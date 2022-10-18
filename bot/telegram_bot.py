import time
import telebot
from help_func import string_converse
from scrap.scrap_habr_freelance import ParseHabr
from scrap.scrap_rabotaby import ParseRabota
import threading

bot = telebot.TeleBot("5551249593:AAGlZTyq-ECD2vnjJp5nxFCt2npseTwY88s")
task_habr, vacancy_rabota = ParseHabr(), ParseRabota()


@bot.message_handler(commands=["help"])
def com_help(message):
    bot.send_message(message.from_user.id, "/start - Начать отслеживать freelance.habr.com и rabota.by")


@bot.message_handler(commands=["start"])
def tracking(message):
    bot.send_message(message.chat.id, "Начинаю отслеживать\nfreelance.habr.com и rabota.by")

    def loop(name_class, choose: str, timer: int, time_to_push: int) -> None:
        bot.send_message(message.chat.id, text=string_converse(name_class.get_first_info(), choose=choose))
        time_counter, collect_info_to_print = 0, []
        while True:
            if name_class.search_new_info():
                collect_info_to_print.extend(name_class.get_new_many_info())
            match collect_info_to_print:
                case _ if time_counter >= time_to_push and len(collect_info_to_print) != 0:
                    bot.send_message(message.chat.id, text=string_converse(collect_info_to_print, choose=choose))
                    collect_info_to_print.clear()
                    time_counter = 0
                case _ if time_counter >= time_to_push and len(collect_info_to_print) == 0:
                    bot.send_message(message.chat.id, text=("В freelance.habr.com" if choose == "habr"
                                     else "В rabota.by" " ничего нового нет..."))
                    time_counter = 0
            time.sleep(timer)
            time_counter += (timer // 60)

    thread_habr = threading.Thread(target=loop, args=(task_habr, "habr", 300, 60), daemon=True)
    thread_rabota = threading.Thread(target=loop, args=(vacancy_rabota, "rabota", 600, 60), daemon=True)

    thread_habr.start()
    thread_rabota.start()


bot.polling(none_stop=True, interval=0)
