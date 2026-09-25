"""Leitura, escrita e visualização de imagens.

Responsável: Gustavo Mello.
Bibliotecas aqui são permitidas: só carregam/salvam/plotam, não processam.
"""
import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def carregar_cinza(caminho, largura_max=1024):
    """
    Abre uma imagem do disco, reduz se for grande e converte para tons de cinza.

    caminho     : caminho do arquivo de imagem (ex.: "data/originais/ISIC_0014049.jpg").
    largura_max : largura máxima em pixels. Imagens mais largas são reduzidas para
                  essa largura, e a altura é ajustada na mesma proporção para a
                  lesão não ficar deformada. Imagens menores não são alteradas.

    Devolve uma matriz 2D (altura, largura), dtype uint8, com valores de 0 a 255.

    A conversão usa a fórmula ponderada, I = 0.299R + 0.587G + 0.114B,
    implementada manualmente: os pesos seguem a sensibilidade do olho humano,
    que é maior ao verde e menor ao azul.
    """
    img = Image.open(caminho)

    img = img.convert("RGB") #Converte imagens de diferentes tipos para RGB assim padronizando os canais para sempre 3, faciltando na conversão para cinza

    largura, altura = img.size

    if largura > largura_max:
        nova_largura = largura_max
        nova_altura = int((nova_largura / largura) * altura) # regra de 3
        img = img.resize((nova_largura, nova_altura))

    arr = np.array(img)

    R = arr[:, :, 0]
    G = arr[:, :, 1]
    B = arr[:, :, 2]

    R = R.astype(np.float64)
    G = G.astype(np.float64)
    B = B.astype(np.float64)

    cinza = (0.299 * R) + (0.587 * G) + (0.114 * B)
    cinza = np.round(cinza).astype(np.uint8)

    return cinza

def salvar(img, caminho):
    """
    Salva uma imagem em tons de cinza no disco. É o caminho inverso do carregar_cinza:
    array -> imagem da Pillow -> arquivo.

    img     : matriz 2D (altura, largura), dtype uint8, valores de 0 a 255.
    caminho : onde salvar (ex.: "../resultados/ISIC_0014049_equalizada.png").
              Se a pasta ainda não existir, ela é criada.

    Não devolve nada, o resultado é o arquivo criado.

    Use sempre .png: o PNG guarda os pixels exatamente como estão. O JPG comprime
    alterando os valores dos pixels, o que falsearia a comparação por métricas.
    """
    pasta = os.path.dirname(caminho)
    if pasta:
        os.makedirs(pasta, exist_ok=True)  # cria a pasta (e as de cima) se faltar

    Image.fromarray(img).save(caminho)

def mostrar(imagens, titulos):
    """
    Mostra várias imagens lado a lado e, embaixo de cada uma, o seu histograma.

        | imagem 1 | imagem 2 | imagem 3 |   <- linha 0: as imagens
        | hist. 1  | hist. 2  | hist. 3  |   <- linha 1: os histogramas

    imagens : lista de matrizes 2D uint8 (ex.: [original, equalizada]).
    titulos : lista de textos, um para cada imagem, na mesma ordem.

    Não devolve nada; só desenha a figura.

    Detalhes importantes:
    - vmin=0 e vmax=255 fixam a escala de cinza. Sem isso o matplotlib estica o
      contraste de cada imagem sozinho, e o antes/depois de uma operação pontual
      pareceria igual.
    - set_xlim(0, 255) deixa todos os histogramas na mesma escala horizontal,
      para dar para comparar um com o outro.
    - squeeze=False garante que "eixos" seja sempre uma grade 2D, mesmo com uma
      única imagem, então eixos[linha][coluna] funciona em qualquer caso.
    """
    n = len(imagens)
    fig, eixos = plt.subplots(2, n, figsize=(4 * n, 6), squeeze=False)

    for i in range(n):
        # linha 0: a imagem
        eixos[0][i].imshow(imagens[i], cmap="gray", vmin=0, vmax=255)
        eixos[0][i].set_title(titulos[i])
        eixos[0][i].axis("off")

        # linha 1: o histograma (quantos pixels existem de cada tom, de 0 a 255)
        # TODO: trocar np.bincount pela nossa histograma() quando operacoes_pontuais.py estiver pronto
        contagem = np.bincount(imagens[i].ravel(), minlength=256)
        eixos[1][i].bar(range(256), contagem, width=1)
        eixos[1][i].set_xlim(0, 255)

    plt.tight_layout()
    plt.show()


