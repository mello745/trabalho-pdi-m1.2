"""Transformações de intensidade (etapa 4 do fluxo).

Responsável: Gustavo Mello.
Proibido: cv2.equalizeHist, skimage.exposure.*, etc.
"""

import numpy as np

def histograma(img):
    """
    Conta quantos pixels existem de cada tom de cinza.

    img : matriz 2D uint8 (valores de 0 a 255).

    Devolve um vetor de 256 posições: contagem[t] = quantos pixels têm o tom t.
    """
    contagem = np.zeros(256, dtype=np.int64)

    for valor in img.ravel():
        contagem[valor] += 1

    return contagem

def aplicar_lut(img, tabela):
    """
    Aplica uma tabela de conversão (LUT, slide 11): tom antigo -> tom novo.

    img    : matriz 2D uint8.
    tabela : vetor de 256 posições uint8; tabela[t] é o novo valor do tom t.

    Toda operação pontual é "montar a tabela + aplicar a tabela". A indexação
    tabela[img] usa o valor de cada pixel como posição na tabela, para a imagem
    inteira de uma vez.
    """
    return tabela[img]

def equalizar_histograma(img):
    """
    Espalha os tons da imagem por toda a faixa 0–255 (equalização de histograma).

    img : matriz 2D uint8.

    Devolve uma matriz 2D uint8 do mesmo tamanho, com o contraste redistribuído.
    """
    h = histograma(img)
    total = img.size   #altura x largura = h.sum()

    acumulada = np.zeros(256, dtype=np.float64)
    soma = 0
    for t in range(256):
        soma += h[t]
        acumulada[t] = soma / total

    # fração acumulada do tom mais escuro que existe na imagem
    minima = acumulada[h > 0][0]

    # imagem com um tom só: não há contraste para espalhar, devolve igual
    # (sem isso a fórmula abaixo dividiria por zero)
    if minima == 1:
        return img.copy()

    # desconta a mínima para o tom mais escuro virar 0 e o mais claro virar 255
    #tabela de conversão: tom antigo -> tom novo
    tabela = np.round(255 * (acumulada - minima) / (1 - minima))
    tabela = np.clip(tabela, 0, 255).astype(np.uint8)

    #troca cada pixel pelo seu tom novo
    return aplicar_lut(img, tabela)

def correcao_gama(img, gama):
    """
    Clareia (gama < 1) ou escurece (gama > 1) a imagem, mexendo mais nos tons médios.

    img  : matriz 2D uint8.
    gama : expoente da curva. gama = 1 não muda nada.

    Devolve uma matriz 2D uint8 do mesmo tamanho.
    """
    if gama <= 0:
        raise ValueError("gama deve ser maior que zero.")

    # monta a tabela só para os 256 tons possíveis (em vez de ~700 mil pixels)
    tons = np.arange(256, dtype=np.float64)
    normalizada = tons / 255.0                        # 0–255  ->  0–1
    corrigida = normalizada ** gama                   # aplica a curva
    saida = corrigida * 255.0                         # 0–1  ->  0–255
    tabela = np.round(saida).astype(np.uint8)

    return aplicar_lut(img, tabela)
