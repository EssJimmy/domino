# Documentación del código

# Métodos de minimax
## Minimax estándar
Función principal de Minimax, regresa el valor heurístico calculado por la función y una copia de la ficha que vamos a tirar. También nos ayuda a saber cuantas piezas tenemos nosotros y cuántas tiene el oponente, lo cual es para saber quien va ganando. Toma como parámetro la profundidad máxima que se va a recorrer, para evitar que se vaya a cosas como las combinaciones de 7 en 21 que serían aproximadamente 116,280 casos.

```python
def miniMaxInicia(profundidad):
    print("Entra a minimax")
    copia = juego.copiaNodo(juego.nodo)
    valorHeuristico, copia = miniMax(copia, profundidad, True)
    print("Valor heurístico del nodo actual: {}".format(valorHeuristico))
    copia.imprimeTodo()
    print("Sale de minimax")

    return valorHeuristico, copia
    
    
def miniMax(nodo, profundidad, maximiza):
    sucesores, valorHeuristico = juego.listaSucesores(nodo, maximiza)
    #Si entra aqui es estado final
    if len(sucesores) == 0:
        #print("Sin sucesores")
        return valorHeuristico, nodo
    
    #Entra aqui sólo si la profundidad es cero
    if profundidad == 0:
        #print("Sin profundidad")
        return juego.funcionHeuristica(nodo), nodo
        
    if maximiza:
        mejorValor = -1001
        mejorNodo = None
        for s in sucesores:
            valor, nodoBasura = miniMax(s, profundidad - 1, False)
            if valor > mejorValor:
                mejorValor = valor
                mejorNodo = s
        #Regresamos el mejor sucesor para regresarlo en la llamada inicial
        #print("Maximiza\tProfundidad: {}\tValor: {}".format(\
        #                    profundidad, mejorValor))
        return mejorValor, mejorNodo
    else:
        mejorValor = 1001
        for s in sucesores:
            valor, nodoBasura = miniMax(s, profundidad - 1, True)
            if valor < mejorValor:
                mejorValor = valor
        #No regresamos el nodo sucesor, sino el actual
        #De otra manera se regresaría el nodo hoja con mayor valor pero 
        #no sabríamos cómo llegar a el
        #print("Maximiza\tProfundidad: {}\tValor: {}".format(\
        #                    profundidad, mejorValor))
        return mejorValor, nodo
```

### Funciones auxiliares a minimax estándar

**Lista sucesores:**

Revisa la lista de adyacencia del nodo al que estamos explorando.

```python
def listaSucesores(self, nodo, jugador):
        res = list()
        #Si gana TumbaFichas
        if len(nodo.mano) == 0:
            #valor de la función heurística: 1000
            return res, 1000
        #Si gana el oponente
        if nodo.manoOponente == 0:
            return res, -1000
        if jugador:
            for f in nodo.mano:
                self.agregaSucesorMano(nodo, f, res)        
            if len(res) == 0:
                self.agregaSucesorSopa(nodo, res)
        else:
            self.agregaSucesorOponente(nodo, res)
        return res, 0
```

**Agrega sucesor sopa:**

Agrega el sucesor del nodo a la sopa de fichas.
```python
def agregaSucesorSopa(self, nodo, lista):
        n1,n2 = nodo.numJugables[0], nodo.numJugables[1]
        copia = None
        for f in nodo.sopa:
            if f is not None:
                f1, f2 = f.getNums()
                b = [n1 == f1, n1 == f2, n2 == f1, n2 == f2]
                if any(b):
                    if b[0]:
                        copia = self.copiaNodo(nodo)
                        copia.numJugables[0] = f2
                        copia.sopa[self.indicesFichas[f1][f2]] = None
                        lista.append(copia)
                    if b[1] and not b[0]:
                        copia = self.copiaNodo(nodo)
                        copia.numJugables[0] = f1
                        copia.sopa[self.indicesFichas[f1][f2]] = None
                        lista.append(copia)   
                    if b[2] and not b[0]:
                        copia = self.copiaNodo(nodo)
                        copia.numJugables[1] = f2
                        copia.sopa[self.indicesFichas[f1][f2]] = None
                        lista.append(copia)
                    if b[3] and not b[1] and not b[2]:
                        copia = self.copiaNodo(nodo)
                        copia.numJugables[1] = f1
                        copia.sopa[self.indicesFichas[f1][f2]] = None
                        lista.append(copia)  
 ```
 
 **Agrega sucesor oponente:**
 
 ```python                       
    def agregaSucesorOponente(self, nodo, lista):
        n1,n2 = nodo.numJugables[0], nodo.numJugables[1]
        copia = None
        for f in nodo.sopa:
            if f is not None:
                f1, f2 = f.getNums()
                b = [n1 == f1, n1 == f2, n2 == f1, n2 == f2]
                if any(b):
                    if b[0]:
                        copia = self.copiaNodo(nodo)
                        copia.numJugables[0] = f2
                        copia.sopa[self.indicesFichas[f1][f2]] = None
                        copia.manoOponente -= 1 
                        lista.append(copia)
                    if b[1] and not b[0]:
                        copia = self.copiaNodo(nodo)
                        copia.numJugables[0] = f1
                        copia.sopa[self.indicesFichas[f1][f2]] = None
                        copia.manoOponente -= 1
                        lista.append(copia)   
                    if b[2] and not b[0]:
                        copia = self.copiaNodo(nodo)
                        copia.numJugables[1] = f2
                        copia.sopa[self.indicesFichas[f1][f2]] = None
                        copia.manoOponente -= 1
                        lista.append(copia)
                    if b[3] and not b[1] and not b[2]:
                        copia = self.copiaNodo(nodo)
                        copia.numJugables[1] = f1
                        copia.sopa[self.indicesFichas[f1][f2]] = None
                        copia.manoOponente -= 1
                        lista.append(copia)
```

