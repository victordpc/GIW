def automata(estados, estadosFinales,funcionTransicion, cadena):
    """Implementación de un AFD.
     : estados -> Lista de estados posibles, se asume que el primer estado proporcionado es el inicial.
     : estadosFinales -> Lista de estados finales aceptables.
     : funcionTransicion -> Lista de tuplas con la función de transición entre estados.
     : cadena -> Cadena con la secuencia de datos de entrada.
     
     % Retorno True si se ha llegado a un estado aceptado, False en otro caso."""
    
    # Comprobamos la validez de la entrada
    if not estados or not estadosFinales or not funcionTransicion or not cadena or (estadosFinales not in estados) :
        return False

    return True

estados=(1,2,3)
estadosFinales=(3)
transicion=[[1,"a",2],[1,"b",1],[1,"c",3], [2,"a",1],[2,"b",3],[2,"c",2], [3,"a",3],[3,"b",2],[3,"c",1]]
cadena="abcab"

print(automata(estados,estadosFinales,transicion,cadena))
