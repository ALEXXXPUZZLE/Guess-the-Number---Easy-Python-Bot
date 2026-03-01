import telebot 
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton # <--- libraries
import random 



bot = telebot.TeleBot('8470359939:AAEeFa-NBEWu4GpZeB9LuDTveOlaUx5NxMQ') # <----- import your token from @botfather
tmp_number = []


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id, 'A simple game: guess the number!\nWrite a number, and if it matches, you win!\nNumbers range from 1 to 100!'
)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add('play')
    bot.send_message(message.chat.id, 'Do you want to play the game Guess the number from 1 to 100? If so, click the button or write "play".', reply_markup=markup)
@bot.message_handler(func=lambda message: message.text in ['play', 'Play'])


def game(message):
    tmp_number.append(random.randint(1, 100))
    msg = bot.send_message(message.chat.id, 'I thought of a number, write it down and try to guess it.')
    bot.register_next_step_handler(msg, check_num)
def check_num(message):
    try:
        if int(message.text) > 100 or int(message.text) <= 0:
            bot.send_message(message.chat.id, 'No more than 100 and no less than 0')
            tmp_number.clear()
            game(message)
        else:
            if int(message.text) in tmp_number:
                bot.send_message(message.chat.id, 'You guessed it right!')
                tmp_number.clear()
            else:
                markup = types.ReplyKeyboardMarkup()
                markup.add('Yes')
                bot.send_message(message.chat.id, f'You guessed wrong, I guessed: {tmp_number[0]}. Want to try again?', reply_markup=markup)
                tmp_number.clear()
    except ValueError:
        bot.send_message(message.chat.id, 'Enter integer!')

@bot.message_handler(func=lambda message: message.text in ['yes', 'Yes'])

def callback_check(message):
    if message.text.lower() == 'yes':
        game(message)
    else:
        start(message)

bot.infinity_polling()