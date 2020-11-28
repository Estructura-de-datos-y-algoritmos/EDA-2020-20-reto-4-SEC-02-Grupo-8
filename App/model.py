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
import config
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import bfs
from DISClib.ADT import map as m
from DISClib.ADT import stack
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.DataStructures import mapentry as me
from DISClib.Utils import error as error
from math import sin, cos, sqrt, atan2, radians
import gpxpy.geo
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

def newAnalyzer():

    analyzer = {'graph': None}
                #'edad': None}

    analyzer["graph"] = gr.newGraph(datastructure='ADJ_LIST',
                                    directed=True,
                                    size=1000,
                                    comparefunction=compareStations)
    analyzer['ruta'] = m.newMap(1000, 
                                maptype='PROBING', 
                                loadfactor=0.5,
                                comparefunction= compareStations)

    analyzer['edad'] = m.newMap(15, 
                                maptype='PROBING', 
                                loadfactor=0.5,
                                comparefunction= compareAge)
    analyzer["coor_start"] = m.newMap(700, 
                                maptype='PROBING', 
                                loadfactor=0.5,
                                comparefunction= compareCoordinates)
    analyzer["coor_end"] = m.newMap(700, 
                                maptype='PROBING', 
                                loadfactor=0.5,
                                comparefunction= compareCoordinates)

    return analyzer


# Funciones para agregar informacion al grafo

# ==============================
# Funciones de consulta
# ==============================

def addRuta(analyzer, trip):
    origen = trip["start station id"]
    destino = trip["end station id"]
    key = origen+"-"+destino
    llave = m.get(analyzer["ruta"], key)
    if llave is None:
        valor = {}
        valor["lstDuracion"] = lt.newList('SINGLE_LINKED', compareLista)
        m.put(analyzer["ruta"], key, valor)
    else:
        valor = me.getValue(llave)
    lt.addLast(valor["lstDuracion"], trip["tripduration"])

    return analyzer


def addnewTrip(analyzer):
    llave = m.keySet(analyzer["ruta"])
    itera = it.newIterator(llave)
    while it.hasNext(itera):
        recorrido = 0
        duracion = 0
        ruta = it.next(itera)
        llv = m.get(analyzer["ruta"], ruta)
        valor = me.getValue(llv)
        itera2 = it.newIterator(valor["lstDuracion"])
        while it.hasNext(itera2):
            rec = int(it.next(itera2))
            recorrido += rec
        duracion = recorrido/lt.size(valor["lstDuracion"])
        ruta = ruta.split("-")
        origen = ruta[0]
        destino = ruta[1]
        addStation(analyzer, origen)
        addStation(analyzer, destino)
        addConnection(analyzer, origen, destino, duracion)
        


'''
def addTrip(analyzer, trip):
    
    origen = trip["start station id"]
    destino = trip["end station id"]
    duracion = int(trip["tripduration"])
    addStation(analyzer, origen)
    addStation(analyzer, destino)
    addConnection(analyzer, origen, destino, duracion)
'''

def addStation(analyzer, id):

    if not gr.containsVertex(analyzer["graph"], id):
        gr.insertVertex(analyzer["graph"], id)
    return analyzer


def addConnection(analyzer, origen, destino, duracion):

    arco = gr.getEdge(analyzer["graph"], origen, destino)
    if arco is None:
        gr.addEdge(analyzer["graph"], origen, destino, duracion)
        return analyzer

def addAge(analyzer, trip):

    llave = aproximaredad(analyzer, trip)
    entra = m.get(analyzer["edad"], llave)

    if entra is None:
        valor = NewEntry(trip)
        m.put(analyzer["edad"], llave, valor)
    else:
        valor = me.getValue(entra)
        actualizar(valor["e_salida"], trip["start station id"])
        actualizar(valor["e_llegada"], trip["end station id"])
    
    return analyzer

def actualizar(map, llave):
    entry = m.get(map, llave)
    if entry is None:
        m.put(map, llave, 1)
    else:
        valor = me.getValue(entry)
        valor += 1
        me.setValue(entry, valor)
    return map



