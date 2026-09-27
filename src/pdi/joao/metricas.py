"""Métricas de qualidade com referência (etapa 8 do fluxo).

Responsável: João Paulo Jorge.
Métricas escolhidas: PSNR (erro/ruído) + SSIM (estrutura). Referência = original sem ruído.
Proibido: skimage.metrics.*, cv2.PSNR.
"""
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def _checar_mesmo_tamanho(img1, img2):
    # sem isso o NumPy faz broadcast e devolve um número sem sentido em vez de erro
    if img1.shape != img2.shape:
        raise ValueError(f"As imagens precisam ter o mesmo tamanho: {img1.shape} x {img2.shape}.")


def mse(img1, img2):
    _checar_mesmo_tamanho(img1, img2)
    a = img1.astype(np.float64)
    b = img2.astype(np.float64)
    return np.mean((a - b) ** 2)


def psnr(img1, img2, max_val=255.0):
    """PSNR em dB. Quanto maior, mais parecido com a referência (menos erro)."""
    erro = mse(img1, img2)
    if erro == 0:
        return float("inf")
    return 10 * np.log10((max_val**2) / erro)


def _media_local(img, win):
    """Média de cada janela win x win (uma por posição válida da janela).

    sliding_window_view só cria uma "visão" das janelas, sem copiar os pixels;
    a média é tirada direto nos dois últimos eixos (as linhas e colunas da janela).
    """
    return sliding_window_view(img, (win, win)).mean(axis=(-2, -1))


def _janelas_media_variancia_covariancia(img1, img2, win=7):
    """Média, variância e covariância locais por janela win x win.

    Usa var(x) = E[x²] - E[x]² e cov(x, y) = E[xy] - E[x]E[y], então só precisa
    de médias locais — evita montar uma matriz (n_janelas x win²), que numa
    imagem 1024 px passava de 1 GB de memória.
    """
    # float antes de multiplicar: em uint8, img1 * img1 estoura e volta para 0 sem avisar
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)

    mu_a = _media_local(img1, win)
    mu_b = _media_local(img2, win)

    var_a = _media_local(img1 * img1, win) - mu_a**2
    var_b = _media_local(img2 * img2, win) - mu_b**2
    cov_ab = _media_local(img1 * img2, win) - mu_a * mu_b

    return mu_a, mu_b, var_a, var_b, cov_ab


def ssim(img1, img2, win=7, max_val=255.0):
    """SSIM médio (janelas locais), implementação própria da fórmula de Wang et al.

    Diferença para o artigo: aqui a janela é uniforme 7x7; o artigo usa Gaussiana 11x11 (σ = 1.5).
    """
    _checar_mesmo_tamanho(img1, img2)
    a = img1.astype(np.float64)
    b = img2.astype(np.float64)

    c1 = (0.01 * max_val) ** 2
    c2 = (0.03 * max_val) ** 2

    mu_a, mu_b, var_a, var_b, cov_ab = _janelas_media_variancia_covariancia(a, b, win)

    numerador = (2 * mu_a * mu_b + c1) * (2 * cov_ab + c2)
    denominador = (mu_a**2 + mu_b**2 + c1) * (var_a + var_b + c2)

    return np.mean(numerador / denominador)