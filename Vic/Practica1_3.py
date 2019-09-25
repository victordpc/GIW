import csv
import re

def buscarPalabras():
    regex1 = r'(\W|^)('
    regex2 = r')(\W|$)'
    resultado = dict()

    texto=open(fichero2,encoding='utf-8').read()
    texto=texto.upper()

    # Limpiamos el texto de entrada
    texto = texto.replace("\n"," ")
    texto = texto.replace(" ","  ")

    with open(fichero1,encoding='utf-8') as origen:
        reader = csv.reader(origen, delimiter=',')

        for lista in reader:
            for palabra in lista:
                palabra= palabra.upper()

                regex = regex1+palabra+regex2

                x = re.findall(regex, texto)
                resultado[palabra]=len(x)
    return resultado

fichero1="vic/file1.csv"
fichero2="vic/file2.txt"

resultado = buscarPalabras()
            
print(resultado)
