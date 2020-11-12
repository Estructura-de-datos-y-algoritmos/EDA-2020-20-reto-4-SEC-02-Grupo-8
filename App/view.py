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
    print("3- Requerimiento 1")
    print("4- Requerimiento 2")
    print("5- Requerimiento 3")
    print("6- Requerimiento 4")
    print("7- Requerimiento 5")
    print("8- Requerimiento 8")
    print("0- Salir")
    print("*******************************************")



while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
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
        

    elif int(inputs[0]) == 3:
        pass
       
        

    elif int(inputs[0]) == 4:
        pass
        


    elif int(inputs[0]) == 5:
        pass
       

    
    elif int(inputs[0]) == 6:
        pass
        

    
    elif int(inputs[0]) == 7:
        pass
       

    else:
        sys.exit(0)
sys.exit(0)


"""
Menu principal
"""