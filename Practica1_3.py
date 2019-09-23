import csv

fichero1="file1.csv"
fichero2="file2.txt"


texto=open(fichero2,encoding='utf-8').read()
texto=texto.upper()
# Limpiamos el texto de entrada
texto = texto.replace("\n"," ")
texto = texto.replace(" ","  ")

regex1 = r'(\W|^)('
regex2 = r')(\W|$)'

with open(fichero1,encoding='utf-8') as origen:
    reader = csv.reader(origen, delimiter=',')

    for lista in reader:
        for palabra in lista:
            palabra= palabra.upper()

            regex = regex1+palabra+regex2



cadena = "bienvenido aaplicación mimi mi".capitalize() 
print (cadena.count("mi") )
print (cadena.find("mi",0) )
 
print (cadena.find("mi", 0, 10) )
print (cadena.find("mi", 14) )
