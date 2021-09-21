import PyPDF2
import csv


pdfFileObj = open("listapresenca_DCT1101_13072021.pdf", "rb")
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
numPages = pdfReader.numPages

print("Páginas:",numPages)

pageObj = pdfReader.getPage(0)
text = pageObj.extractText()

start = text.find("ASSINATURA") + len("ASSINATURA")
print("Posição:", start)

end = text.rfind("Página")
print("Posição:", end)

text = text[start:end]

print()
print(text)
print()

wordList = []
word = ''
previous = " "
for letter in text:
	if previous.isalpha() or previous.isspace():
		typePrevious = True
	else:
		typePrevious = False
	if letter.isalpha() or letter.isspace():
		typeCurrent = True
	else:
		typeCurrent = False

	if typePrevious == typeCurrent:
		word += letter
	else:
		wordList += [word]
		word = letter

	previous = letter
wordList += [word]

print()
print(wordList)

students = {}
numStudents = len(wordList) // 2

for i in range(numStudents):
	name = wordList[2*i]
	matr = wordList[2*i+1]
	if i < 9:
		matr = matr[:-1]
	else:
		matr = matr[:-2]
	students[matr] = name

print()

for stud in students:
	print(stud, students[stud])

print()

# Obtém dados de presença

signatures = {}
with open('DCT1101 ALP.csv', encoding='utf-8') as fileCSV:
  reader = csv.DictReader(fileCSV, delimiter=',')
  for row in reader:
    code = len(signatures) + 1
    if code not in signatures:
      signatures[code] = row

print("Datas")
attendance = {}
for row in signatures:
  date = signatures[row]['Carimbo de data/hora'][:10]
  student = signatures[row]['Matrícula']
  print(date)
  print(student)
  if date not in attendance:
    attendance[date] = []
  attendance[date].append(student)

print()
print("Frequência Final - Alunos Ausentes")
print()
for date in attendance:
  file_name = date.replace('/', '')
  file_name = file_name[4:8] + '_' + file_name[2:4] + '_' + file_name[0:2]
  file_name = file_name + ".txt"
  date_file = open(file_name, "wt")
  date_file.write("Algoritmos e Lógica de Programação - 2021.1\n")
  date_file.write("Lista de Frequência - ")
  date_file.write(file_name[:-4])
  date_file.write("\n")
  date_file.write("\nPresentes\n")
  for stud in students:
    if stud in attendance[date]:
      date_file.write(students[stud])
      date_file.write("\n")
  date_file.write("\nAusentes\n")
  for stud in students:
    if stud not in attendance[date]:
      date_file.write(students[stud])
      date_file.write("\n")
  date_file.close()
