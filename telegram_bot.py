#!/usr/bin/env python

import logging
from telegram import Update
from telegram.ext import Updater, PrefixHandler, CallbackContext, MessageHandler, Filters
import config
import json
from datetime import time

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

subscribers_file = 'subscribers.txt'

def load_subscribers():
    try:
        with open(subscribers_file, 'r') as file:
            subscribers = json.load(file)
    except:
        subscribers = set()
    return set(subscribers)

def save_subscribers(subscribers):
    with open(subscribers_file, 'w') as file:
        json.dump(list(subscribers), file)

def subscribe(update: Update, context: CallbackContext):
    subscribers = load_subscribers()
    subscribers.add(update.effective_chat.id)
    save_subscribers(subscribers)
    update.message.reply_text("Ti sei sottoscritto")

def unsubscribe(update: Update, context: CallbackContext):
    subscribers = load_subscribers()
    subscribers.remove(update.effective_chat.id)
    save_subscribers(subscribers)
    update.message.reply_text("Hai annullato la sottoscrizione")

def send_plot_to_subscribers(context: CallbackContext):
    subscribers = load_subscribers()
    for chat_id in subscribers:
        context.bot.send_photo(chat_id, photo = open('plot.png', 'rb'))

def show_plot_handler(update: Update, context: CallbackContext):
    context.bot.send_photo(update.effective_chat.id, photo = open('plot.png', 'rb'))

def main(blocking = True):
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(config.TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(PrefixHandler(['!', '#', '/'], 'pollini', show_plot_handler))
    dispatcher.add_handler(PrefixHandler(['!', '#', '/'], 'subscribe', subscribe))
    dispatcher.add_handler(PrefixHandler(['!', '#', '/'], 'unsubscribe', unsubscribe))

    updater.job_queue.run_daily(send_plot_to_subscribers, time(hour=8))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    if blocking:
        updater.idle()


if __name__ == '__main__':
    main()