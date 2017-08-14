# -*- coding: utf-8 -*-

import telebot
import time
import db_worker as db
from config import TOKEN, user_id

thumbs_up = '👍'
wrong = '☠'

commands = {  # command description used in the "help" command
              'word': 'get random word from dictionary in English',
              'delete': 'delete pair of words',
              'add': 'add new pair to Dictionary',
              'slovo': 'add random word from dictionary in Russian',
              'help': 'show all commands'
}

# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print (str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)

def user(chat_id):
    if chat_id == user_id[0]: return 'user_1'
    else: return 'user_2'

#Return a word and save their to the Shalve
@bot.message_handler(commands=['word'])
def new_words(m):
    usr = user(m.chat.id)
    word = db.save_words(usr, 'eng')
    db.status(m.chat.id, 1)
    bot.send_message(m.chat.id, word)
    
@bot.message_handler(commands=['slovo'])
def new_words(m):
    usr = user(m.chat.id)
    word = db.save_words(usr, 'rus')
    db.status(m.chat.id, 1)
    bot.send_message(m.chat.id, word)
    
# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page   

@bot.message_handler(commands=['add'], content_types=['text'])
def add_words(m):
    pass

@bot.message_handler(content_types=['text'])
def check_answer(m):
    usr = user(m.chat.id)
    words = db.load_words(usr)
    answer = ''
    if words[2] == 'eng': 
        answer = words[1]
    else: 
        answer = words[0]
    answer = answer.encode('utf-8')
    if m.text.lower() == answer.decode():
        sqldb = db.DBWorker()
        sqldb.add_point(usr, words[0], words[1])
        db.del_words(usr)
        bot.send_message(m.chat.id, thumbs_up)
    else:
        db.del_words(usr)
        bot.send_message(m.chat.id, wrong)
        bot.send_message(m.chat.id, 'Правильный ответ \n >>>>> {}'.format(answer.decode().upper()))
    word = db.save_words(usr, words[2])
    bot.send_message(m.chat.id, word)

    
if __name__ == '__main__':
    #print (db.load_words('user_1'))
    bot.polling(none_stop=True)