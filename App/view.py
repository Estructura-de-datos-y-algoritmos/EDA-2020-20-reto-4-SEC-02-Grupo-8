"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
from time import process_time
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

tripFile = '201801-1-citibike-tripdata.csv'
#initialStation = None
#recursionLimit = 20000


# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de Citibike")
    print("3- Requerimiento 2")
    print("4- Requerimiento 3")
    print("5- Requerimiento 4")
    print("6- Requerimiento 5")
    print("7- Requerimiento 6")
    print("0- Salir")
    print("*******************************************")



while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando rutas ....")
        t1 = process_time()
        controller.loadFile(cont)
        arcos = controller.totalConnections(cont)
        vertices = controller.totalStops(cont)
        conectado = controller.connectedComponents(cont)
        print('Numero de arcos: ' + str(arcos))
        print('Numero de vertices: ' + str(vertices)) 
        print('El número de componentes fuertemente conectados es: ' + str(conectado))
        t2 = process_time()
        t = t2-t1
        print("Tiempo requerido: ", t)
        

    elif int(inputs[0]) == 3:                                                      #FALTA
        print("Ruta turistica circular...\n")
        time = int(input("Digite cuanto tiempo tiene disponible en minutos: "))
        time *= 60
        identificador = input("Diga el identificador de la estacion de inicio: ")
        controller.rutaCircular(cont, time, identificador)       
        

    elif int(inputs[0]) == 4:
        print("Estaciones Criticas...\n")
        first, second, vertice, vertice2, third, vertice3 = controller.estacionCritica(cont)
        print("TOP 3 ESTACIONES A LAS QUE LLEGAN MÁS BICICLETAS\n")
        print("Primero ", vertice, "con", first, "\nSegundo ", vertice2, "con", second, "\nTercero ", vertice3, "con", third) 
        primero, segundo, tercero, verti, verti2, verti3 = controller.estacionCriticaSalida(cont) 
        print("\nTOP 3 ESTACIONES A LAS QUE SALEN MÁS BICICLETAS\n")
        print("Primero ", verti, "con", primero, "\nSegundo ", verti2, "con", segundo, "\nTercero ", verti3, "con", tercero)
        fi, se, th, v, v2, v3 = controller.estacionCriticaSinuso(cont)
        print("\nTOP 3 ESTACIONES QUE MENOS USO TIENEN\n")
        print("Primero ", v, "con", fi, "\nSegundo ", v2, "con", se, "\nTercero ", v3, "con", th)


    elif int(inputs[0]) == 5:
        print("Ruta turistica...\n")
        id = input("diga el id de la estación inicial: ")
        tiempo = int(input("Diga cuanto tiempo tiene en minutos: "))
        tiempo = tiempo*60
        paths = controller.rutaTuristica(cont, id)
        controller.rutasTuristicas(paths, tiempo)
       

    
    elif int(inputs[0]) == 6:
        print("Recomendador de rutas...\n")
        edad = input("Digite su edad en años: \n")
        max_salida, max_llegada = controller.inician(cont, edad)
        print("La estación de la cual más se inician viajes es: ", max_salida, "\n")
        print("La estacion de la cual llegan mas viajes es: ", max_llegada)
        

    
    elif int(inputs[0]) == 7:
        print("Ruta de interes turistico...\n")                            #40.766272, -73.993442
        print("COORDENADAS\n")                                             #40.685531, -73.956102
        first_la = input("Digite su latitud: ")                            #40.766352, -73.801875 (QUEENS)    40.678405, -73.992076 (BROOKLYN)
        first_lo = input("Digite su longitud: ")                           #40.76727216,-73.99392888    40.71473993, -74.00910627
        last_la = input("Digite la latitud de su destino: ")
        last_lo = input("Digite la longitud de su destino: ")
        firstStation, lastStation = controller.coordenadas(cont, first_la, first_lo, last_la, last_lo)
        print("La estación más cercana a su ubicación es : ", firstStation, "\nLa más cercana a su destino es: ", lastStation)


    else:
        sys.exit(0)
sys.exit(0)


"""
Menu principal
"""