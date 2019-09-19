
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


def automata(estados, estadosFinales, funcionTransicion, cadena, inicial):
    """Implementación de un AFD.
     : estados -> Lista de estados posibles.
     : estadosFinales -> Lista de estados finales aceptables.
     : funcionTransicion -> Lista de tuplas con la función de transición entre estados.
     : cadena -> Cadena con la secuencia de datos de entrada.
     : inicial -> Estado inicial del automata.

     % Retorno -> True si se ha llegado a un estado aceptado, False en otro caso."""

    # Comprobamos la validez de la entrada
    if not estados or not estadosFinales or not funcionTransicion or not cadena or (estadosFinales not in estados):
        return False

    # Tratamos la entrada
    transicion = tratarFuncionTransicion(funcionTransicion)

    actual = inicial
    seguir = True
    indice = 1
    resultado = True

    while(resultado and seguir):
        entrada = cadena[indice-1:indice]
        len(cadena)

        if actual not in transicion or entrda not in transicion[actual]:
            resultado = False
            continue

        actual = transicion[actual][entrada]

        indice += 1
        if indice > len(cadena):
            seguir = False
            resultado = False

    print(funcionTransicion)
    return resultado and actual in estadosFinales


estados = (1, 2, 3)
estadosFinales = (3)
transicion = [[1, "a", 2], [1, "b", 1], [1, "c", 3], [2, "a", 1],
              [2, "b", 3], [2, "c", 2], [3, "a", 3], [3, "b", 2], [3, "c", 1]]
cadena = "abcab"
inicial = 1

print(automata(estados, estadosFinales, transicion, cadena, inicial))
