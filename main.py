# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 13:09:46 2023

@author: Luis Rojas, Jaime Perez, Anthoan Juarez 
"""

#%%Manual de usuario
"""
Se deben correr todos los módulos en el orden en que aparecen 
En en módulo "Inicia Juego", en la linea juego = Domino() se puede modificar
por juego = Domino(True), lo cual inicia una partida preestablecida que se utilizó para
provar y depurar
En caso de que se inicie el juego sin esta modificación, se pedirán las fichas de la mano
Para dar una ficha, se debe dar el formato "# #" y enter, donde # es un entero entre 0 y 6
y forzosamente separados por un espacio. Este formato aplica cada que en pantalla aparezca
"Dar ficha: "
Al recibir su mano, el programa preguntará qué jugador empieza. Si se da "1" y enter
Iniciará el oponente. Si se da cualquier otra cosa, empezará el programa.

TUMBAFICHAS JUEGA
El programa, de tener un sólo movimiento posible, imprimirá "MOVIMIENTO FORZADO".
Si no tiene fichas jugables, se le pedirá al usuario ingresar las fichas que esté comiendo
hasta obtener una que pueda jugar.
Si tiene más de un movimiento posible, llamará a la función minimax_inicia y jugará la ficha
que lo lleve al nodo que maximiza su función heurística.
En cualquier caso, imprimirá la ficha que jugó y la información del nodo resultante.

OPONENTE JUEGA
El programa preguntará si el oponente come o no fichas
En caso de que sí coma, se debe dar "1" y enter. En caso de que no coma, se debe dar
"2" y enter. Cualquier otra entrada puede llevar a un mal funcionamiento del programa.
Si el oponente come, debe darse "1" y enter por cada ficha que se comió, incluida
la ficha que se jugó.
Cuando el oponente terminó de comer, o si no comió en primer lugar, se pedirá al 
usuario que ingrese la ficha con el formato mencionado anteriormente.
En caso de que la ficha pueda jugarse en ambos extremos, se imprimirán ambos extremos
y "1.Izquierda, 2.Derecha: ". El usuario deberá dar "1" o "2" y enter, de acuerdo
a qué extremo se eligió. 
Ejemplo:
    OPONENTE JUEGA
    1.Oponente come 2.Oponente no come:: 2
    Dar ficha :: 0 2
    (0,2)
    Numeros Jugables: [0,2]
    1.Izquierda, 2.Derecha: 1  --- Es decir, se jugó del lado del 0
    ...
    Numeros Jugables: [2,2]
    
