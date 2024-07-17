import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceAlbum = None

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()
        durata = self._view._txtInDurata.value
        if durata == "":
            self._view._txt_result.controls.append(
                ft.Text("Inserire un valoree di durata"))
            self._view.update_page()
            return

        try:
            durataInt = int(durata)
        except ValueError:
            self._view._txt_result.controls.append(
                ft.Text("Inserire un valore intero di durata"))
            self._view.update_page()
            return

        self._model.buildGraph(durataInt)
        nN, nE = self._model.getGraphDetails()
        self._view._txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato"))
        self._view._txt_result.controls.append(
            ft.Text(f"Num nodi = {nN}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Num archi = {nE}"))

        self.fillDDAlbum()

        self._view.update_page()

    def fillDDAlbum(self):
        albums = self._model.getAlbums()
        albums.sort(key = lambda x: x.Title)
        for a in albums:
            self._view._ddAlbum.options.append(
                ft.dropdown.Option(data=a,
                                   on_click=self.getSelectedAlbum,
                                   text=a.Title
                                   ))

    def getSelectedAlbum(self, e):
        album = e.control.data
        if album is None:
            self._view._txt_result.controls.append(ft.Text("Non è stato selezionato nessun album"))
            self._view.update_page()
        else:
            self._choiceAlbum = album
        print(album)

    def handleAnalisiComp(self, e):
        album = self._choiceAlbum
        if album is None:
            self._view._txt_result.controls.append(ft.Text("Non è stato album"))
            self._view.update_page()
            return
        numAlb, durataTot = self._model.getConnessaDetails(album)
        self._view._txt_result.controls.append(
            ft.Text(f"La componente connessa di {album} "
                    f"ha dimensione {numAlb} e durata totale {durataTot}"))
        self._view.update_page()

    def handleGetSetAlbum(self, e):
        pass