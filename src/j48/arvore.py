from math import log


def gerarArvore(classes, atributos, data):
    arvore = Arvore(classes, atributos, data)
    arvore.gerar()

    return arvore


class ExibirArvore:
    def __init__(self, arvore):
        self.atributos = arvore.atributos
        self.arvore = arvore.arvore

    def exibir(self):
        self.exibirRecursivo(self.arvore)

    def exibirRecursivo(self, no, identacao=""):
        if not no.isFolha:
            if no.limiar is None:
                for index, filho in enumerate(no.filhos):
                    if filho.isFolha:
                        print(identacao + no.nome + " = " +
                              self.atributos[index] + " : " + filho.nome)
                    else:
                        print(identacao + no.nome + " = " +
                              self.atributos[index] + ": ")
                        self.exibirRecursivo(filho, identacao + "|  ")
            else:
                filho_esquerda = no.filhos[0]
                filho_direita = no.filhos[1]
                if filho_esquerda.isFolha:
                    print(identacao + no.nome + " <= " +
                          str(no.limiar) + " : " + filho_esquerda.nome)
                else:
                    print(identacao + no.nome + " <= " +
                          str(no.limiar)+" : ")
                    self.exibirRecursivo(filho_esquerda, identacao + "|  ")

                if filho_direita.isFolha:
                    print(identacao + no.nome + " > " +
                          str(no.limiar) + " : " + filho_direita.nome)
                else:
                    print(identacao + no.nome + " > " +
                          str(no.limiar) + " : ")
                    self.exibirRecursivo(filho_direita, identacao + "|  ")


class Arvore:
    def __init__(self, classes, atributos, data):
        self.classes = classes
        self.atributos = list(atributos.keys())
        self.data = data
        self.arvore = None

    def gerar(self):
        self.arvore = self.gerarArvore(self.data, self.atributos)

    def gerarArvore(self, data, atributos):
        if len(data) == 0:
            return No(True, "Error", None)

        classe_nome = self.classeNome(data)

        if len(classe_nome) == 1:
            return No(True, classe_nome[0], None)
        elif len(atributos) == 0:
            return No(True, self.classeDominante(data), None)
        else:
            (melhor_atributo, melhor_limiar,
                extremos) = self.separarAtributos(data, atributos)

            atributos_restantes = atributos[:]
            atributos_restantes.remove(melhor_atributo)

            no = No(False, melhor_atributo, melhor_limiar)
            no.filhos = [self.gerarArvore(
                sub_data, atributos_restantes) for sub_data in extremos]

            return no

    def classeNome(self, data):
        return list(set([x[-1] for x in data]))

    def classeDominante(self, data):
        frequencia = [0] * len(self.classes)

        for linha in data:
            index = self.classes.index(linha[-1])
            frequencia[index] += 1

        return self.classes[frequencia.index(max(frequencia))]

    def separarAtributos(self, data, atributos):
        extremos = []
        maior_entropia = -float('inf')
        melhor_atributo = -1
        melhor_limiar = None

        for atributo in atributos:
            atributo_index = self.atributos.index(atributo)

            data.sort(key=lambda x: x[atributo_index])

            for i in range(0, len(data) - 1):
                atual = data[i][atributo_index]
                proximo = data[i + 1][atributo_index]

                limiar = (atual + proximo) / 2

                if atual != proximo:
                    menores = []
                    maiores = []

                    for linha in data:
                        if linha[atributo_index] > limiar:
                            maiores.append(linha)
                        else:
                            menores.append(linha)

                    ganho = self.ganho(data, [menores, maiores])

                    if ganho >= maior_entropia:
                        extremos = [menores, maiores]
                        maior_entropia = ganho
                        melhor_atributo = atributo
                        melhor_limiar = limiar

        if melhor_atributo == -1:
            extremos = [data, data]
            melhor_atributo = atributos[0]
            melhor_limiar = limiar

        return (melhor_atributo, melhor_limiar, extremos)

    def ganho(self, data, extremos):
        total = len(data)
        impureza_antes_separar = self.entropia(data)

        pesos = [len(x)/total for x in extremos]

        impureza_depois_separar = 0

        for i in range(len(extremos)):
            peso = pesos[i] * self.entropia(extremos[i])
            impureza_depois_separar += peso

        return impureza_antes_separar - impureza_depois_separar

    def entropia(self, data):
        total = len(data)

        if total == 0:
            return 0

        frequencia = [0] * len(self.classes)

        for linha in data:
            index = self.classes.index(linha[-1])
            frequencia[index] += 1

        frequencia = [x/total for x in frequencia]
        entropia = sum([x * log(x, 2) if x != 0 else 0 for x in frequencia])

        return entropia * -1


class No:
    def __init__(self, isFolha, nome, limiar):
        self.nome = nome
        self.limiar = limiar
        self.isFolha = isFolha
        self.filhos = []