"""
#%%Import
import time
import math

#%%miniMax
def minimax_inicia(profundidad):
    print("Entra a minimax")
    copia = juego.copia_nodo(juego.nodo)
    valor_heuristico, copia = minimax(copia, profundidad, True)
    print("Valor heurístico del nodo actual: {}".format(valor_heuristico))
    copia.imprime_todo()
    print("Sale de minimax")
    return valor_heuristico, copia
    
    
def minimax(nodo, profundidad, maximiza):
    sucesores, valor_heuristico = juego.lista_sucesores(nodo, maximiza)
    #Si entra aqui es estado final
    if len(sucesores) == 0:
        #print("Sin sucesores")
        return valor_heuristico, nodo
    #Entra aqui sólo si la profundidad es cero
    if profundidad == 0:
        #print("Sin profundidad")
        return juego.funcion_heuristica(nodo), nodo
    if maximiza:
        mejor_valor = -1001
        mejor_nodo = None
        for s in sucesores:
            valor, nodo_basura = minimax(s, profundidad - 1, False)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_nodo = s
        #Regresamos el mejor sucesor para regresarlo en la llamada inicial
        #Regresamos el mejor valor de la lista de movimientos posibles
        #si tenemos que comer habrá problemas pero no tenemos control sobre eso
        #de cualquier manera ya que serán movimientos forzados y no se llama 
        #a minimax en dichos casos
        return mejor_valor, mejor_nodo
    
    else:
        suma = 0
        for s in sucesores:
            valor, nodo_basura = minimax(s, profundidad - 1, True)
            suma += valor
        #No regresamos el nodo sucesor, sino el actual
        #De otra manera se regresaría el nodo hoja con mayor valor pero 
        #no sabríamos cómo llegar a el
        #Regresamos la suma de los valores ya que es incierto si el oponente 
        #tendrá oportunidad de jugar ciertas fichas. Buscamos regresar un valor
        #esperado si se alcanza cierto estado.
        return suma/len(sucesores), nodo
                


#%%Clase Domino
#Queremos poder jugar siempre llamando al objeto domino, nada de funciones 
#externas
class Domino:
    indices_fichas = [[0, 1,  2,  3,  4,  5,  6],
                     [1, 7,  8,  9,  10, 11, 12],
                     [2, 8,  13, 14, 15, 16, 17],
                     [3, 9,  14, 18, 19, 20, 21],
                     [4, 10, 15, 19, 22, 23, 24],
                     [5, 11, 16, 20, 23, 25, 26],
                     [6, 12, 17, 21, 24, 26, 27]]
    
    combinaciones = [[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [1,3,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [1,4,6,4,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [1,5,10,10,5,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [1,6,15,20,15,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [1,7,21,35,35,21,7,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [1,8,28,56,70,56,28,8,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [1,9,36,84,126,126,84,36,9,1,0,0,0,0,0,0,0,0,0,0,0,0],
                     [1,10,45,120,210,252,210,120,45,10,1,0,0,0,0,0,0,0,0,0,0,0],
                     [1,11,55,165,330,462,462,330,165,55,11,1,0,0,0,0,0,0,0,0,0,0],
                     [1,12,66,220,495,792,924,792,495,220,66,12,1,0,0,0,0,0,0,0,0,0],
                     [1,13,78,286,715,1287,1716,1716,1287,715,286,78,13,1,0,0,0,0,0,0,0,0],
                     [1,14,91,364,1001,2002,3003,3432,3003,2002,1001364,91,14,1,0,0,0,0,0,0,0],
                     [1,15,105,455,1365,3003,5005,6435,6435,5005,3003,1365,455,105,15,1,0,0,0,0,0,0],
                     [1,16,120,560,1820,4368,8008,11440,12870,11440,8008,4368,1820,560,120,16,1,0,0,0,0,0],
                     [1,17,136,680,2380,6188,12376,19448,24310,24310,19448,12376,6188,2380,680,136,17,1,0,0,0,0],
                     [1,18,153,816,3060,8568,18564,31824,43758,48620,43758,31824,18564,8568,3060,816,153,18,1,0,0,0],
                     [1,19,171,969,3876,11628,27132,50388,75582,92378,92378,75582,50388,27132,11628,3876,969,171,19,1,0,0],
                     [1,20,190,1140,4845,15504,38760,77520,125970,167960,184756,167960,125970,77520,38760,15504,4845,1140,190,20,1,0],
                     [1,21,210,1330,5985,20349,54264,116280,203490,293930,352716,352716,293930,203490,116280,54264,20349,5985,1330,210,21,1]]
    
    def __init__(self, pred = False):
        self.nodo = self.Nodo([],set(), 7, [-1,-1], set(), set(), 1, 7)
        self.inicializa_sopa()
        print("INICIA JUEGO")

        if pred:
            self.mano_predeterminada()
        else:
            self.dar_mano()

        self.jugador = self.pide_jugador()
        self.continua = True
            
    class Ficha:

        def __init__(self, n1, n2):
            self.num=[]
            self.num.append(n1)
            self.num.append(n2)


        def __str__(self):
            return "(" + str(self.num[0]) + "," + str(self.num[1]) + ")"
        

        #def __eq__(self,otro):
           # return self.num[0] == otro.num[0] and self.num[1] == otro.num[1]


        def tiene_num(self, n):
            return self.num[0] == n or self.num[1] == n
            
            
        def get_nums(self):
            return self.num[0], self.num[1]
    
    class Nodo:

        def __init__(self, sopa, mano, mano_oponente, num_jugables,\
                     falta_oponente, falta_mano, probabilidad, nMano):
            self.sopa = sopa
            self.mano_oponente = mano_oponente
            self.mano = mano
            self.num_jugables = num_jugables
            self.falta_oponente = falta_oponente
            self.falta_mano = falta_mano
            self.probabilidad = probabilidad
            self.nMano = nMano


        def imprime_sopa(self):
            s = ""

            for i in self.sopa:
                if i is not None:
                    s += i.__str__() +", "
            print(s)


        def imprime_mano(self):
            s = ""

            for i in self.mano:
                s += i.__str__() +", "
            print(s)


        def imprime_todo(self):
            print("Sopa:")
            self.imprime_sopa()
            print("Mano:")
            self.imprime_mano()
            print("#Fichas del Oponente: {0}\nNumeros Jugables: [{1},{2}]\n"\
                  .format(self.mano_oponente,\
                          self.num_jugables[0], self.num_jugables[1]))
                

    def copia_nodo(self, nodo):
        copia = self.Nodo(nodo.sopa.copy(),\
                          nodo.mano.copy(),\
                          nodo.mano_oponente,\
                          nodo.num_jugables.copy(),\
                          nodo.falta_oponente.copy(),\
                          nodo.falta_mano.copy(),\
                          nodo.probabilidad,\
                          nodo.nMano)
        return copia
            

    def inicializa_sopa(self):
        for i in list(range(0,7)):
            for j in range(i,7):
                f = self.Ficha(i,j)
                self.nodo.sopa.append(f)


    def dar_mano(self):
        while len(self.nodo.mano) < 7:
            self.dar_ficha()


    def dar_ficha(self):
        f = self.quitar_ficha()
        if f is None:
            return None
        self.nodo.mano.add(f)
        print("Ficha agregada")


    def quitar_ficha(self):
        i, j = self.recibe_numeros()
        if i is None:
            return None
        f = self.nodo.sopa[self.indices_fichas[i][j]]
        if f is None:
            print("Ficha no disponible")
            return None
        self.nodo.sopa[self.indices_fichas[i][j]] = None
        return f


    #Para dar una ficha, se manda "n m"
    #n y m deben ser enteros entre 0 y 6. Debe haber un espacio entre ellos
    def recibe_numeros(self):
        inp = input("Dar ficha :: ")

        if len(inp) != 3:
            print("Formato incorrecto")
            return None, None
        
        i = int(ord(inp[0]))-48
        t = inp[1]
        j = int(ord(inp[2]))-48

        if t != " ":
            print("Formato incorrecto")
            return None , None
        
        if not(0<=i<=6) or not(0<=j<=6):
            print("Numero incorrecto")
            #darFicha()
            return None , None
        
        return i , j
        

    #%Dar mano predeterminada 
    def mano_predeterminada(self):
        if len(self.nodo.mano) != 0:
            return 
        self.nodo.mano.add(self.Ficha(1,2))
        self.nodo.mano.add(self.Ficha(3,3))
        self.nodo.mano.add(self.Ficha(4,5))
        self.nodo.mano.add(self.Ficha(0,0))
        self.nodo.mano.add(self.Ficha(6,6))
        self.nodo.mano.add(self.Ficha(0,3))
        self.nodo.mano.add(self.Ficha(2,6))
        self.nodo.sopa[self.indices_fichas[1][2]] = None
        self.nodo.sopa[self.indices_fichas[3][3]] = None
        self.nodo.sopa[self.indices_fichas[4][5]] = None
        self.nodo.sopa[self.indices_fichas[0][0]] = None
        self.nodo.sopa[self.indices_fichas[6][6]] = None
        self.nodo.sopa[self.indices_fichas[0][3]] = None
        self.nodo.sopa[self.indices_fichas[2][6]] = None
        
    def decide_lado(self):
        cont = True

        while cont:
            print("Numeros Jugables: [{0},{1}]".format(\
                  self.nodo.num_jugables[0], self.nodo.num_jugables[1]))
            inp = input("1.Izquierda, 2.Derecha: ")

            if not(inp == "1" or inp == "2"):
                print("Respuesta inváida")

            else:
                cont = False

        return inp
        

    def jugar_ficha(self, ficha, lado = None):
        if not isinstance(ficha, self.Ficha):
            print("eso no es una ficha padrino")    
            return False
        
        n0 = ficha.num[0]
        n1 = ficha.num[1]
        j0 = self.nodo.num_jugables[0]
        j1 = self.nodo.num_jugables[1]

        if j0 == -1:
            self.nodo.num_jugables[0] = n0
            self.nodo.num_jugables[1] = n1
            return True
        
        b = [j0 == n0, j0 == n1, j1 == n0, j1 == n1]
        
        if not any(b):
            print("Ficha injugable padrino")
            self.nodo.sopa[self.indices_fichas[n0][n1]] = ficha
            return False
        
        if b[0] and b[2]:
            self.nodo.num_jugables[1] = n1
            return True
        
        if b[1] and b[3]:
            self.nodo.num_jugables[1] = n0
            return True
        
        if (b[1] and b[2]) or (b[0] and b[3]):
            if lado == None:
                lado = self.decide_lado()

            if lado == "1":
                if b[0]:
                    self.nodo.num_jugables[0] = n1
                else:
                    self.nodo.num_jugables[0] = n0

            else:
                if b[2]:
                    self.nodo.num_jugables[1] = n1
                else:
                    self.nodo.num_jugables[1] = n0

            return True
        
        if b[0]:
            self.nodo.num_jugables[0] = n1
        if b[1]:
            self.nodo.num_jugables[0] = n0
        if b[2]:
            self.nodo.num_jugables[1] = n1
        if b[3]:
            self.nodo.num_jugables[1] = n0

        return True


    def imprime_todo(self):
        self.nodo.imprime_todo()


    def pide_jugador(self):
        jugador = input("1.Oponente Inicia 2.TumbaFichas Inicia:: ")

        return not jugador == "1"
        

    def inicia_turno(self):
        continua_turno = True

        if self.jugador == False:
            print("OPONENTE JUEGA")

            while continua_turno:
                inp = input("1.Oponente come 2.Oponente no come:: ")

                if inp[0] == "1":
                    if sum(f is None for f in self.nodo.sopa)\
                        == 28 - self.nodo.mano_oponente:
                        print("JUEGO TERMINADO: EMPATE!!")
                        self.continua = False
                        continua_turno = False
                    self.nodo.mano_oponente += 1

                else:
                    f = None
                    while f is None:
                        f = self.quitar_ficha()
                    print(f)
                    bien_jugado = self.jugar_ficha(f)

                    if bien_jugado:
                        self.nodo.mano_oponente -= 1
                        continua_turno = False

                        if self.nodo.mano_oponente == 0:
                            print("JUEGO TERMINADO: OPONENTE GANA!!")
                            self.continua = False

            self.jugador = True

        else:
            print("TUMBAFICHAS JUEGA")
            n1 = self.nodo.num_jugables[0]
            n2 = self.nodo.num_jugables[1]
            lado = None
            while continua_turno:
                copia = set()
                fichas_jugables = set()

                for f in self.nodo.mano:
                    f1, f2 = f.get_nums()

                    if f1 == n1 or f1== n2 or f2 == n1 or f2 == n2 or n1 == -1:
                        fichas_jugables.add(f)

                    else:
                        copia.add(f)
                        
                if len(fichas_jugables) != 0:
                    if len(fichas_jugables) == 1:
                        f = fichas_jugables.pop()
                        f1, f2 = f.get_nums()

                        #Caso donde una ficha se puede jugar en ambos lados
                        if ((f1 == n1 and f2 == n2)or (f1 == n2 and f2 == n1))\
                                    and n1 != n2:
                            start_time = time.time()
                            valor_heuristico, mejor_nodo = minimax_inicia(self.profundidad())
                            print(time.time() - start_time)
                            f, lado = self.encuentra_transicion(self.nodo, mejor_nodo)
                            
                        else:
                            print("MOVIMIENTO FORZADO")

                    else:
                        #Llamar a minMax
                        #Pon la profundidad como parametro!! >:(
                        start_time = time.time()
                        valor_heuristico, mejor_nodo = minimax_inicia(self.profundidad())
                        print(time.time() - start_time)
                        #Necesitamos elegir la ficha y el lado
                        #Crear una funcion que recibe dos nodos, padre e hijo
                        #La función regresa la ficha y lado i.e. la transición
                        #Sacar esa ficha de fichasJugables
                        f, lado = self.encuentra_transicion(self.nodo, mejor_nodo)
                        fichas_jugables.remove(f)
                        copia.update(fichas_jugables)
                    print(f)
                    self.nodo.mano = copia
                    self.jugar_ficha(f,lado)
                    self.nodo.nMano -= 1 
                    continua_turno = False

                    if len(self.nodo.mano) == 0:
                        print("JUEGO TERMINADO: TUMBAFICHAS 5000 GANA!!")
                        self.continua = False

                else:
                    if sum(f is None for f in self.nodo.sopa)\
                            == 28 - self.nodo.mano_oponente:
                        print("JUEGO TERMINADO: EMPATE!!")
                        self.continua = False
                        continua_turno = False

                    else:
                        print("A pastar")
                        self.dar_ficha()
                        self.nodo.nMano += 1

            self.jugador = False
        

    def agrega_sucesor_mano(self, nodo: Nodo, ficha: Ficha, lista):
        n1,n2 = nodo.num_jugables[0], nodo.num_jugables[1]
        copia = None
        f1, f2 = ficha.get_nums()
        b = [n1 == f1, n1 == f2, n2 == f1, n2 == f2]

        if any(b):
            if b[0]:
                copia = self.copia_nodo(nodo)
                copia.num_jugables[0] = f2
                copia.mano.remove(ficha)
                copia.nMano -= 1
                lista.append(copia)

            if b[1] and not b[0]:
                copia = self.copia_nodo(nodo)
                copia.num_jugables[0] = f1
                copia.mano.remove(ficha)
                copia.nMano -= 1
                lista.append(copia)

            if b[2] and not b[0]:
                copia = self.copia_nodo(nodo)
                copia.num_jugables[1] = f2
                copia.mano.remove(ficha)
                copia.nMano -= 1
                lista.append(copia)

            if b[3] and not b[1] and not b[2]:
                copia = self.copia_nodo(nodo)
                copia.num_jugables[1] = f1
                copia.mano.remove(ficha)
                copia.nMano -= 1
                lista.append(copia)

                
        if n1 == -1:
            copia = self.copia_nodo(nodo)
            copia.num_jugables[0] = f1
            copia.num_jugables[1] = f2
            copia.mano.remove(ficha)
            copia.nMano -= 1
            lista.append(copia)

            
            
    #Falta cambiar la probabilidad del nodo y los numeros no jugables
    def agrega_sucesor_sopa(self, nodo: Nodo, lista):
        n1,n2 = nodo.num_jugables[0], nodo.num_jugables[1]
        copia = None
        fSopa = 0
        fJugables = 0
        for f in nodo.sopa:
            if f is not None:
                fSopa += 1
                f1, f2 = f.get_nums()
                b = [n1 == f1, n1 == f2, n2 == f1, n2 == f2]
                if any(b):
                    fJugables += 1
                    
        if not fJugables == 0:
            prob = self.probabilidad_come(fSopa,fJugables)
        else:
            prob = [0,0]
        for f in nodo.sopa:            
            if f is not None:
                f1, f2 = f.get_nums()
                b = [n1 == f1, n1 == f2, n2 == f1, n2 == f2]
                if any(b):
                    if b[0]:
                        copia = self.copia_nodo(nodo)
                        copia.num_jugables[0] = f2
                        copia.sopa[self.indices_fichas[f1][f2]] = None
                        copia.probabilidad = prob[0]
                        copia.nMano += prob[1]-1
                        lista.append(copia)
                        
                    if b[1] and not b[0]:
                        copia = self.copia_nodo(nodo)
                        copia.num_jugables[0] = f1
                        copia.sopa[self.indices_fichas[f1][f2]] = None
                        copia.probabilidad = prob[0]
                        copia.nMano += prob[1]-1
                        lista.append(copia)

                    if b[2] and not b[0]:
                        copia = self.copia_nodo(nodo)
                        copia.num_jugables[1] = f2
                        copia.sopa[self.indices_fichas[f1][f2]] = None
                        copia.probabilidad = prob[0]
                        copia.nMano += prob[1]-1
                        lista.append(copia)

                    if b[3] and not b[1] and not b[2]:
                        copia = self.copia_nodo(nodo)
                        copia.num_jugables[1] = f1
                        copia.sopa[self.indices_fichas[f1][f2]] = None
                        copia.probabilidad = prob[0]
                        copia.nMano += prob[1]-1
                        lista.append(copia)
                        

    def agrega_sucesor_oponente(self, nodo: Nodo, lista):
        n1,n2 = nodo.num_jugables[0], nodo.num_jugables[1]
        copia = None
        #Suponiendo que el oponente no tuvo que comer para jugar
        fSopa = 0
        fJugables = 0
        #Probabilidad de que el oponente tenga una ficha en particular
        #Igual para todas las fchas jugables
        for f in nodo.sopa:
            if f is not None:
                fSopa += 1
                f1, f2 = f.get_nums()
                b = [n1 == f1, n1 == f2, n2 == f1, n2 == f2]
                if any(b):
                    fJugables += 1
        if not fJugables == 0:
            prob = self.probabilidad_come_oponente(fSopa, fJugables, nodo.mano_oponente)
            #print("p:{} q:{} c:{}".format(prob[0],prob[1],prob[2]))
        else:
            prob = [0,0,0]
        for f in nodo.sopa:
            if f is not None:
                f1, f2 = f.get_nums()
                b = [n1 == f1, n1 == f2, n2 == f1, n2 == f2]
                if any(b):
                    if b[0]:
                        copia = self.copia_nodo(nodo)
                        copia.num_jugables[0] = f2
                        copia.sopa[self.indices_fichas[f1][f2]] = None
                        copia.mano_oponente -= 1 
                        copia.probabilidad = prob[0]
                        lista.append(copia)
                        
                    if b[1] and not b[0]:
                        copia = self.copia_nodo(nodo)
                        copia.num_jugables[0] = f1
                        copia.sopa[self.indices_fichas[f1][f2]] = None
                        copia.mano_oponente -= 1 
                        copia.probabilidad = prob[0]
                        lista.append(copia)

                    if b[2] and not b[0]:
                        copia = self.copia_nodo(nodo)
                        copia.num_jugables[1] = f2
                        copia.sopa[self.indices_fichas[f1][f2]] = None
                        copia.mano_oponente -= 1 
                        copia.probabilidad = prob[0]
                        lista.append(copia)

                    if b[3] and not b[1] and not b[2]:
                        copia = self.copia_nodo(nodo)
                        copia.num_jugables[1] = f1
                        copia.sopa[self.indices_fichas[f1][f2]] = None
                        copia.mano_oponente -= 1 
                        copia.probabilidad = prob[0]
                        lista.append(copia)
                        
        #Suponiendo que tuvo que comer 
        #Se añade el valor esperado de fichas que tendía que comer para que 
        #Obtenga cualquiera de las fichas jugables
        nuevaLista = []
        for n in lista:
            copia = self.copia_nodo(n)
            copia.probabilidad = prob[1]
            copia.mano_oponente += prob[2]
            nuevaLista.append(copia)
        lista.extend(nuevaLista)
            
                        
                        
    #Regresa la lista de estados sucesores porsibles y un valor heurístico del
    #nodo. Se regresa el valor heurístico de los nodos donde algún jugador gana
    #pues se debe checar la condición de victoria para generar sucesores 
    #Si es nodo final, no tiene sentido generar sucesores
    def lista_sucesores(self, nodo, jugador):
        res = list()

        #Si gana TumbaFichas
        if nodo.nMano == 0:
            #valor de la función heurística: 1000
            return res, 1000
        
        #Si gana el oponente
        if nodo.mano_oponente == 0:
            return res, -1000
        
        if jugador:
            for f in nodo.mano:
                self.agrega_sucesor_mano(nodo, f, res)
            if len(res) == 0:
                self.agrega_sucesor_sopa(nodo, res)
        else:
            self.agrega_sucesor_oponente(nodo, res)
        return res, 0
           
    #Llamada sólo en nodos intermedios
    #Para nodos finales, se utiliza el valor retornado por listaSucesores
    #Falta hacer estrategia con los numeros no jugables
    #Falta hacer estrategia con las probabilidades
    #Se podría sumar el valor esperado de fichas comidas
    def funcion_heuristica(self, nodo):
        return 10*(nodo.mano_oponente - nodo.nMano)*nodo.probabilidad
    

    def encuentra_transicion(self, nodoPadre: Nodo, nodoHijo: Nodo):
        p1 = nodoPadre.num_jugables[0]
        h1 = nodoHijo.num_jugables[0]
        dif = nodoPadre.mano.difference(nodoHijo.mano)
        #Si todo va bien, debería entrar aqui siempre
        if len(dif) == 1:
            ficha = dif.pop()
            if (p1 == ficha.num[0] and h1 == ficha.num[1])\
                    or(p1 == ficha.num[1] and h1 == ficha.num[0])\
                    or p1 == -1:
                return ficha, "1"    
            else:
                return ficha, "2"
        print("Error")
        print()
        return None, None
    
    def profundidad(self):
        if self.nodo.num_jugables[0] == -1:
            return 7
        c = 0
        for f in self.nodo.sopa:
            if f is not None:
                c += 1
        print("Profundidad: {}".format(24 - c))
        return 24 - c
    
    def probabilidad_come_oponente(self, fSopa, fJugables, nOponente):
        #Combinaciones de fSopa en nOponente
        lista=[0,0,0]
        if nOponente > fSopa:
            return lista
        p = self.combinaciones[fSopa-1][nOponente-1]/self.combinaciones[fSopa][nOponente]
        lista[0] = p
        #Prob de 
        q = self.combinaciones[fSopa-fJugables][nOponente]/self.combinaciones[fSopa][nOponente]
        lista[1] = q
        s = 0
        p = 1
        for i in range(1,fSopa-nOponente-fJugables+2):
            s += i*p*fJugables/(fSopa-nOponente-i+1)
            p = p*(fSopa-nOponente-fJugables-i+1)/(fSopa-nOponente-i+1)
        lista[2] = math.floor(s)
        return lista
    
    def probabilidad_come(self, fSopa, fJugables):
        #Combinaciones de fSopa en nOponente
        lista=[0,0]
        q = 1/fJugables
        lista[0] = q
        s = 0
        p = 1
        for i in range(1,fSopa-fJugables+2):
            s += i*p*fJugables/(fSopa-i+1)
            p = p*(fSopa-fJugables-i+1)/(fSopa-i+1)
        lista[1] = math.floor(s)
        return lista
        
        
        

#%% Inicia Juego
juego = Domino()
while juego.continua:   
    juego.imprime_todo()
    juego.inicia_turno()
juego.imprime_todo()


