import json
import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from aiogram.types import ContentTypes, Message
import docx2txt
import PyPDF2
import glob
import pathlib
import textstat
import requests
from bs4 import BeautifulSoup
import urllib
from requests_html import HTML
from requests_html import HTMLSession
from difflib import SequenceMatcher

API_TOKEN = 'xxxx'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

print("bot started...")

def word_count(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts

def getstr(latest_file):
    ext = pathlib.Path(latest_file).suffix

    if(ext == ".docx"):
        print("this is docx file\n")
        if os.path.isfile(latest_file):
            file = open(latest_file, encoding="UTF-8", errors='ignore')
            my_text = docx2txt.process(latest_file)
            return(my_text)
    elif(ext == ".pdf"):
        print("this is pdf file\n")
        if os.path.isfile(latest_file):
            pdffileobj=open(latest_file,'rb')
            pdfreader=PyPDF2.PdfFileReader(pdffileobj)
            x=pdfreader.numPages
            print(x)
            my_text=''
            for i in range(0,x):
                pageObj = pdfreader.getPage(i)
                a = pageObj.extractText()
                my_text = my_text+a
    elif(ext == ".txt"):
        print("txt file")
        if os.path.isfile(latest_file):
            file = open(latest_file)
            my_text = file.read()
            return my_text

def readability(my_text):
    x = textstat.flesch_reading_ease(my_text)
    y = textstat.flesch_kincaid_grade(my_text)
    print(x)
    print(y)
    return x

# web scraping

def removetags(content):
    for data in content(['style','script']):
        data.decompose()
    return ' '.join(content.stripped_strings)

def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except:
        print("error")

def scrap(query):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)
    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)
    return links

def gettextlist(c):
    u = []
    for i in range(0,10):
        u.append(c[i])

    r = []
    for i in u:
        temp = requests.get(i)
        r.append(temp)

    t = []
    for i in r:
        soup = BeautifulSoup(i.content,'html.parser')
        a = removetags(soup)
        t.append(a)
    return t

def getratio(t,test_str):
    my_seq = []
    for i in t:
        seq = SequenceMatcher(a = test_str, b = i)
        my_seq.append(seq.ratio()*100)
    sum = 0
    for i in my_seq:
        print(i)
        sum = sum+i
    avg = sum/5
    return avg


button1 = InlineKeyboardButton(text="Plagiarism Checker", callback_data="m1")
button2 = InlineKeyboardButton(text="SEO Score", callback_data="m2")
button3 = InlineKeyboardButton(text="Keyword Density", callback_data="m3")
button4 = InlineKeyboardButton(text="Word Counter", callback_data="m4")

button5 = InlineKeyboardButton(text="Total Keywords", callback_data="m5")
button6 = InlineKeyboardButton(text="Specific Keyword", callback_data="m6")
button7 = InlineKeyboardButton(text="Top Keyword", callback_data="m7")

button8 = InlineKeyboardButton(text="Operations", callback_data="m8")
button9 = InlineKeyboardButton(text="My father", url='https://t.me/Muthuram0')
button10 = InlineKeyboardButton(text="Help", callback_data="m10")
button11 = InlineKeyboardButton(text="Buy me coffe", callback_data="m11")

keyboard_inline = InlineKeyboardMarkup(row_width=2).add(button1,button2,button3,button4)
keyboard_inline2 = InlineKeyboardMarkup(row_width=2).add(button5,button6,button7)
keyboard_inline3 = InlineKeyboardMarkup(row_width=2).add(button8,button9,button10,button11)

@dp.message_handler(commands=['start'])
async def echo(message: types.Message):
    # await types.ChatActions.upload_photo()

    # media = types.MediaGroup()

    name = message.from_user.first_name
    print(name)

    photo = InputFile("seo.png")
    await bot.send_photo(chat_id=message.chat.id, photo = photo, 
        caption = f"Hello {name}.\nI am SEO bot. I can perform plagiarism checking, analysing the overall seo score based on the important attributes, find the keywords list and the density of the every keywords, and can give the count of words in the file.\nJust send your file in word or pdf format and click any option to perform.\n\n\nMy operations : \n1. Plagiarism Checker   2. SEO Score Analysis\n3. Keyword Density   4. Word Counter\n", 
        reply_markup = keyboard_inline3)

    # media.attach_photo(types.InputFile('seo.png'), f"Hello {name}.\nI am SEO bot. I can perform plagiarism checking, analysing the overall seo score based on the important attributes, find the keywords list and the density of the every keywords, and can give the count of words in the file.\nJust send your file in word or pdf format and click any option to perform.\n\n\nMy operations : \n1. Plagiarism Checker   2. SEO Score Analysis\n3. Keyword Density   4. Word Counter\n\nType '/operations' to get all the operations.")
    # await message.reply_media_group(media=media)
    
@dp.message_handler(commands=['operations','operation'])
async def send_welcome(message: types.Message):
    await message.reply("Operations",reply_markup=keyboard_inline)

# @dp.message_handler(commands=['testing'])
# async def send_testing(message: types.Message):
#     photo = InputFile("seo.png")
#     await bot.send_photo(chat_id=message.chat.id, photo = photo, caption = "hello", reply_markup = keyboard_inline)

