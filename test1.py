import docx2txt
import PyPDF2
import glob
import pathlib

pdffileobj=open("C:/Users/LENOVO/Downloads/test.pdf",'rb')
pdfreader=PyPDF2.PdfFileReader(pdffileobj)
x=pdfreader.numPages
print(x)
my_text=''
for i in range(0,x):
    pageObj = pdfreader.getPage(i)
    a = pageObj.extractText()
    my_text = my_text+a
print(my_text)