import textstat
import PyPDF2

pdffileobj=open("C:/Users/LENOVO/Downloads/test.pdf",'rb')
pdfreader=PyPDF2.PdfFileReader(pdffileobj)
x=pdfreader.numPages
print(x)
my_text=''
for i in range(0,x):
    pageObj = pdfreader.getPage(i)
    a = pageObj.extractText()
    my_text = my_text+a

x = textstat.flesch_reading_ease(my_text)
y = textstat.flesch_kincaid_grade(my_text)
print(x)
print(y)

if(x>=95):
    print("Score is 95%")
elif(90<= x <95):
    print("score is 90%")
elif(85<= x <90):
    print("score is 85%")
elif(80<= x <85):
    print("score is 80%")
elif(75<= x <80):
    print("score is 75%")
elif(70<= x <75):
    print("score is 70%")
elif(65<= x <70):
    print("score is 65%")
elif(60<= x <65):
    print("score is 60%")
elif(55<= x <60):
    print("score is 55%")
elif(50<= x <55):
    print("score is 50%")
elif(40<= x <50):
    print("score is 40%")
elif(30<= x <40):
    print("score is 30%")
elif(20<= x <30):
    print("score is 20%")
elif(10<= x <20):
    print("score is 10%")
elif(0<= x <10):
    print("score is less than 10%")
else:
    print("undecidable")