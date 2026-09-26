
"""Convolução 2D genérica.

Responsável: Heloisa Born.

Implementação manual utilizada como base para filtros espaciais
de suavização e aguçamento.

Proibido utilizar funções prontas como:
cv2.filter2D, scipy.ndimage.convolve e scipy.signal.convolve2d.
"""

import numpy as np


def gauss_create(sigma=1.0, size=3):
    """
    Cria um kernel Gaussiano 2D normalizado.

    Parâmetros
    ----------
    sigma : float
        Desvio-padrão da distribuição Gaussiana.

    size : int
        Tamanho do kernel. Deve ser um número ímpar.

    Retorno
    -------
    numpy.ndarray
        Kernel Gaussiano cuja soma dos elementos é igual a 1.
    """

    if size <= 0 or size % 2 == 0:
        raise ValueError("O tamanho do kernel deve ser positivo e ímpar.")

    if sigma <= 0:
        raise ValueError("Sigma deve ser maior que zero.")

    # Distância do centro do kernel.
    raio = size // 2

    kernel = np.zeros((size, size), dtype=np.float64)

    # Calcula manualmente cada elemento usando a fórmula Gaussiana 2D.
    for i in range(size):
        for j in range(size):

            x = i - raio
            y = j - raio

            kernel[i, j] = np.exp(
                -((x ** 2 + y ** 2) / (2 * sigma ** 2))
            )

    # Normaliza o kernel para que a soma seja igual a 1.
    kernel = kernel / np.sum(kernel)

    return kernel


def conv2d_float(imagem, kernel):
    """
    Aplica convolução 2D manual em uma imagem em tons de cinza.

    A função retorna valores em ponto flutuante, pois alguns filtros
    como Laplaciano e Sobel podem gerar valores negativos.

    Parâmetros
    ----------
    imagem : numpy.ndarray
        Imagem de entrada 2D.

    kernel : numpy.ndarray
        Máscara utilizada na convolução.

    Retorno
    -------
    numpy.ndarray
        Resultado da convolução em float64.
    """

    if imagem.ndim != 2:
        raise ValueError("A convolução espera uma imagem 2D em tons de cinza.")

    if kernel.ndim != 2:
        raise ValueError("O kernel deve possuir duas dimensões.")

    altura_kernel, largura_kernel = kernel.shape

    if altura_kernel % 2 == 0 or largura_kernel % 2 == 0:
        raise ValueError("As dimensões do kernel devem ser ímpares.")

    # Converte para float para evitar overflow e permitir valores negativos.
    imagem = imagem.astype(np.float64)
    kernel = kernel.astype(np.float64)

    # Na convolução, o kernel é rotacionado 180 graus.
    kernel_invertido = np.flip(kernel, axis=(0, 1))

    # Define o tamanho do padding necessário.
    pad_h = altura_kernel // 2
    pad_w = largura_kernel // 2

    # Adiciona zeros ao redor da imagem.
    imagem_padded = np.pad(
        imagem,
        ((pad_h, pad_h), (pad_w, pad_w)),
        mode="constant",
        constant_values=0
    )

    altura, largura = imagem.shape

    resultado = np.zeros(
        (altura, largura),
        dtype=np.float64
    )

    # Percorre pixel por pixel.
    for i in range(altura):
        for j in range(largura):

            # Seleciona a região da imagem correspondente ao tamanho do kernel.
            regiao = imagem_padded[
                i:i + altura_kernel,
                j:j + largura_kernel
            ]

            # Multiplica região e kernel elemento a elemento e soma tudo.
            resultado[i, j] = np.sum(regiao * kernel_invertido)

    return resultado


def normalize_minmax(imagem):
    """
    Normaliza os valores de uma imagem para o intervalo de 0 a 255.

    Utilizada principalmente para visualizar resultados como
    magnitude de gradiente do filtro Sobel.
    """

    imagem = imagem.astype(np.float64)

    minimo = np.min(imagem)
    maximo = np.max(imagem)

    # Evita divisão por zero caso todos os pixels tenham o mesmo valor.
    if maximo == minimo:
        return np.zeros_like(imagem)

    normalizada = (
        (imagem - minimo)
        / (maximo - minimo)
    ) * 255.0

    return normalizada
