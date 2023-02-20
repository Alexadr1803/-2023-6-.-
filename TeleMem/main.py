import telebot
from telebot import types
from pathlib import Path
import os
import random

teams = {"Кошки" : "cats", "Собаки" : "dogs", "Компьютерные игры" : "games", "Школа" : "school"}
mem_add = False
mem = ["Отправить мем", "мем", "отправить мем", 'Мем']
send = False
god_mode = False
def get_path():
        raw_path = Path(__file__).resolve()
        source_path = raw_path.parent
        return str(source_path)

ans = "dogs"
bot = telebot.TeleBot('6012879927:AAGiVXmAstVC4hw1pF7PnCoSJwNbbRTz7Vg')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global god_mode
    print(message.from_user.username)
    if god_mode:
        if message.text == "send_all":
        
                for i in ["dogs", "cats", "school", "games"]:
                    path = f"{get_path()}\\{i}"
                    for j in os.listdir(f'{path}'):
                        k = open(f"{path}\\{j}", "rb")
                        bot.send_message(message.chat.id, "Вот ваш мем")
                        bot.send_photo(message.chat.id, k)
        if message.text[:4] == "eval":
            eval(message.text[4:])
            return

    if message.text in mem:
        rmk = types.ReplyKeyboardMarkup()
        rmk.add(types.KeyboardButton("Кошки"), types.KeyboardButton("Компьютерные игры"), types.KeyboardButton("Школа"),types.KeyboardButton("Собаки")); #наша клавиатура
        msg = bot.send_message(message.from_user.id, "Выберите тему мема из списка:", reply_markup=rmk)
        bot.register_next_step_handler(msg, callback_worker)
        

    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши 'Отправить мем' или 'Мем' для получения мема и напиши 'Добавить мем', чтобы добавить свою картинку в систему!")
    elif message.text == "exit please":
        bot.send_message(message.from_user.id, "Я служил вам верой и правдой, спасибо за пользование!")
        bot.send_message(message.from_user.id, "Еще увидимся... Досвидания....")
        raise "Вырубись"
    elif message.text == "god mode":
        bot.send_message(message.from_user.id, "Режим бога включен!")
        god_mode = True

    elif message.text == "Добавить мем":
        rmk = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        rmk.add(types.KeyboardButton("Кошки"), types.KeyboardButton("Компьютерные игры"), types.KeyboardButton("Школа"),types.KeyboardButton("Собаки")); #наша клавиатура
        msg = bot.send_message(message.from_user.id, "Выберите тему мема из списка:", reply_markup=rmk)
        bot.register_next_step_handler(msg, callback_worke)


    else:
        bot.send_message(message.from_user.id, "😭Я тебя не понимаю. Напиши /help для просмотра команд.")

def callback_worker(call):
    try:
        call.text = teams[call.text]
        path = f"{get_path()}\\{call.text}"
        k = open(f"{path}\\{random.choice(os.listdir(f'{path}'))}", "rb")
        bot.send_message(call.chat.id, "Вот ваш мем")
        bot.send_photo(call.chat.id, k)
        
    except Exception as error:
        bot.send_message(call.from_user.id, "Вы ввели что-то не то(")

def callback_worke(call):
    global ans
    if call.text in teams:
        ans = teams[call.text]
        bot.send_message(call.from_user.id, "Пришлите картинку!")
        bot.register_next_step_handler(call, add_mem)
    else:
        bot.send_message(call.from_user.id, "Вы ввели что-то не то!")

def add_mem(message):
    global ans
    try:
        from string import ascii_lowercase
        from random import sample
        word = ''.join(sample(ascii_lowercase, 5)).capitalize()
        mem_add = message.photo[-1].file_id   
        file_info = bot.get_file(mem_add)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f"{get_path()}\\{ans}\\{word}.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "Картинка добавлена!🤠")
    except:
        bot.send_message(message.chat.id, "Это не картинка!🤠")
        bot.send_message(message.chat.id, "Введи добавить мем снова!")
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


bot.polling(none_stop=True, interval=0)
