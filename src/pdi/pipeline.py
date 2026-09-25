"""Pipeline: aplica uma sequência de etapas na imagem, guardando o resultado de cada uma.

Responsável: Gustavo Mello.

Uma "etapa" é só um par (nome, função). A função recebe uma imagem e devolve outra.
A ordem da lista é a ordem do processamento — trocar a ordem ou uma função já cria
a segunda configuração exigida pelo enunciado.
"""
def executar(img, etapas):
    """
    Aplica as etapas em sequência e guarda o resultado de cada uma.

    img    : imagem de entrada (matriz 2D uint8).
    etapas : lista de pares (nome, função). Cada função recebe uma imagem
             e devolve outra.

    Devolve uma lista de pares (nome, imagem), começando pela original:
        [("original", img), ("degradada", ...), ..., ("agucada", ...)]
    """   
    resultados = [("original", img)]
    atual = img

    for nome, funcao in etapas:
        atual = funcao(atual)
        resultados.append((nome, atual))
    return resultados

def nomes(resultados):
    """Só os nomes das etapas, na ordem (para usar como títulos das figuras)."""
    return [nome for nome, imagem in resultados]

def imagens(resultados):
    """Só as imagens na ordem"""
    return [imagem for nome, imagem in resultados]

def final(resultados):
    """A imagem produzida pela útima etapa"""
    return resultados[-1][1]
