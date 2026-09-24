"""Filtragem espacial – aguçamento (etapa 6 do fluxo).

Responsável: João Paulo Jorge.
O resultado final NÃO pode ser só bordas: sempre combinar com a imagem.
Proibido: cv2.Laplacian, cv2.Sobel, skimage.filters.*.
"""

import numpy as np

from pdi.heloisa.convolucao import conv2d_float, gauss_create, normalize_minmax

KERNEL_LAPLACIANO = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]], dtype=np.float64)
KERNEL_SOBEL_X = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
KERNEL_SOBEL_Y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float64)


def _clip_uint8(img):
    return np.clip(img, 0, 255).astype(np.uint8)


def laplacian_sharpen(img, c=1.0):
    """Aguçamento com Laplaciano: saída = f + c * laplaciano(f).

    Com o kernel usado (centro positivo), somar o laplaciano realça bordas mantendo
    o restante da imagem — por isso o resultado não vira "só bordas".
    """
    laplaciano = conv2d_float(img, KERNEL_LAPLACIANO)
    saida = img.astype(np.float64) + c * laplaciano
    return _clip_uint8(saida)


def sobel_edges(img):
    """Magnitude do gradiente de Sobel, normalizada para [0, 255]."""
    gx = conv2d_float(img, KERNEL_SOBEL_X)
    gy = conv2d_float(img, KERNEL_SOBEL_Y)
    magnitude = np.sqrt(gx**2 + gy**2)
    return _clip_uint8(normalize_minmax(magnitude))


def highboost(img, size=3, sigma=1.0, k=1.5):
    """High-boost filtering: realça detalhes de alta frequência.

    1. borra a imagem (gaussiano);
    2. máscara = original - borrada (componente de alta frequência);
    3. saída = original + k * máscara (k > 1 => high-boost; k = 1 => unsharp masking).
    """
    kernel = gauss_create(sigma=sigma, size=size)
    borrada = conv2d_float(img, kernel)

    mascara = img.astype(np.float64) - borrada
    saida = img.astype(np.float64) + k * mascara
    return _clip_uint8(saida)
