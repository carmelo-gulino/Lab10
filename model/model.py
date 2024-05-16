import copy

import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        self.countries_list = DAO.get_all_countries()  #lista di nazioni
        self.raggiungibili = set()  #insieme di nodi raggiungibili
        self.countries_map = {}
        for country in self.countries_list:
            self.countries_map[country.CCode] = country  #mappa di nazioni
        self.countries_graph = nx.Graph()  #creo il grafo vuoto

    def build_graph(self, year):
        """
        Costruisce il grafo facendo una query sui confini: se il confine è di terra aggiunge l'arco
        """
        self.countries_graph.clear()
        for contiguity in DAO.get_contiguities(year):  #guardo tutti i confini ricevuti
            s1 = self.countries_map[contiguity.state1no]  #estraggo le nazioni
            s2 = self.countries_map[contiguity.state2no]
            self.countries_graph.add_node(s1)  #aggiungo i nodi al grafo
            self.countries_graph.add_node(s2)
            if contiguity.conttype == 1:
                self.countries_graph.add_edge(s1, s2)  #aggiungo l'arco tra i due nodi (oggetto Contiguity)

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

    def get_nodes_ricorsione(self, nodo, prec):
        self.raggiungibili = set()
        self.ricorsione(nodo, prec)
        print(self.raggiungibili)

    def ricorsione(self, nodo, prec):
        """
        Nodi raggiungibili tramite algoritmo ricorsivo
        :param prec: nodo precedente, inizialmente settato a None
        :param nodo: nodo di partenza di ogni ricorsione
        """
        if len(self.countries_graph[nodo]) == 1 and prec in self.countries_graph[nodo]:
            return  #se ho un solo vicino e quel vicino è il precedente, ho finito
        else:
            for vicino in self.countries_graph[nodo]:
                if vicino not in self.raggiungibili:  #solo se non ho ancora considerato quello Stato
                    self.raggiungibili.add(vicino)  #aggiungo il vicino alla lista
                    prec = nodo  #il precedente è il nodo che ho appena visitato
                    self.ricorsione(vicino, prec)

    def get_nodes_iterativo(self, source):
        """
        Trova i nodi raggiungibili con un algoritmo iterativo
        :param source: nodo di partenza
        """
        visitati = set()    #set per non avere duplicati
        da_visitare = [source]
        while len(da_visitare) > 0:
            for nodo in da_visitare:
                for vicino in self.countries_graph[nodo]:
                    if vicino not in visitati:
                        da_visitare.append(vicino)
                visitati.add(nodo)
                da_visitare.remove(nodo)
        return visitati
