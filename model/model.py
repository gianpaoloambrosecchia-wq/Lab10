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
    # Questo metodo trova gli archi e poi dagli archi del tree trovo i nodi e gli appendo in una lista.
    def getBFSNodesFromEdges(self, codiceStato):

        #METODO PIU SEMPLICE
        # Crea l'albero BFS a partire dal nodo sorgente
        #albero_bfs = nx.bfs_tree(self._graph, nodoSource)

        # Restituisce i nodi dell'albero convertiti in lista (nodoSource incluso)
        #return list(albero_bfs.nodes)


        #OPPURE ALTRO METODO SEMPLICE (USANDO LA COMPONENTE CONNESSA)
        # Tutti i nodi raggiungibili da 'start' (grafo non orientato)
        #raggiungibili = nx.node_connected_component(self._graph, nodoSource)

        # Grafo orientato — solo seguendo gli archi in avanti
        #raggiungibili = nx.descendants(self._graph, nodoSource)
        #raggiungibili.add(nodoSource)  # descendants non include il nodo stesso
        #return list(raggiungibili)


        nodoSource = self._idMap[codiceStato]
        # nx.bfs_edges ritorna tuple di valori (cioè i nodi) e bisogna passargli il grafo e il nodo sorgente
        archi = nx.bfs_edges(self._graph, nodoSource)
        nodiBFS=[]
        # Appendi solo l'arco v perche la u (nodo partenza) lo appendi nell'iterazione precedente
        for u,v in archi:
            nodiBFS.append(v)
        return nodiBFS


    def ricorsione(self, nodo):
        self._raggiungibili.append(nodo)

        for vicino in self._graph.neighbors(nodo):
            if vicino not in self._raggiungibili:  # evita i cicli
                self.ricorsione(vicino)


    def trovaRaggiungibili(self, codiceStato):
        self._raggiungibili = []
        nodoSource = self._idMap[codiceStato]
        self.ricorsione(nodoSource)



