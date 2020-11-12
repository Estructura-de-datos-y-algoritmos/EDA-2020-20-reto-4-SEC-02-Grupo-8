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
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
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

    analyzer = {'graph': None
                    }

    analyzer["graph"] = gr.newGraph(datastructure='ADJ_LIST',
                                    directed=True,
                                    size=1000,
                                    comparefunction=compareStations)

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


# ==============================
# Funciones Helper
# ==============================

    


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