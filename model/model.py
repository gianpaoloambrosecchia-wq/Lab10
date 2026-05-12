import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._raggiungibili = []

    def buildGraph(self, anno):
        self._graph.clear()
        nodes = DAO.getAllNodes(anno)
        self._graph.add_nodes_from(nodes)
        for node in nodes:
            self._idMap[node.CCode] = node

        self.add_edges(anno)

    def add_edges(self, anno):
        edges = DAO.getAllEdges(anno, self._idMap)
        for e in edges:
            self._graph.add_edge(e.country1, e.country2)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getNumNodes(self):
        return len(self._graph.nodes)

    # Metodo per avere i vicini di un nodo, restituisce un grafo di vicini
    # che trasformo in lista per averne la lunghezza
    def infoVicini(self, node):
        vicini = list(self._graph.neighbors(node))
        return len(vicini)


    # Metodo di networkX per avere il numero di componenti connesse di un grafo
    def getNumeroComponentiConnesse(self):
        return nx.number_connected_components(self._graph)


    # USA QUESTO METODO PER AVERE LA LISTA DI NODI RAGGIUNGIBILI DA UN NODO SORGENTE!!!!!!!!!!!
    # Questo metodo trova gli archi e poi dagli archi del tree trovo i nodi e gli appendo in una lista
    def getBFSNodesFromEdges(self, codiceStato):
        # nx.bfs_edges ritorna tuple di valori (cioè i nodi) e bisogna passargli il grafo e il nodo sorgente
        nodoSource = self._idMap[codiceStato]
        archi = nx.bfs_edges(self._graph, nodoSource)
        nodiBFS=[]
        # Appendi solo l'arco v perche la u (nodo partenza) lo appendi nell'iterazione precedente
        for u,v in archi:
            nodiBFS.append(v)
        return nodiBFS


    def ricorsione(self, parzialeRagg):

        if len(parzialeRagg) == 0:
            return
        else:
            for n in parzialeRagg:
                self._raggiungibili.append(n)
                self.ricorsione(self._graph.neighbors(n))
                self._raggiungibili.pop()


    def trovaRaggiungibili(self, codiceStato):
        nodoSource = self._idMap[codiceStato]
        parzialeRagg = list(self._graph.neighbors(nodoSource))
        self.ricorsione(parzialeRagg)


