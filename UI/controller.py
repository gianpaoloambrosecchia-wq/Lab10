import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCalcola(self, e):
        anno = self._view._txtAnno.value
        if anno=="":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Attenzione inserire un valore di anno", color="red")
            )
            self._view.update_page()
            return
        try:
            annoInt = int(anno)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Attenzione inserire un valore numerico nel campo anno", color="red")
            )
            self._view.update_page()
            return

        if annoInt < 1816 or annoInt > 2016:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Attenzione inserisci un anno compreso tra 1816 e 2016", color="red")
            )
            self._view.update_page()
            return

        self._model.buildGraph(annoInt)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text("Grafo creato correttamente", color="green")
        )

        for n in self._model._graph.nodes:
            self._view._ddStati.options.append(
                ft.dropdown.Option(
                    key=n.CCode,
                    text=n.StateNme
                )
            )

        self._view._txt_result.controls.append(
            ft.Text(f"Il grafo ha {self._model.getNumeroComponentiConnesse()} vicini")
        )

        for n in self._model._graph.nodes:
            numVicini = self._model.infoVicini(n)
            self._view._txt_result.controls.append(
                ft.Text(f"{n} -- {numVicini} vicini")
            )
        self._view.update_page()


    def handleRaggiungibili(self, e):
        codiceStato = self._view._ddStati.value
        if codiceStato=="":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Seleziona uno stato", color="red")
            )
            self._view.update_page()
            return

        nodiRaggiungibili = self._model.getBFSNodesFromEdges(int(codiceStato))
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Lo Stato selezionato può raggiungere {len(nodiRaggiungibili)} Nazioni")
        )
        for n in nodiRaggiungibili:
            self._view._txt_result.controls.append(
                ft.Text(f"{n}")
            )
        self._view.update_page()













