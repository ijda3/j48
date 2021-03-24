from j48.dados import carregaAtributos, carregaData
from j48.arvore import gerarArvore, ExibirArvore


class Main:
    def __init__(self):
        self.classes = []
        self.atributos = {}
        self.numeroAtributos = -1
        self.data = []
        self.arvore = None

    def setAtributos(self, caminho_atributos):
        [classes, atributos] = carregaAtributos(caminho_atributos)

        self.classes = classes
        self.atributos = atributos

    def setData(self, caminho_data):
        self.data = carregaData(caminho_data, self.atributos)

    def gerarArvore(self):
        self.arvore = gerarArvore(self.classes, self.atributos, self.data)

    def exibirArvore(self):
        obj = ExibirArvore(self.arvore)
        obj.exibir()
