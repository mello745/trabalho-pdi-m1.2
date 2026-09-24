"""Métricas de qualidade com referência (etapa 8 do fluxo).

Responsável: João Paulo Jorge.
Métricas escolhidas: PSNR (erro/ruído) + SSIM (estrutura). Referência = original sem ruído.
Proibido: skimage.metrics.*, cv2.PSNR.
"""

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def mse(img1, img2):
    a = img1.astype(np.float64)
    b = img2.astype(np.float64)
    return np.mean((a - b) ** 2)


def psnr(img1, img2, max_val=255.0):
    """PSNR em dB. Quanto maior, mais parecido com a referência (menos erro)."""
    erro = mse(img1, img2)
    if erro == 0:
        return float("inf")
    return 10 * np.log10((max_val**2) / erro)


def _janelas_media_variancia_covariancia(img1, img2, win=7):
    """Média, variância e covariância locais por janela win x win, via
    sliding_window_view (implementação própria, sem skimage.metrics.structural_similarity)."""
    a = sliding_window_view(img1, (win, win)).reshape(-1, win * win)
    b = sliding_window_view(img2, (win, win)).reshape(-1, win * win)

    mu_a, mu_b = a.mean(axis=1), b.mean(axis=1)
    var_a, var_b = a.var(axis=1), b.var(axis=1)
    cov_ab = ((a - mu_a[:, None]) * (b - mu_b[:, None])).mean(axis=1)

    return mu_a, mu_b, var_a, var_b, cov_ab


def ssim(img1, img2, win=7, max_val=255.0):
    """SSIM médio (janelas locais), implementação própria da fórmula de Wang et al."""
    a = img1.astype(np.float64)
    b = img2.astype(np.float64)

    c1 = (0.01 * max_val) ** 2
    c2 = (0.03 * max_val) ** 2

    mu_a, mu_b, var_a, var_b, cov_ab = _janelas_media_variancia_covariancia(a, b, win)

    numerador = (2 * mu_a * mu_b + c1) * (2 * cov_ab + c2)
    denominador = (mu_a**2 + mu_b**2 + c1) * (var_a + var_b + c2)

    return np.mean(numerador / denominador)
