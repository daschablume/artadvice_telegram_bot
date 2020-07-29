#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 16:43:39 2020

@author: macuser
"""
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import ConversationHandler
from sheet_logic import get_advice_string, archive_advice_list, list_of_text 
from sheet_logic import add_advice
import creditts
import time
import os
import logging 
from tokens import TOKEN, heroku_url

SLEEP_CONSTANT = 3
copy_of_advice_list = list_of_text.copy()
PORT = int(os.environ.get('PORT', 5000))
GETTING_ANSWER = range(1)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context): 
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=creditts.hello_msg)

def advice(update, context):
    global copy_of_advice_list
    advice_string = get_advice_string(copy_of_advice_list)
    if advice_string is None:
        advice_string = creditts.end_of_advices_msg
        copy_of_advice_list = list_of_text.copy()
        context.bot.send_message(
        chat_id=update.effective_chat.id, text=advice_string)
    else:
        context.bot.send_message(
        chat_id=update.effective_chat.id, text=advice_string)
        time.sleep(SLEEP_CONSTANT)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=creditts.advice_suggestion)
    
def about(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=creditts.creditts)
    
def archive(update, context):
    archive_advice_str = get_advice_string(archive_advice_list)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=archive_advice_str)
    
def add(update, context):
  update.message.reply_text(creditts.add_advice_sugg)
  time.sleep(SLEEP_CONSTANT)
  update.message.reply_text(creditts.return_suggestion)
  return GETTING_ANSWER

def received_information(update, context):
    text = update.message.text
    if text == '/cancel':
        return cancel(update, context)
    add_advice(text)
    update.message.reply_text(creditts.thanks_msg)
    time.sleep(SLEEP_CONSTANT)
    update.message.reply_text(creditts.advice_suggestion)
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text(creditts.cancel_msg)
    time.sleep(SLEEP_CONSTANT)
    update.message.reply_text(creditts.advice_suggestion)
    return ConversationHandler.END

def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=creditts.dont_understang_msg)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('advice',advice))
    dp.add_handler(CommandHandler('about', about))
    dp.add_handler(CommandHandler('archive', archive))
    conv_handler = ConversationHandler(
      entry_points = [CommandHandler('add', add)], 
      states = {GETTING_ANSWER: [MessageHandler(Filters.text, received_information)]},
      fallbacks = [CommandHandler('cancel', cancel)]        
    )
    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('heroku_url' + TOKEN)
    
if __name__ == '__main__':
    main()