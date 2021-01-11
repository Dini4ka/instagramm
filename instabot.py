# нужна программа, которая будет автоматически отправлять комментарии на определённые посты.
# должна быть возможность указать ссылку на пост,
# задать различный текст комментариев и временной интервал отправки (каждый час, каждые 7 мин и т.п.)

# login1 : dorozhka_ula
# number_phone1 : 79641411590
# password1 : Denis_71265

# login2 : petranna12
# number_phone2 : 79605908231
# password2 : Denis_71265

# login3 : andrpan12
# number_phone3 : 79258688784
# password3 : Denis_71265

# link : https://www.instagram.com/p/CJkAmg-h43m/

from time import sleep
import pickle
from selenium import webdriver
import os
import random

# Запуск всех трёх ботов
bot1 = webdriver.Firefox(executable_path='geckodriver.exe')
bot2 = webdriver.Firefox(executable_path='geckodriver.exe')
#bot3 = webdriver.Firefox(executable_path='geckodriver.exe')


class instabot:

    def __init__(self):
        self.username_bot1 = 'dorozhka_ula'
        self.password_bot1 = 'Denis_71265'
        self.username_bot2 = 'petranna12'
        self.password_bot2 = 'Denis_71265'
        #self.username_bot3 = 'andrpan12'
        #self.password_bot3 = 'Denis_71265'

        #авторизуем ботов
        bot1.get('https://www.instagram.com/')
        bot2.get('https://www.instagram.com/')
        #bot3.get('https://www.instagram.com/')
        sleep(2)

        # Следующие строки говорят боту найти поля для заполнения логина и пароля.
        username_input_bot1 = bot1.find_element_by_name("username")
        password_input_bot1 = bot1.find_element_by_name("password")
        username_input_bot2 = bot2.find_element_by_name("username")
        password_input_bot2 = bot2.find_element_by_name("password")
        #username_input_bot3 = bot3.find_element_by_name("username")
        #password_input_bot3 = bot3.find_element_by_name("password")

        # Заполнение логина и пароля
        username_input_bot1.send_keys(self.username_bot1)
        password_input_bot1.send_keys(self.password_bot1)
        username_input_bot2.send_keys(self.username_bot2)
        password_input_bot2.send_keys(self.password_bot2)
        #username_input_bot3.send_keys(self.username_bot3)
        #password_input_bot3.send_keys(self.password_bot3)

        # Вход
        login_button_bot1 = bot1.find_element_by_xpath("//button[@type='submit']")
        login_button_bot2 = bot2.find_element_by_xpath("//button[@type='submit']")
        #login_button_bot3 = bot3.find_element_by_xpath("//button[@type='submit']")
        try:
            login_button_bot1.click()
            print('bot1 is ready')
        except:
            print('bot1 is broken')
        try:
            login_button_bot2.click()
            print('bot2 is ready')
        except:
            print('bot2 broken')
        #try:
        #    login_button_bot3.click()
        #    print('bot3 is ready')
        #except:
        #   print('bot3 broken')
        # Берём куки или обновляем их
        pickle.dump(bot1.get_cookies(), open("cookies_bot_1.pkl", "wb"))
        pickle.dump(bot2.get_cookies(), open("cookies_bot_2.pkl", "wb"))
        #pickle.dump(bot3.get_cookies(), open("cookies_bot_3.pkl", "wb"))

        sleep(5)


    def type_comments(self, links, nicks, time, count):
        cookies_for_bot1 = pickle.load(open("cookies_bot_1.pkl", "rb"))
        cookies_for_bot2 = pickle.load(open("cookies_bot_2.pkl", "rb"))
        #cookies_for_bot3 = pickle.load(open("cookies_bot_3.pkl", "rb"))
        # Переведём время в секунды
        letter = time[len(time) - 1]
        if letter == 'm':
            time = int(time[0:len(time) - 1]) * 60
        if letter == 's':
            time = int(time[0:len(time) - 1]) * 1
        if letter == 'h':
            time = int(time[0:len(time) - 1]) * 3600
        if letter == 'd':
            time = int(time[0:len(time) - 1]) * 3600 * 24
        for i in range(count):
            for link in links:
                who_is_he = [bot1, bot2]
                author = random.choice(who_is_he)
                author.get(link)
                #bot3.get(link)
                if author == bot1:
                    for cookie in cookies_for_bot1:
                        author.add_cookie(cookie)
                else:
                    for cookie in cookies_for_bot2:
                        author.add_cookie(cookie)
                #for cookie in cookies_for_bot3:
                #    bot3.add_cookie(cookie)
                sleep(5)
                comment_text = random.sample(nicks,random.randint(2,len(nicks)))
                comment = author.find_element_by_class_name('Ypffh')
                comment.click()
                comment = author.find_element_by_class_name('Ypffh.focus-visible')
                comment.send_keys(' '.join(comment_text))
                send_button = author.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[3]/div/form/button')
                send_button.click()
                sleep(time)
                sleep(2)

BOTS = instabot()
