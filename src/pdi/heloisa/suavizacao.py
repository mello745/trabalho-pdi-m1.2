
"""Filtragem espacial – suavização (etapa 5 do fluxo).

Responsável: Heloisa Born.

Implementação própria de filtros de suavização:
- filtro Gaussiano;
- filtro de mediana.

Proibido utilizar funções prontas como:
cv2.GaussianBlur, cv2.medianBlur, cv2.blur e scipy.ndimage.*.
"""

import numpy as np

from pdi.heloisa.convolucao import conv2d_float, gauss_create


def filtro_gaussiano(imagem, tamanho=5, sigma=1.0):
    """
    Aplica suavização Gaussiana em uma imagem.

    Parâmetros
    ----------
    imagem : numpy.ndarray
        Imagem de entrada em tons de cinza.

    tamanho : int
        Tamanho do kernel Gaussiano. Deve ser ímpar.

    sigma : float
        Desvio-padrão utilizado na criação do kernel Gaussiano.

    Retorno
    -------
    numpy.ndarray
        Imagem suavizada no intervalo de 0 a 255.
    """

    # Cria o kernel Gaussiano.
    kernel = gauss_create(
        sigma=sigma,
        size=tamanho
    )

    # Aplica a convolução manual implementada em convolucao.py.
    resultado = conv2d_float(
        imagem,
        kernel
    )

    # Garante valores válidos para uma imagem de 8 bits.
    # Arredonda antes de converter: astype sozinho trunca (14.9999 viraria 14).
    resultado = np.clip(np.round(resultado), 0, 255)

    return resultado.astype(np.uint8)


def filtro_mediana(imagem, tamanho=3):
    """
    Aplica filtro de mediana manual em uma imagem.

    Para cada pixel, os valores da vizinhança são ordenados
    e o valor central da lista é utilizado como novo pixel.

    Parâmetros
    ----------
    imagem : numpy.ndarray
        Imagem de entrada em tons de cinza.

    tamanho : int
        Tamanho da janela. Deve ser positivo e ímpar.

    Retorno
    -------
    numpy.ndarray
        Imagem suavizada no formato uint8.
    """

    if imagem.ndim != 2:
        raise ValueError("O filtro de mediana espera uma imagem 2D.")

    if tamanho <= 0 or tamanho % 2 == 0:
        raise ValueError("O tamanho da janela deve ser positivo e ímpar.")

    raio = tamanho // 2

    # Padding nas bordas para preservar o tamanho da imagem.
    imagem_padded = np.pad(
        imagem,
        ((raio, raio), (raio, raio)),
        mode="edge"
    )

    altura, largura = imagem.shape

    resultado = np.zeros(
        (altura, largura),
        dtype=np.uint8
    )

    # Percorre todos os pixels da imagem.
    for i in range(altura):
        for j in range(largura):

            # Seleciona a vizinhança do pixel atual.
            regiao = imagem_padded[
                i:i + tamanho,
                j:j + tamanho
            ]

            # Transforma a região em uma lista única de valores.
            valores = regiao.flatten()

            # Ordena os valores.
            valores_ordenados = np.sort(valores)

            # Como a janela tem tamanho ímpar, existe um único valor central.
            indice_central = len(valores_ordenados) // 2

            resultado[i, j] = valores_ordenados[indice_central]

    return resultado
