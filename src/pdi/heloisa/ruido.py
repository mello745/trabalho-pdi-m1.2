
"""Inserção de ruído controlado (etapa 3 do fluxo).

Responsável: Heloisa Born.

Implementação própria da adição de ruído gaussiano.
Os parâmetros de intensidade (sigma) e semente devem ser registrados
para garantir que os experimentos possam ser reproduzidos.
"""

import numpy as np


def ruido_gaussiano(imagem, sigma=15.0, semente=42, media=0.0):
    """
    Adiciona ruído gaussiano controlado a uma imagem.

    Parâmetros
    ----------
    imagem : numpy.ndarray
        Imagem de entrada. Pode ser em tons de cinza ou RGB.

    sigma : float
        Desvio-padrão da distribuição gaussiana.
        Quanto maior o sigma, maior a intensidade do ruído.

    semente : int
        Semente utilizada pelo gerador de números pseudoaleatórios.
        Permite reproduzir exatamente o mesmo ruído em execuções diferentes.

    media : float
        Média da distribuição gaussiana.
        Por padrão é zero para não provocar um clareamento ou
        escurecimento sistemático da imagem.

    Retorno
    -------
    numpy.ndarray
        Imagem com ruído, no intervalo de 0 a 255 e tipo uint8.
    """

    # Sigma negativo não representa um desvio-padrão válido.
    if sigma < 0:
        raise ValueError("O valor de sigma deve ser maior ou igual a zero.")

    # Converte a imagem para ponto flutuante antes da soma.
    # Isso evita problemas de overflow do uint8 durante as operações.
    imagem_float = imagem.astype(np.float64)

    # Cria um gerador pseudoaleatório com uma semente fixa.
    # Com a mesma semente, conseguimos reproduzir o mesmo experimento.
    gerador = np.random.default_rng(semente)

    # Gera uma matriz de ruído com exatamente o mesmo formato da imagem.
    ruido = gerador.normal(
        loc=media,
        scale=sigma,
        size=imagem.shape
    )

    # Soma o ruído gerado aos valores dos pixels da imagem original.
    imagem_ruidosa = imagem_float + ruido

    # Garante que nenhum pixel fique abaixo de 0 ou acima de 255.
    imagem_ruidosa = np.clip(imagem_ruidosa, 0, 255)

    # Retorna ao formato padrão de imagens de 8 bits.
    # Arredonda antes de converter: astype sozinho trunca (127.9 viraria 127)
    # e deixaria o ruído com média negativa, escurecendo a imagem.
    return np.round(imagem_ruidosa).astype(np.uint8)