def addCoordinate(analyzer, trip):
    
    esta = m.get(analyzer["coor_start"], trip["start station id"])
    if esta is None:
        dicci = {}
        dicci["latitud"] = trip["start station latitude"]
        dicci["longitud"] = trip["start station longitude"]
        m.put(analyzer["coor_start"], trip["start station id"], dicci)
    entra = m.get(analyzer["coor_end"], trip["end station id"])
    if entra is None:
        diccit = {}
        diccit["latitud"] = trip["end station latitude"]
        diccit["longitud"] = trip["end station longitude"]
        m.put(analyzer["coor_end"], trip["end station id"], diccit)
    
    return analyzer


def aproximaredad(analyzer, trip):
    año = trip["birth year"]
    edad = 2020 - int(año)
    if edad <= 10:
        llave = 1
        return llave
    elif edad <= 20 and edad > 10:
        llave = 2
        return llave
    elif edad <= 30 and edad > 20:
        llave = 3
        return llave
    elif edad <= 40 and edad > 30:
        llave = 4
        return llave
    elif edad <= 50 and edad > 40:
        llave = 5
        return llave
    elif edad <= 60 and edad > 50:
        llave = 6
        return llave
    else:
        llave = 7
        return llave

def aproximarEdad(analyzer, edad):
    try:
        edad = int(edad)
        if edad <= 10:
            llave = 1
            return llave
        elif edad <= 20 and edad > 10:
            llave = 2
            return llave
        elif edad <= 30 and edad > 20:
            llave = 3
            return llave
        elif edad <= 40 and edad > 30:
            llave = 4
            return llave
        elif edad <= 50 and edad > 40:
            llave = 5
            return llave
        elif edad <= 60 and edad > 50:
            llave = 6
            return llave
        else:
            llave = 7
            return llave
    except:
        print("No hay registros")

def NewEntry(trip):
    
    entry = {'e_salida': None}
            #'e_llegada': None}

    entry['e_salida'] = m.newMap(30, 
                                    maptype='PROBING', 
                                    loadfactor=0.5,
                                    comparefunction= compareStations)
    entry['e_llegada'] = m.newMap(30, 
                                    maptype='PROBING', 
                                    loadfactor=0.5,
                                    comparefunction= compareStations)

    return entry

def inician(analyzer, edad):                              

    llave = aproximarEdad(analyzer, edad)
    tabla = m.get(analyzer["edad"], llave)
    if tabla is not None:
        map_salida = me.getValue(tabla)["e_salida"]
        map_llegada = me.getValue(tabla)["e_llegada"]
        max_salida = maximo(map_salida)
        max_llegada = maximo(map_llegada)
        paths = rutaTuristica(analyzer, max_salida)
        distancia_e(paths, max_llegada)
    
    return (max_salida, max_llegada)


def maximo(map):
    llave = m.keySet(map)
    itera = it.newIterator(llave)
    mayor = 0
    while it.hasNext(itera):
        ll = it.next(itera)
        entry = m.get(map, ll)
        valor = me.getValue(entry)
        if valor > mayor:
            mayor = valor
            estacion = ll
    return estacion



