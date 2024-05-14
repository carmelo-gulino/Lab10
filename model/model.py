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

