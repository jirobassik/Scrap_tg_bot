import telebot
from scrap.scrap_habr_freelance import ParseHabr
from scrap.scrap_rabotaby import ParseRabota
from thread_proc import Thread_proc

bot = telebot.TeleBot(token="5551249593:AAGlZTyq-ECD2vnjJp5nxFCt2npseTwY88s")
task_habr, vacancy_rabota = ParseHabr(), ParseRabota()
thread_habr, thread_rabota = Thread_proc(), Thread_proc()
