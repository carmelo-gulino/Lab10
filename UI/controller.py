import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCalcola(self, e):
        if self._view._txtAnno.value is not None:
            try:
                anno = int(self._view._txtAnno.value)
                if anno > 2016 or anno < 1816:
                    self._view.create_alert("Inserire un numero tra 1816 e 2016!")
                else:
                    self._model.build_graph(anno)
                    self.print_graph()
                    self.fill_ddStato(self._model.countries_graph.nodes())
            except ValueError:
                self._view.create_alert("Inserire un numero!")
        else:
            self._view.create_alert("Inserire un anno!")

    def print_graph(self):
        """
        Stampa il grafo creato e le relative informazioni
        """
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo creato correttamente."))
        self._view._txt_result.controls.append(ft.Text(self._model.countries_graph))
        self._view._txt_result.controls.append(ft.Text(
            f"Il grafo ha {nx.number_connected_components(self._model.countries_graph)} componenti connesse."))
        for node, degree in self._model.countries_graph.degree: #tupla nodo - grado
            self._view._txt_result.controls.append(ft.Text(f"{node} -- {degree} vicini."))
        self._view.update_page()

    def fill_ddStato(self, countries):
        """
        Riempie il dropdown ogni volta che viene creato un nuovo grafo
        """
        self._view._ddStato.options.clear()
        if self._view._btnRaggiungibili.disabled:
            self._view._btnRaggiungibili.disabled = False
        for country in countries:
            self._view._ddStato.options.append(ft.dropdown.Option(key=country.CCode,
                                                                  text=country.StateNme,
                                                                  data=country,
                                                                  on_click=self.read_country))
        self._view.update_page()

    def read_country(self, e):
        """
        Estrae l'oggetto Country dopo averlo selezionato dal menu dropdown
        """
        self._view._ddStato.data = e.control.data

    def handleRaggiungibiliDFS(self, e):
        source = self._view._ddStato.data
        raggiungibili = self._model.get_nodes_DFS(source)
        self.print_raggiungibili(source, raggiungibili, "DFS")

    def handleRaggiungibiliBFS(self, e):
        source = self._view._ddStato.data
        raggiungibili = self._model.get_nodes_BFS(source)
        self.print_raggiungibili(source, raggiungibili, "BFS")

    def handleRaggiungibiliRicorsione(self, e):
        source = self._view._ddStato.data
        esplorabili = set([vicino for vicino in self._model.countries_graph[source]])
        raggiungibili = self._model.get_nodes_ricorsione(set(), esplorabili, source, source)
        self.print_raggiungibili(source, raggiungibili, "ricorsivo")

    def print_raggiungibili(self, source, raggiungibili, metodo):
        """
        Stampa l'elenco di nodi raggiungibili
        """
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"I nodi raggiungibili da {source} con metodo {metodo} sono:"))
        for country in raggiungibili:
            self._view._txt_result.controls.append(ft.Text(country))
        self._view.update_page()


