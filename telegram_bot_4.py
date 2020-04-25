from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import random
import math

base_keyboard = [['/dice', '/timer']]
dice_keyboard = [['/6', '/2x6', '/20', '/back']]
timer_keyboard = [['/30s', '/1m', '/5m', '/back']]
close_keyboard = [['/close']]

base_markup = ReplyKeyboardMarkup(base_keyboard, one_time_keyboard=False)
dice_markup = ReplyKeyboardMarkup(dice_keyboard, one_time_keyboard=False)
timer_markup = ReplyKeyboardMarkup(timer_keyboard, one_time_keyboard=False)
active_timer_markup = ReplyKeyboardMarkup(close_keyboard, one_time_keyboard=False)


def start(update, context):
    update.message.reply_text('Привет! Я бот-гадалка!')
    update.message.reply_text("/dice: кинуть кубики, /timer: засечь время", reply_markup=base_markup)


def dices(update, context):
    update.message.reply_text("кинуть кубики: 6 граней, 2 по 6, 20 или вернуться назад", reply_markup=dice_markup)


def dice6(update, context):
    number = math.trunc(random.random() * 6) + 1
    update.message.reply_text("{0}".format(number))


def dice2x6(update, context):
    number1 = math.trunc(random.random() * 6) + 1
    number2 = math.trunc(random.random() * 6) + 1
    update.message.reply_text("{0} {1}".format(number1, number2))


def dice20(update, context):
    number = math.trunc(random.random() * 20) + 1
    update.message.reply_text("{0}".format(number))


# Управление таймерами.

def timers(update, context):
    update.message.reply_text("засечь: 30 сек., 1 мин., 5 мин.  или вернуться назад", reply_markup=timer_markup)


def set_timer(update, context, delay):
    job = context.job_queue.run_once(finish_timer, delay, context=update.message.chat_id)

    context.chat_data['job'] = job
    update.message.reply_text('Установлен таймер на {0} секунд'.format(delay), reply_markup=active_timer_markup)


def finish_timer(context):
    job = context.job
    context.bot.send_message(job.context, text='Время истекло.', reply_markup=timer_markup)


def reset_timer(update, context):
    if 'job' in context.chat_data:
        context.chat_data['job'].schedule_removal()
        del context.chat_data['job']

    update.message.reply_text('Таймер сброшен.', reply_markup=timer_markup)


# Таймеры

def timer30s(update, context):
    set_timer(update, context, 30)


def timer1m(update, context):
    set_timer(update, context, 60)


def timer5m(update, context):
    set_timer(update, context, 300)


def main():
    updater = Updater("YOUR_TOKEN", use_context=True)

    dp = updater.dispatcher

    # Переключение режимов
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("dice", dices))
    dp.add_handler(CommandHandler("timer", timers))
    dp.add_handler(CommandHandler("back", start))

    # Кубики
    dp.add_handler(CommandHandler("6", dice6))
    dp.add_handler(CommandHandler("2x6", dice2x6))
    dp.add_handler(CommandHandler("20", dice20))

    # Таймеры
    dp.add_handler(CommandHandler("30s", timer30s, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("1m", timer1m, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("5m", timer5m, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("close", reset_timer, pass_chat_data=True))

    updater.start_polling()
    print('Bot started')
    updater.idle()


if __name__ == '__main__':
    main()