@dp.callback_query_handler(text="m1")
async def reply(call:types.CallbackQuery):
    list_of_files = glob.glob('E:\pythontut\seobot\downloads\documents\*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    c = getstr(latest_file)
    await call.message.answer("Enter a heading of the file(which is used to search on the google)")
    @dp.message_handler()
    async def specific(message: types.Message):
        query = message.text
        await call.message.answer("Please wait...")
        linklist = scrap(query)
        textlist = gettextlist(linklist)
        ratio = getratio(textlist,c)
        await call.message.answer(ratio)
    

@dp.callback_query_handler(text="m2")
async def reply(call:types.CallbackQuery):
    list_of_files = glob.glob('E:\pythontut\seobot\downloads\documents\*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    c = getstr(latest_file)
    read_score = readability(c)
    await call.message.answer(read_score)

@dp.callback_query_handler(text="m3")
async def reply(call:types.CallbackQuery):
    await call.message.answer("Operations",reply_markup=keyboard_inline2)

@dp.callback_query_handler(text="m4")
async def reply(call:types.CallbackQuery):
    list_of_files = glob.glob('E:\pythontut\seobot\downloads\documents\*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    c = getstr(latest_file)
    count = 0
    c = c.lower()
    word_list = c.split(" ")
    d = len(word_list)
    await call.message.answer(d)

@dp.callback_query_handler(text="m5")
async def reply(call:types.CallbackQuery):

    list_of_files = glob.glob('E:\pythontut\seobot\downloads\documents\*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    c = getstr(latest_file)
    c = c.lower()
    e = word_count(c)

    elimination = ['-','is','an','a','the','was','are','were','have','had','has',
                    'been','be','what','where','when','whom','who','whose',
                    'how','to','in','about','i','for','you','him','her','she',
                    'they','them','with','without','say','said','of','and','to',
                    'too','it','that','this','on','do','did','done','at','but',
                    'we','by','can','could','will','would','must','might','as',
                    'go','up','once','upon','your',':',',','.','','he','after',
                    'from','his','during','these','also','known'  ]
    keys = []
    values = []
    items = e.items()
    for item in items:
        keys.append(item[0]), values.append(item[1])
    for a in keys:
        for b in elimination:
            if(a == b):
                del e[a]
                break
    sorted_dict = sorted(e.items(),key=lambda x:x[1],reverse=True)
    print(sorted_dict)
    print(len(sorted_dict))

    result = json.dumps(sorted_dict)
    print(len(result))
    if len(result) > 4096:
        for x in range(0, len(result), 4096):
            await call.message.answer(result[x:x+4096])
    else:
        await call.message.answer(result)
    # await call.message.answer(result)

@dp.callback_query_handler(text="m6")
async def reply(call:types.message):
    await call.message.answer("Enter an keyword")

    @dp.message_handler()
    async def specific(message: types.Message):
        keyword = message.text
        key = keyword.lower()
        list_of_files = glob.glob('E:\pythontut\seobot\downloads\documents\*') # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        c = getstr(latest_file)
        c = c.lower()
        e = word_count(c)

        elimination = ['-','is','an','a','the','was','are','were','have','had','has',
                        'been','be','what','where','when','whom','who','whose',
                        'how','to','in','about','i','for','you','him','her','she',
                        'they','them','with','without','say','said','of','and','to',
                        'too','it','that','this','on','do','did','done','at','but',
                        'we','by','can','could','will','would','must','might','as',
                        'go','up','once','upon','your',':',',','.','','he','after',
                        'from','his','during','these','also','known'  ]
        keys = []
        values = []
        items = e.items()
        for item in items:
            keys.append(item[0]), values.append(item[1])
        for a in keys:
            for b in elimination:
                if(a == b):
                    del e[a]
                    break
        if(key in keys):
            ans = e.get(key)
            print(ans)
            await message.answer(ans)
        else:
            await message.answer("Keyword is not found")

@dp.callback_query_handler(text="m7")
async def reply(call:types.CallbackQuery):
    list_of_files = glob.glob('E:\pythontut\seobot\downloads\documents\*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    c = getstr(latest_file)
    c = c.lower()
    e = word_count(c)

    elimination = ['-','is','an','a','the','was','are','were','have','had','has',
                    'been','be','what','where','when','whom','who','whose',
                    'how','to','in','about','i','for','you','him','her','she',
                    'they','them','with','without','say','said','of','and','to',
                    'too','it','that','this','on','do','did','done','at','but',
                    'we','by','can','could','will','would','must','might','as',
                    'go','up','once','upon','your',':',',','.','','he','after',
                    'from','his','during','these','also','known'  ]
    elivalue = [1,2,3]
    keys = []
    values = []
    items = e.items()
    for item in items:
        keys.append(item[0]), values.append(item[1])
    for a in keys:
        for b in elimination:
            if(a == b):
                del e[a]
                break
    sorted_dict = sorted(e.items(),key=lambda x:x[1],reverse=True)
    l = len(sorted_dict)

    for i in range(20,l-1):
        sorted_dict.pop()

    print(sorted_dict)
    result = json.dumps(sorted_dict)
    await call.message.answer(result)

@dp.callback_query_handler(text="m8")
async def reply(call:types.CallbackQuery):
    await call.message.answer("My Operations",reply_markup=keyboard_inline)

@dp.callback_query_handler(text="m10")
async def reply(call:types.CallbackQuery):
    name = call.from_user.first_name
    await call.message.answer(f"Hello {name} how can I help you ? \n\nTo get all my operations type /operations. \n\nMy father : \n\nhttps://t.me/Muthuram0 \n\nTo get more info : \n\n lorem ipsum")

@dp.callback_query_handler(text="m11")
async def reply(call:types.CallbackQuery):
    await call.message.answer("Thank You")

@dp.message_handler(content_types=ContentTypes.DOCUMENT)
async def doc_handler(message: Message):
    print("working...")
    if document := message.document:
        await document.download(
            destination_dir="E:/pythontut/seobot/downloads/",
            # destination_file="file.pdf",
        )
    await message.reply("Choose the operation",reply_markup=keyboard_inline)
    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
