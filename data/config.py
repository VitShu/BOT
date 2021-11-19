from tkinter.tix import INTEGER

import telebot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import sqlite3


s = Service(r"C:\Users\Vital\Downloads\chromedriver_win32\chromedriver.exe")

driver = webdriver.Chrome(service=s)
id_user = ''
req_user = ''

bot = telebot.TeleBot("2047874741:AAHH6H4yqvi_TTuy18_lxcmI72tb-8-cYlg")
c = sqlite3.connect('users.db', check_same_thread=False)
cursor = c.cursor()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Этот бот пришлет 10 видео из YouTube по Вашему запросу.Для начала "
                                      "введите /")

    cursor.execute('CREATE TABLE IF NOT EXISTS info_id (id INTEGER, request TEXT)')


@bot.message_handler(commands=['search_videos'])
def search_videos(message):
    msg = bot.send_message(message.chat.id, "Введите текст,который вы ищите в YouTube")
    bot.register_next_step_handler(msg, search)


@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, "Вы что-то ищете? Для начала введите /")

def search(message):
    id_user = message.chat.id
    req_user = message.text
    cursor.execute('''INSERT INTO info_id (id, request) VALUES(?,?)''', (id_user,req_user))

    c.commit()

    bot.send_message(message.chat.id, "Начинаю поиск")
    video_href = "https://www.youtube.com/results?search_query=" + message.text
    driver.get(video_href)
    sleep(2)
    videos = driver.find_elements(By.ID, "video-title")
    for i in range(len(videos)):
        bot.send_message(message.chat.id, videos[i].get_attribute('href'))
        if i == 10:
            break





bot.polling()