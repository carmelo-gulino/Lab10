import copy

import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        self.countries_list = DAO.get_all_countries()  #lista di nazioni
        self.countries_map = {}
        for country in self.countries_list:
            self.countries_map[country.CCode] = country  #mappa di nazioni
        self.countries_graph = nx.Graph()   #creo il grafo vuoto

    def build_graph(self, year):
        """
        Costruisce il grafo facendo una query sui confini: se il confine è di terra aggiunge l'arco
        """
        self.countries_graph.clear()
        for contiguity in DAO.get_contiguities(year):   #guardo tutti i confini ricevuti
            s1 = self.countries_map[contiguity.state1no]    #estraggo le nazioni
            s2 = self.countries_map[contiguity.state2no]
            self.countries_graph.add_node(s1)   #aggiungo i nodi al grafo
            self.countries_graph.add_node(s2)
            if contiguity.conttype == 1:
                self.countries_graph.add_edge(s1, s2)   #aggiungo l'arco tra i due nodi (oggetto Contiguity)

    def get_nodes_DFS(self, source):
        """
        Nodi raggiungibili tramite DFS
        """
        edges = nx.dfs_edges(self.countries_graph, source)
        raggiungibili = []
        for u, v in edges:
            raggiungibili.append(v)
        return raggiungibili

    def get_nodes_BFS(self, source):
        """
        Nodi raggiungibili tramite BFS
        """
        edges = nx.bfs_edges(self.countries_graph, source)
        raggiungibili = []
        for u, v in edges:
            raggiungibili.append(v)
        return raggiungibili

    def get_nodes_ricorsione(self, parziale, esplorabili, source, nodo):
        """
        Nodi raggiungibili tramite algoritmo ricorsivo
        :param parziale: insieme di nodi
        :param esplorabili: lista di tutti i vicini del nodo di partenza
        :param source: nodo sorgente
        :param nodo: nodo di partenza di ogni ricorsione
        """
        result = None
        # CASO BANALE
        if len(esplorabili) == 0:  #se ho esplorato tutti i vicini della sorgente, ho finito
            result = copy.deepcopy(parziale)
            return result
        # CASO RICORSIVO
        else:
            for vicino in self.countries_graph[nodo]:   #guardo i vicini del ndo
                if nodo == source:
                    esplorabili.remove(vicino)  #se sto esplorando la sorgente, rimuovo dagli esplorabili il nodo
                parziale.add(vicino)
                self.get_nodes_ricorsione(parziale, esplorabili, source, vicino)
            parziale.pop()
