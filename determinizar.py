# 4;A;{D};{a,b};A,a,A;A,a,B;A,b,A;B,b,C;C,b,D
# det. para 4;{A};{{AD}};{a,b};{A},a;{AB};{A},b,{A};{AB},a,{AB};{AB};b,{AC};{AC},a,{AB};{AC},b,{AD};{AD},a,{AB};{AD},b,{A}
#4;P;{S};{0,1};P,0,P;P,0,Q;P,1,P;Q,0,R;Q,1,R;R,0,S;S,0,S;S,1,S
#3;A;{C};{1,2,3,&};A,1,A;A,&,B;B,2,B;B,&,C;C,3,C

class Transicao:
    def __init__(self, origem, simbolo, destino):
        self.origem = origem
        self.simbolo = simbolo
        self.destino = destino

    def __repr__(self) -> str:
        return f"{self.origem},{self.simbolo},{self.destino}"

def obter_elementos(texto):
    return [i for i in texto if i != '{' and i != '}' and i != ',']

def obter_transicoes_estado(estado, transicoes):
    return [i for i in transicoes if i.origem == estado]

def obter_transicoes_nd_estado(estado, simbolo, transicoes):
    return [i for i in transicoes if i.origem == estado and i.simbolo == simbolo]

def obter_transicoes_nd_estado_composto(estado, simbolo, transicoes):
    return [i for i in transicoes if i.origem in estado and i.simbolo == simbolo]

def obter_destinos_nd_estado_composto(estado, simbolo, transicoes):
    # return [i.destino for i in transicoes if i.origem in estado and i.simbolo == simbolo]
    destinos = set()
    for i in transicoes:
        if i.origem.issubset(estado) and i.simbolo == simbolo:
            destinos = destinos.union(i.destino)
    return destinos

def obter_transicoes_epsilon_estado(estado, transicoes):
    return [i.destino for i in transicoes if i.origem == estado and i.simbolo == '&']

def obter_transicoes(transicoes_str):
    lista_transicoes = []
    lista_estados = []
    for i in transicoes_str:
        origem, simbolo, destino = i.split(',')
        transicao = Transicao(origem, simbolo, destino)
        lista_transicoes.append(transicao)
        if origem not in lista_estados:
            lista_estados.append(origem)
        if destino not in lista_estados:
            lista_estados.append(destino)
    return (lista_transicoes, lista_estados)

def obter_epsilon_fecho(estado, estado_inicial, transicoes):
    epsilon_fecho = []
    epsilon_fecho.append(estado)
    for e in epsilon_fecho:
        for t in obter_transicoes_epsilon_estado(e, transicoes):
            epsilon_fecho.append(t)
    for transicao in transicoes:
        if transicao.origem == estado:
            transicao.origem = set(epsilon_fecho)
        if transicao.destino == estado:
            transicao.destino = set(epsilon_fecho)
    if estado_inicial == estado:
        estado_inicial = set(epsilon_fecho)
    return set(epsilon_fecho)

def obter_epsilon_fechos(estados, estado_inicial, transicoes):
    for estado in estados:
        epsilon_fecho = obter_epsilon_fecho(estado, estado_inicial, transicoes)
        estados[estados.index(estado)] = epsilon_fecho

def obter_estados_novos(estado_inicial, alfabeto, transicoes):
    estados_novos = []
    transicoes_novas = []
    estados_novos.append(estado_inicial)
    for e in estados_novos:
        for a in alfabeto:
            estado_novo = set()
            estado_novo = estado_novo.union(obter_destinos_nd_estado_composto(e, a, transicoes))
            if estado_novo not in estados_novos:
                estados_novos.append(estado_novo)
            transicao_nova = Transicao(e, a, estado_novo)
            if estado_novo in estados_novos and transicao_nova not in transicoes_novas:
                transicoes_novas.append(Transicao(e, a, estado_novo))
    return (estados_novos, transicoes_novas)           

def encontrar_novos_estados_finais(estados_novos, estados_finais):
    novos_finais = []
    for e in estados_novos:
        for f in estados_finais:
            if set(f).issubset(e) and e not in novos_finais:
                novos_finais.append(e)
    return novos_finais

def formatar_listas_estados(lista):
    lista_final = []
    for i in lista:
        lista_final.append(formatar_set(i))
    return ",".join(lista_final)

def formatar_set(conjunto):
    return "".join(sorted(list(conjunto)))

def formatar_transicoes(transicoes):
    transicoes_str = []
    for i in transicoes:
        aux = f"{{{formatar_set(i.origem)}}},{i.simbolo},{{{formatar_set(i.destino)}}}"
        transicoes_str.append(aux)
    return transicoes_str

def ler():
    entrada = input()
    lista_entrada = entrada.split(";")
    num_estados, estado_inicial, estados_finais_str, alfabeto_str, transicoes_str = lista_entrada[0], {lista_entrada[1]}, lista_entrada[2], lista_entrada[3], lista_entrada[4:]
    estados_finais = obter_elementos(estados_finais_str)
    alfabeto = obter_elementos(alfabeto_str)
    tupla_aux = obter_transicoes(transicoes_str)
    transicoes = tupla_aux[0]
    estados = tupla_aux[1]

    # obter_estados_novos(estados, alfabeto, transicoes)
    obter_epsilon_fechos(estados, estado_inicial, transicoes)
    (estados_novos, transicoes_novas) = obter_estados_novos(estado_inicial, alfabeto, transicoes)
    # print(estados_novos)
    # print(transicoes_novas)
    novos_finais = encontrar_novos_estados_finais(estados_novos, estados_finais)
    # print(novos_finais)
    # print(formatar_listas_estados(estados_novos))
    # print(formatar_listas_estados(novos_finais))
    print(f"{len(estados_novos)};{{{formatar_set(estado_inicial)}}};{{{{{','.join({formatar_listas_estados(novos_finais)})}}}}};{{{','.join(alfabeto)}}};{';'.join(formatar_transicoes(transicoes_novas))}")

ler()