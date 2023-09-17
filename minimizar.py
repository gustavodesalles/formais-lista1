#8;P;{S,U,V,X};{0,1};P,0,Q;P,1,P;Q,0,T;Q,1,R;R,0,U;R,1,P;S,0,U;S,1,S;T,0,X;T,1,R;U,0,X;U,1,V;V,0,U;V,1,S;X,0,X;X,1,V
# 8;P;{S,U,V,X};{0,1};P,1,P;Q,0,T;Q,1,R;R,0,U;R,1,P;S,0,U;S,1,S;T,0,X;T,1,R;U,0,X;U,1,V;V,0,U;V,1,S;X,0,X;X,1,V
#minimizar para 5;P;{S};{0,1};P,0,Q;P,1,P;Q,0,T;Q,1,R;R,0,S;R,1,P;S,0,S;S,1,S;T,0,S;T,1,R

class Transicao:
    def __init__(self, origem, simbolo, destino):
        self.origem = origem
        self.simbolo = simbolo
        self.destino = destino

    def __repr__(self) -> str:
        return f"[{self.origem}, {self.simbolo}, {self.destino}]"

def obter_elementos(texto):
    return [i for i in texto if i != '{' and i != '}' and i != ',']

def obter_transicoes(transicoes_str):
    lista_transicoes = []
    conjunto_estados = set()
    for i in transicoes_str:
        origem, simbolo, destino = i.split(',')
        transicao = Transicao(origem, simbolo, destino)
        lista_transicoes.append(transicao)
        conjunto_estados.add(origem)
        conjunto_estados.add(destino)
    return (lista_transicoes, conjunto_estados)

def obter_transicoes_estado(estado, transicoes):
    return [i for i in transicoes if i.origem == estado]

def encontrar_estado_em_classe(estado, classes_equivalencia):
    for classe in classes_equivalencia:
        if estado in classe:
            return classes_equivalencia.index(classe)

def obter_classes_transicoes_estado(transicoes_estado, classes_equivalencia):
    lista_num_classes = []
    for i in transicoes_estado:
        lista_num_classes.append(encontrar_estado_em_classe(i.destino, classes_equivalencia))
    return lista_num_classes


def remover_inalcancaveis(estado_inicial, transicoes):
    alcancaveis = []
    alcancaveis.append(estado_inicial)
    for i in alcancaveis:
        for j in transicoes:
            if j.origem == i and j.destino not in alcancaveis:
                alcancaveis.append(j.destino)

    transicoes[:] = [i for i in transicoes if (i.origem in alcancaveis) and (i.destino in alcancaveis)]
    return set(alcancaveis)

def remover_mortos(estados_finais, transicoes):
    vivos = estados_finais.copy()
    for i in vivos:
        for j in transicoes:
            if j.destino == i and j.origem not in vivos:
                vivos.append(j.origem)
    
    transicoes[:] = [i for i in transicoes if (i.origem in vivos) and (i.destino in vivos)]
    return set(vivos)

def determinar_classes_equivalencia(estados, estados_finais, transicoes):
    k_menos_f = [estados.difference(estados_finais)]
    f = estados_finais
    classes_equivalencia = [k_menos_f, f]
    while True:
        dicionario_classes = dict()
        for estado in estados:
            lista_num_classe = obter_classes_transicoes_estado(obter_transicoes_estado(estado, transicoes), classes_equivalencia)
            dicionario_classes.setdefault(lista_num_classe, []).append(estado)
        lista_classes = list(dicionario_classes.values())
        if set(lista_classes) == set(classes_equivalencia):
            return lista_classes
        classes_equivalencia = lista_classes.copy()

def remover_equivalentes(estados, estados_finais, transicoes):
    lista_classes_equivalentes = determinar_classes_equivalencia(estados, estados_finais, transicoes)
    for classe in lista_classes_equivalentes:
        classe.sort()
        estado_superior = classe[0]

def ler():
    entrada = input()
    lista_entrada = entrada.split(";")
    num_estados, estado_inicial, estados_finais_str, alfabeto_str, transicoes_str = lista_entrada[0], lista_entrada[1], lista_entrada[2], lista_entrada[3], lista_entrada[4:]
    estados_finais = obter_elementos(estados_finais_str)
    alfabeto = obter_elementos(alfabeto_str)
    tupla_aux = obter_transicoes(transicoes_str)
    transicoes = tupla_aux[0]
    estados = tupla_aux[1]

    estados = remover_inalcancaveis(estado_inicial, transicoes)
    estados = remover_mortos(estados_finais, transicoes)
    print(estados)
    print(transicoes)

ler()
# print(obter_elementos("{a,b,cde}"))