**Copia nodo:**

Copia un nodo del árbol de búsqueda al atributo llamado Nodo, que es parte de la clase Ficha
```python
    def copiaNodo(self, nodo):
        copia = self.Nodo(nodo.sopa.copy(),\
                          nodo.mano.copy(),\
                          nodo.manoOponente,\
                          nodo.numJugables.copy(),\
                          nodo.faltaOponente.copy(),\
                          nodo.faltaMano.copy(),\
                          nodo.probabilidad)
        return copia
```

## Minimax a profundidad limitada con casos
En esta versión de minimax, el árbol de búsqueda está mucho más limitado debido a la información que tenemos a la mano, los casos utilizados son los siguientes:

*  Presencia de las fichas en la sopa.
*  Presencia de las fichas jugadas.
*  Conocimiento de si el oponente comió o no comió fichas.
*  Cantidad de fichas en nuestra mano que contienen dicho número.

Todo esto ayuda a reducir el árbol, pero también viene con mucho peso en memoria, al utilizar múltiples ciclos y decisiones, por lo que se decidió limitar su profundidad a solo 2 movimientos, que serían el nivel 0, el nivel 1 y el nivel 2 del árbol. Se decidió no utilizar este método por el problema que representaba su implementación, así como el no ser capaz de mirar a una profundidad mayor a 2.
    
```python
def juega_ficha(mano: set, probs: dict, mejor_tirada: dict, extremos: list):
    # inicializa un arreglo de las peores jugadas posibles que puede tirar el oponente
    peores_jugadas = []
    
    # un boolean para saber cuando hayamos encontrado la ficha 'perfecta' a jugar
    found = False
    
    """
    revisamos si tenemos alguna ficha en nuestra mano que sea posible tirar, si no existe
    entonces llamamos a la función come_ficha
    """
    if mejor_tirada[extremos[0]] == 0 and mejor_tirada[extremos[1]] == 0:
        come_ficha()
        return
    
    # si un extremo no se encuentra, pero el otro sí, trabajamos sobre el extremo que tenemos
    elif mejor_tirada[extremos[0]] == 0:
        min_llave_tirada = extremos[1]
        extremo = 1

    elif mejor_tirada[extremos[1]] == 0:
        min_llave_tirada = extremos[0]
        extremo = 0

    """
    si se encuentran ambos extremos en nuestra mano, vemos cual es el peor extremo que puede
    tirar el oponente y lo tomamos en consideración
    """
    else:    
        min_valor_tirada = min((mejor_tirada[extremos[0]], mejor_tirada[extremos[1]]))
        for key, value in mejor_tirada:
            if value == min_valor_tirada:
                min_llave_tirada = int(key)
                extremo = 1

                if extremos[0] == key:
                    extremo = 0

                break
    
    # llenamos el arreglo de las peores jugadas que nos pueden hacer
    for ficha in probs:
        """
        si la probabilidad de que el oponente pueda tener la ficha es nula, no lo añadimos, sabemos
        un oponente no tiene una ficha, o algún número en específico si tuvo que comer
        """
        if min_llave_tirada in ficha and probs[ficha]:
            peores_jugadas.append(ficha)

    # creamos una copia del árbol que contiene la probabilidad de que el oponente tenga dicha ficha
    aux = probs
    while (not found) and len(aux) > 0:
        # encontramos el valor máximo que se refiere a la peor jugada que nos puede hacer
        max_key1 = max(zip(aux.values(), aux.keys()))[1]
        aux2 = aux
        del aux2[max_key1] 
    
        # vamos buscando hasta que encontremos un valor en formato #-# que se encuentre en nuestra mano
        for i in range(len(aux)):
            max_key2 = max(zip(aux2.values(), aux2.keys()))[1]
            
            # revisamos que el valor exista en nuestra mano
            if ((max_key1, max_key2) in mano or (max_key2, max_key1) in mano) and ((max_key1, max_key2) in peores_jugadas or (max_key2, max_key1) in peores_jugadas):
                # revisamos en que extremo lo tenemos que tirar y lo hacemos
                if max_key1 in extremos:
                    index = extremos.index(max_key1)
                    extremos[index] = max_key2
                    

                elif max_key2 in extremos:
                    index = extremos.index(max_key2)
                    extremos[index] = max_key1
                   
                found = True

                if (max_key1, max_key2) in mano:
                    ficha = (max_key1, max_key2)    
                elif (max_key2, max_key1) in mano:
                    ficha = (max_key2, max_key1)

                # quitamos la ficha de nuestra mano
                mano.remove(ficha)
                return
            
            # si no encontramos, ninguna ficha, quitamos el segundo valor más alto y volvemos a iniciar
            del aux2[max_key2]
        
        # si no encontramos combinaciones con max_key1 validas, quitamos el valor y volvemos a empezar
        del aux[max_key1]
    """
    si no pudimos hacer nada de lo anterior, pero sabemos que tenemos un valor en el otro extremo volvemos a iniciar, pero ahora los casos
    son todavia mas limitados
    """
    if extremo == 0:
        extremo = 1
    else:
        extremo = 0

    aux_mano = mano
    for ficha in aux_mano:
        if extremos[extremo] in ficha:
            if extremos[extremo] == ficha[0]:
                extremos[extremo] == ficha[1]
            else:
                extremos[extremo] == ficha[0]
            
            mano.remove(ficha)
            return
```