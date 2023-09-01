from contextlib import nullcontext
from statistics import median
from turtle import update
from urllib import response
import constants as keys
import responses as R
import telegram
from telegram import InputMediaPhoto
from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from PIL import Image
import logging

from aiogram import Bot, Dispatcher, executor, types

print("Bot started...")

API_TOKEN = 'BOT_TOKEN_HERE'

bot = Bot(token="5841113758:AAGgnScZeQHbDdKAl1awDL_YVjhOaeRIe1Y")
# dp = Dispatcher("5841113758:AAGgnScZeQHbDdKAl1awDL_YVjhOaeRIe1Y")

def start_command(update, context):
  
  img = Image.open('seo.png')
  update.message.reply_text(main_menu_message(),
                         reply_markup=main_menu_keyboard())
    # bot.send_photo(chat_id=update.message.chat.id, photo=open('seo.png','rb'),caption="hello", reply_markup=main_menu_keyboard())
  # update.sendMediaGroup(InputMediaPhoto(img,caption = "hello",reply_markup=main_menu_keyboard()))
    # update.message.reply_text("Type something random")

def main_menu(update, context):
  update.callback_query.message.edit_text(main_menu_message(),
                          reply_markup=main_menu_keyboard())

def first_menu(update, context):
  update.callback_query.message.edit_text(first_menu_message())

def second_menu(update, context):
  update.callback_query.message.edit_text(second_menu_message())

def third_menu(update, context):
  update.callback_query.message.edit_text(third_menu_message())

def fourth_menu(update, context):
  update.callback_query.message.edit_text(fourth_menu_message())

def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Plagiarism Checker', callback_data='m1'),InlineKeyboardButton('SEO Checker', callback_data='m2')],
              [InlineKeyboardButton('Keyword Density', callback_data='m3'),InlineKeyboardButton('Word Counter', callback_data='m4'),]]
  return InlineKeyboardMarkup(keyboard)

def main_menu_message():
  return """Hello Muthu.\nI am SEO bot. I can perform plagiarism checking, overall seo score, keyeword density, and word counter.\nJust send your file in word or pdf format and click any ooption to perform."""

def first_menu_message():
  return 'Send the document in pdf or word format'

def second_menu_message():
  return 'Send the document in pdf or word format'

def third_menu_message():
  return 'Send the document in pdf or word format'

def fourth_menu_message():
  return 'Send the document in pdf or word format'


def help_command(update, context):
    update.message.reply_text("updating...")

def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)

    update.message.reply_text(response)

def error(update, context):
    print(context.error)

def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    @dp.message_handler(commands=['test'])
    async def send_welcome(message: types.Message):
      await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")
      await types.ChatActions.upload_photo()

    # Create media group
      media = types.MediaGroup()

    # Attach local file
      media.attach_photo(types.InputFile('seo.png'), 'Cat!')
    # More local files and more cats!
      media.attach_photo(types.InputFile('seo.png'), 'More cats!')
      await message.reply_media_group(media=media)


    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    dp.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
    dp.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
    dp.add_handler(CallbackQueryHandler(third_menu, pattern='m3'))
    dp.add_handler(CallbackQueryHandler(fourth_menu, pattern='m4'))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

main()