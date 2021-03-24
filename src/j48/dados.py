def carregaAtributos(caminho_atributos):
    with open(caminho_atributos, 'r') as arquivo:
        classes = [x.strip() for x in arquivo.readline().split(',')]
        atributos = {}

        for linha in arquivo:
            [atributo, valor] = [x.strip() for x in linha.split(":")]
            atributos[atributo] = valor

    return (classes, atributos)


def carregaData(caminho_data, atributos):
    tipos = list(atributos.keys())

    with open(caminho_data, 'r') as arquivo:
        data = []

        for linha in arquivo:
            valores = [x.strip() for x in linha.split(",")]

            if valores != [] or valores != [""]:
                novos_valores = [mudaTipo(atributos[i], valores[tipos.index(i)])
                                 for i in tipos]
                novos_valores.append(valores[-1])
                data.append(novos_valores)

    return data


def mudaTipo(tipo, valor):
    tipos = {"int": int, "float": float}

    return (tipos[tipo])(valor)