def rutaCircular(analyzer, tiempo, station):

    nodos = dfs.DepthFirstSearch(analyzer["graph"], station)
    estacionesdestino = m.keySet(nodos['visited'])
    itera = it.newIterator(estacionesdestino)
    lst_rutas ={}
    while it.hasNext(itera):
        conta_tiempo1 =0
        Key_stacion = it.next(itera)
        key1=""
        ruta_ok = False
        vallor =""

        valor = m.get(nodos['visited'],Key_stacion)['value']['edgeTo']
        if valor is not None:
            key_ini = valor
            while True:
                valor_arco = gr.getEdge(analyzer["graph"],key_ini,Key_stacion)['weight']
                conta_tiempo1=conta_tiempo1+ valor_arco   + 1200

                if conta_tiempo1 > tiempo:
                    ruta_ok = False
                    break

                if key_ini ==  station:
                    ruta_ok = True
                    key1 = key1 + "*" + key_ini + "-" + Key_stacion
                    vallor = vallor + key1 + "-Valor Arco " + str(valor_arco) + " valor conta_tiempo1 " + str(conta_tiempo1) +"\n"
                    break   

                key1 = key1 + "*"+ key_ini + "-" + Key_stacion 
                Key_stacion = key_ini
                key_ini  = m.get(nodos['visited'],Key_stacion)['value']['edgeTo']
            
            if ruta_ok:
                print("Ruta  Ok...", key1)
                print("vallor... ", vallor)
                key_ruta = key1.split("*")
                key_2 =""
                for k in reversed(key_ruta):
                    if k != "":
                        if len(key_2)== 0: #prmera vez que entra 
                            key_2 = k
                        else:
                            key_2 = key_2 + "-"+ k 
                
                print("Ruta ordenada ",key_2)
                ultima = key_2.split("-")
                print("ultima", ultima, "longi ", len(ultima))
                ultima_ruta = ultima[len(ultima)-1]
                print("ultima ruta ", ultima_ruta)
                ultimo_valor = gr.getEdge(analyzer["graph"],ultima_ruta,station)

                if (ultimo_valor is not None):
                    conta_tiempo1 = conta_tiempo1 +  ultimo_valor['weight']
                                    
                    if (conta_tiempo1 <= tiempo):
                        key_2 = key_2 + "-" + station
                        lst_rutas[key_2] = conta_tiempo1 
    print("Rutas seleccionadas  ",lst_rutas)
    return lst_rutas

def estacionCritica(analyzer):
    
    recorre = dfs.DepthFirstSearch(analyzer["graph"], '72')
    valor = m.valueSet(recorre["visited"])
    itera = it.newIterator(valor)
    first = 0
    second = 0
    third  = 0
    while it.hasNext(itera):
        dicci = it.next(itera)
        edge = dicci["edgeTo"]
        if edge is not None:
            llegan = gr.indegree(analyzer["graph"], edge)
            if llegan > first and llegan > second and llegan > third:
                first = llegan
                vertice = edge
            if llegan < first and llegan > second and llegan > third:
                second = llegan
                vertice2 = edge
            if llegan < first and llegan < second and llegan > third:
                third = llegan
                vertice3 = edge


    return first, second, vertice, vertice2, third, vertice3


def estacionCriticaSalida(analyzer):

    recorre = dfs.DepthFirstSearch(analyzer["graph"], '72')
    valor = m.valueSet(recorre["visited"])
    itera = it.newIterator(valor)
    primero = 0
    segundo = 0
    tercero  = 0
    while it.hasNext(itera):
        dicci = it.next(itera)
        edge = dicci["edgeTo"]
        if edge is not None:
            llegan = gr.outdegree(analyzer["graph"], edge)
            if llegan > primero and llegan > segundo and llegan > tercero:
                primero= llegan
                verti = edge
            if llegan < primero and llegan > segundo and llegan > tercero:
                segundo = llegan
                verti2 = edge
            if llegan < primero and llegan < segundo and llegan > tercero:
                tercero = llegan
                verti3 = edge
    return primero, segundo, tercero, verti, verti2, verti3


def estacionCriticaSinuso(analyzer):
    recorre = dfs.DepthFirstSearch(analyzer["graph"], '72')
    valor = m.valueSet(recorre["visited"])
    itera = it.newIterator(valor)
    fi = 1000
    se = 1000
    th  = 1000
    while it.hasNext(itera):
        dicci = it.next(itera)
        edge = dicci["edgeTo"]
        if edge is not None:
            llegan = gr.indegree(analyzer["graph"], edge)
            salen = gr.outdegree(analyzer["graph"], edge)
            total = llegan + salen
            if total < fi and total < se and total < th:
                fi = total
                v = edge
            if total > fi and total < se and total < th:
                se = total
                v2 = edge
            if total > fi and total > se and total < th:
                th = total
                v3 = edge
    return fi, se, th, v, v2, v3


