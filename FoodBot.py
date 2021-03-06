import telepot
import threading
import json
import enum
import requests
import time
import datetime
import sys
from telepot.delegate import per_chat_id, create_open



import random

# https://telepot.readthedocs.io/en/latest/


token = ''  # use your own token, for protection purposes.

URL = "https://api.telegram.org/bot{}/".format(token)


class Food(enum.Enum):
   Pizza = 1
   Toast = 2
   Falafel = 3

def get_url(url):
    response = requests.get(url)

    content = response.content.decode("utf8")

    return content


def get_json_from_url(url):
    content = get_url(url)

    js = json.loads(content)

    return js


def get_updates():
    url = URL + "getUpdates"

    js = get_json_from_url(url)

    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])

    last_update = num_updates - 1

    text = updates["result"][last_update]["message"]["text"]

    chat_id = updates["result"][last_update]["message"]["chat"]["id"]

    return (text, chat_id)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)

    get_url(url)


text, chat = get_last_chat_id_and_text(get_updates())

send_message(text, chat)


def general_message(chat_id, general_text):
    url = URL + "sendMessage?text={}&chat_id={}".format(general_text, chat_id)

    get_url(url)

def time_of_order():
    localtime = time.localtime(time.time())
    dt_time = localtime
    time_hr = dt_time.tm_hour
    time_min = dt_time.tm_min
    #time_sec = dt_time.tm_sec
    cur_time = str(time_hr) + ":" + str(time_min) #+ ":" + str(time_sec) #seconds isn't necessary
    return cur_time

def order_availability(flag):
    if flag==False: flag = True


def total_execution(orders, order_counter):
    # orders are

    can_client_order = True
    localtime = time.localtime(time.time())
    text, chat = get_last_chat_id_and_text(get_updates())

    start_msg = "Hello! What would you like to order? For pizza, type 1. For a toast, type 2. For a falafel, type 3."

    faulty_msg = "I'm sorry. The value you entered is illegal. Try again later. "

    general_message(chat, start_msg)

    last_textchat = (None, None)

    time.sleep(5)  # the delay is made to allow the bot to recognize the user's input in time.

    while can_client_order:

        text, chat = get_last_chat_id_and_text(get_updates())

        if (text, chat) != last_textchat:

            last_textchat = (text, chat)

            num = int(last_textchat[0])

            if num > 3:

                general_message(chat, faulty_msg)

                raise Exception("Unauthorized value" + text)





            else:

                last_textchat = (text, chat)
                localtime = time.localtime(time.time())
                order_time = time_of_order()
                string = str(Food(int(text)))
                general_message(chat, "your order is " + string + " " + "at " + order_time)
                orders[str(chat)] = text  # adding the latest order to dictionary, by chat_id key, and order priority
                order_counter += 1
                can_client_order = False
                timer = threading.Timer(60 * 60 * 24, order_availability(
                    can_client_order))  # waiting for 24 hours, in a seconds converter
                timer.start()
                print(str(orders) +" , total orders currently" + str(order_counter))

#handling multiple requests


def main():

    #orders are managed by user id(chat id), and their specific order
    #total orders amount is saved into counter.
    orders = {}
    order_counter = 0

    bot = telepot.DelegatorBot(token, [
        (per_chat_id(), create_open(total_execution(orders, order_counter), timeout=10)),
    ])

#finally I inserted the entire order program into a func named total_excection.
#to  manage the total orders I made two global objects named orders, and total order number.
#after that I used a made library named telepot to manage multiple, parallel chats
#and running for each chat the program.


if __name__ == '__main__':
    main()




"""
useful commands for the bot.
#https://api.telegram.org/bot<your-bot-token>/getme

#https://api.telegram.org/bot<your-bot-token>/getUpdates

#getting replies from the bot :

#https://api.telegram.org/bot1259018719:AAFJGpJfixEkBJBut-SyjFY43voF_aRBAIg/sendMessage?chat_id=698903663&text=TestReply

#TelegramBot = telepot.Bot(token)

#print (TelegramBot.getMe())

#TelegramBot.getUpdates()

#print(TelegramBot.getUpdates(649179764+1))

"""




