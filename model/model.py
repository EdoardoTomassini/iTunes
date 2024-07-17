import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}


    def buildGraph(self, durata):
        # QUANDO PER AGGIUNGERE NODI HO BISGONO DI INFO INSERITE
        # DALL'UTENTE COME DURATA IN QUESTO CASO
        # --------> AGGIUNGO I NODI IN BUILDGRAPH() NON IN INIT
        self._grafo.clear()
        self._grafo.add_nodes_from(DAO.getAlbums(durata))

        albums = list(self._grafo.nodes)
        for a in albums:
            self._idMap[a.AlbumId] = a

        myedges = DAO.getConnessioni(self._idMap)
        self._grafo.add_edges_from(myedges)

    def getConnessaDetails(self, v0):
        # mi rstituisce la componente connessa che contiene v0
        # e restituisce un set
        conn = nx.node_connected_component(self._grafo, v0)
        durataTot = 0
        for album in conn:
            durataTot += album.totD

        return len(conn), durataTot


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getAlbums(self):
        # FAI ATTENZIONE A FARE UN PARSE LIST PER I NODI
        return list(self._grafo.nodes)