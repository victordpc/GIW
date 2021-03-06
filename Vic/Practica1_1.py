
def tratarFuncionTransicion(original):
    """Tratamiento de una colección de tuplas de tres elementos para generar un diccionario de diccionarios usando como 
    clave para el primer diccionario el primer elemento, clave para el segundo diccionario el segundo elemento y valor 
    el tercer elemento
    """
    resultado = dict()

    for funcion in original:
        if funcion[0] in resultado:
            (resultado[funcion[0]])[funcion[1]] = funcion[2]
        else:
            resultado[funcion[0]] = {funcion[1]: funcion[2]}

    return resultado


def ejecutarAutomata(inicial, cadena, transicion):
    """Ejecución de un AFD"""
    actual = inicial
    seguir = True
    indice = 1
    resultado = True

    while(resultado and seguir):
        entrada = cadena[indice-1:indice]

        if actual not in transicion or entrada not in transicion[actual]:
            resultado = False
        else:
            actual = transicion[actual][entrada]

            indice += 1
            if indice > len(cadena):
                seguir = False
    return resultado, actual


def automata(estados, estadosFinales, funcionTransicion, cadena, inicial):
    """Implementación de un AFD.
     : estados -> Lista de estados posibles.
     : estadosFinales -> Lista de estados finales aceptables.
     : funcionTransicion -> Lista de tuplas con la función de transición entre estados.
     : cadena -> Cadena con la secuencia de datos de entrada.
     : inicial -> Estado inicial del automata.

     % Retorno -> True si se ha llegado a un estado aceptado, False en otro caso."""

    # Comprobamos la validez de la entrada
    # or (estadosFinales not in estados):
    if not estados or not estadosFinales or not funcionTransicion or not cadena:
        return False

    # Tratamos la entrada
    transicion = tratarFuncionTransicion(funcionTransicion)

    # Ejecutamos el automata
    resultado, actual = ejecutarAutomata(inicial, cadena, transicion)

    alida = ""
    if not resultado:
        salida = "Se ha producido un error con los datos proporcionados"
    elif actual in estadosFinales:
        salida = "Cadena válida"
    else:
        salida = "Cadena invalida"

    return salida.decode()


estados = [1, 2, 3]
estadosFinales = [3]
transicion = [[1, "a", 2], [1, "b", 1], [1, "c", 3], [2, "a", 1],
              [2, "b", 3], [2, "c", 2], [3, "a", 3], [3, "b", 2], [3, "c", 1]]
cadena = "abcab"
inicial = 1

print(automata(estados, estadosFinales, transicion, cadena, inicial))
