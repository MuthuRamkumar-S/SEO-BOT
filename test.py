import os
import string
import docx2txt
import PyPDF2
import glob
import pathlib
import re

list_of_files = glob.glob('E:\pythontut\seobot\downloads\documents\*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)

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
            pageObj = pdfreader.getPage(0)
            my_text = pageObj.extractText()
            return my_text
    elif(ext == ".txt"):
        print("txt file")

def word_count(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts

c = getstr(latest_file)
count = 0
c = c.lower()
e = word_count(c)
sorted_dict = sorted(e.items(),key=lambda x:x[1])
print(e)
print("\n\n\nThe Sorted Dict \n\n\n\n")
print(sorted_dict)
word_list = c.split(" ")
d = len(word_list)