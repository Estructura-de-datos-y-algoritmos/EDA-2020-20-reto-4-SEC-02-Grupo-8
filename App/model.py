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
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.DataStructures import mapentry as me
from DISClib.Utils import error as error
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
    analyzer['edad'] = m.newMap(1000, 
                                maptype='PROBING', 
                                loadfactor=0.5,
                                comparefunction= compareAge)

    return analyzer


# Funciones para agregar informacion al grafo

# ==============================
# Funciones de consulta
# ==============================

def addTrip(analyzer, trip):
    
    origen = trip["start station id"]
    destino = trip["end station id"]
    duracion = int(trip["tripduration"])
    addStation(analyzer, origen)
    addStation(analyzer, destino)
    addConnection(analyzer, origen, destino, duracion)


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
    valor = NewEntry(trip)

    if entra is None:
        
        dicci = {}
        dicci["num"] = 1
        entrada = m.put(valor["e_salida"],trip["start station id"], dicci)
        #llegada = m.put(valor["e_llegada"], trip["end station id"], dicci)
        m.put(analyzer["edad"], llave, entrada)
    else:
        esta = m.get(valor["e_salida"], trip["start station id"])
        if esta is None:
            dicci = {}
            dicci["num"] = 1            
            entrada = m.put(valor["e_salida"],trip["start station id"], dicci)
        else:
            #dicci["num"] += 1
            l = m.get(valor["e_salida"], trip["start station id"])
            v = me.getValue(l)
            v["num"] += 1
        #estaa = m.get(valor["e_llegada"], trip["end station id"])
    
    return dicci


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

def NewEntry(trip):
    
    entry = {'e_salida': None}
            #'e_llegada': None}

    entry['e_salida'] = m.newMap(30, 
                                    maptype='PROBING', 
                                    loadfactor=0.5,
                                    comparefunction= compareStations)
    #entry['e_llegada'] = m.newMap(30, 
     #                               maptype='PROBING', 
      #                              loadfactor=0.5,
       #                             comparefunction= compareStations)

    #m.put(entry["e_salida"], trip[""])
    return entry

def inician(analyzer, edad):

    llave = aproximarEdad(analyzer, edad)
    llv = m.get(analyzer["edad"], llave)
    tabla = me.getValue(llv)
    print(tabla)
    '''
    ids = m.keySet(tabla)
    itera = it.newIterator(ids)
    maxi = 0 

    while it.hasNext(itera):
        id = it.next(itera)
        ll = m.get(tabla, id)
        conteo = me.getValue(ll)
        for k in conteo:
            if conteo[k] > maxi:
                maxi = conteo[k]
                llave = id
    return maxi, llave
    '''
        

def rutaCircular(analyzer, time, identificador):

    kosaju = scc.KosarajuSCC(analyzer["graph"])
    conteo = scc.sccCount(analyzer["graph"], kosaju, identificador)

    return kosaju, conteo

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


def coordenadas(analyzer, first_ll, last_ll):

    pass

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
    
    #print("Compara ids-stop ", id1)
    #print("Compara ids keyvaluestop  ", id2)
    id2 = id2['key']
    if (id1 == id2):
        return 0
    elif (id1 > id2):
        return 1
    else:
        return -1

def compareAge(edad1, edad2):
    
    #print("EDAD1 ------------", edad1)
    #print("EDAD2 ++++++++++", edad2)
    edad2 = edad2['key']
    if  edad1 == edad2:
        return 0
    elif edad1 > edad2:
        return 1
    else:
        return -1
        