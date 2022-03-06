from selenium import webdriver
from time import sleep
import pyautogui
import telebot
import datetime
from pywinauto.application import Application

# What is this - https://habr.com/ru/post/533640/

dir_obs = 'C:/Program Files/obs-studio/bin/64bit'
driver_chrome = 'D:/QA-tests/drivers/chromedriver.exe'
dir_true_files = ''
dir_to_save_fail_screen = ''

name_fail_screen = ('screen' + str(datetime.datetime.today().strftime("%d%m%y%H%M%S")) + '.png')

bot_token = ''


def open_msteams(url):
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=driver_chrome, options=chrome_options)
    driver.set_window_size(1920, 1080)
    driver.get(url)
    find_and_click('/open_team.png')
    sleep(5)
    driver.close()


def find_element(element):
    sleep(1)
    r = None
    count = 100
    while r is None:
        count -= 1
        r = pyautogui.locateCenterOnScreen(dir_true_files + element, confidence=0.7)
        print(count)
        if count == 0:
            print(element + ' found!')
            break
        else:
            if r != None:
                print(element + ' not found!')
                return r
            else:
                continue


def find_and_click(element):
    sleep(1)
    element_find = find_element(element)
    if element_find:
        sleep(1)
        pyautogui.FAILSAFE = False
        pyautogui.moveTo(element_find.x+2, element_find.y+2)
        pyautogui.click(element_find, button='left', clicks=1)


def press_key(key):
    sleep(1)
    pyautogui.press(key)


def active_window(title):
    sleep(1)
    app = Application().connect(title_re=title, backend='win32')
    app.window(title_re=title).set_focus()
    sleep(3)


def write_text(text):
    sleep(1)
    pyautogui.write(text, interval=0.2)


def create_screenshot(screens_directory, name):
    sleep(1)
    im1 = pyautogui.screenshot()
    screenshot = im1.save(screens_directory + name)
    return screenshot


bot = telebot.TeleBot(bot_token)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text:
        try:
            bot.send_message(message.chat.id, text='Im starting entrance to the lesson')
            url = message.text
            open_msteams(url)
            find_and_click('/disable_micro.png')
            if find_element('/micro_status_on.png'):
                find_and_click('/micro_status_on.png')
            find_and_click('/apply_study.png')
            active_window('OBS')
            press_key('f7')
            sleep(3)

            create_screenshot(dir_to_save_fail_screen, name_fail_screen)
            bot.send_photo(message.chat.id, open(dir_to_save_screen + name_fail_screen, 'rb'))
            bot.send_message(message.chat.id, text='Im in the class, starting screen recording')

            # Duration of the lesson 90 min == 5400 sec
            sleep(5400)

            bot.send_message(message.chat.id, text='Lesson is over, Im go out')
            active_window('OBS')
            press_key('f8')
            sleep(3)

            find_and_click('/exit.png')
            bot.send_message(message.chat.id, text='Success!')
        except Exception as e:
            bot.send_message(message.chat.id, text='ERROR: ' + str(e))


bot.polling()