def coordenadas(analyzer, first_la, first_lo, last_la, last_lo):

    map = analyzer["coor_start"]
    firstStation = estacion_cercana(map, first_la, first_lo)

    map = analyzer["coor_end"]
    lastStation = estacion_cercana(map, last_la, last_lo)

    paths = rutaTuristica(analyzer, firstStation)
    distancia_e(paths, lastStation)

    return (firstStation, lastStation)



def estacion_cercana(map, lat, lon):
    
    estacion = ""
    dista = 1000
    lista_k = m.keySet(map)
    itera = it.newIterator(lista_k)
    while it.hasNext(itera):
        id = it.next(itera)
        dicci = m.get(map, id)
        valor = me.getValue(dicci)
        latitud = float(valor["latitud"])
        longitud = float(valor["longitud"])
        ubicacion = (lat, lon)
        origen = (latitud, longitud)
        distance = distancia(origen, ubicacion)
        if distance < dista:
            dista = distance
            estacion = id
    return estacion



def distancia(origen, ubicacion):
    lat1, lon1 = origen
    latitud, longitud = ubicacion
    R = 6371
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))

    latitud = radians(float(latitud))
    longitud = radians(float(longitud))

    dlon = longitud - lon1 
    dlat = latitud - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(latitud) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance


def rutaTuristica(analyzer, id):
    paths = djk.Dijkstra(analyzer["graph"], id)
    return paths

def distancia_e(paths, estacion_llegada):
    keys = m.keySet(paths["visited"])
    itera = it.newIterator(keys)
    while it.hasNext(itera):
        duracion = 0
        ruta_turistica = ""
        estacion = it.next(itera)
        if estacion == estacion_llegada:
            minpath = djk.pathTo(paths, estacion_llegada)
            if minpath is not None:
                while(not stack.isEmpty(minpath)):
                    stop = stack.pop(minpath)
                    duracion += stop["weight"]
                    ruta_turistica += stop["vertexA"] +"-"+ stop["vertexB"]+"\n"
                print("\nDuracion en minutos: ", int(duracion/60))
                print("Camino más corto entre estaciones: ", ruta_turistica)

                    

def rutasTuristicas(paths, tiempo):
    keys = m.keySet(paths["visited"])
    itera = it.newIterator(keys)
    while it.hasNext(itera):
        duracion = 0
        ruta_turistica = ""
        estacion = it.next(itera)
        minpath = djk.pathTo(paths, estacion)
        if minpath is not None:
            while(not stack.isEmpty(minpath)):
                stop = stack.pop(minpath)
                duracion += stop["weight"]
                ruta_turistica += stop["vertexA"] +"-"+ stop["vertexB"]+"\n"
            if duracion <= tiempo:
                print("Duracion en minutos: ", int(duracion/60))
                print("Estaciones para usar: ", ruta_turistica)



# ==============================
# Funciones Helper
# ==============================

    
def totalConnections(analyzer):

    return gr.numEdges(analyzer['graph'])


def totalStops(analyzer):

    return gr.numVertices(analyzer['graph'])

def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju 
    """
    sc= scc.KosarajuSCC(analyzer['graph'])
    return scc.connectedComponents(sc)


def rutascirculares(analyzer, id):

    pass

# ==============================
# Funciones de Comparacion
# ==============================


def compareStations(id1, id2):
    
    id2 = id2['key']
    if (id1 == id2):
        return 0
    elif (id1 > id2):
        return 1
    else:
        return -1

def compareAge(edad1, edad2):
    
    edad2 = edad2['key']
    if  edad1 == edad2:
        return 0
    elif edad1 > edad2:
        return 1
    else:
        return -1

def compareCoordinates(coor1, coor2):
    
    coor2 = coor2["key"]
    if coor1 == coor2:
        return 0
    elif coor1 > coor2:
        return 1
    else:
        return -1



def compareLista(lista1, lista2):
    pass