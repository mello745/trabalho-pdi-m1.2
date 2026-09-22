# Imagens selecionadas (ISIC)

Fonte: International Skin Imaging Collaboration — https://www.isic-archive.com
Categoria: **Melanoma** (dermatoscópicas) · Região anatômica: **Tronco posterior (Posterior trunk)**

Critério de seleção: entre as 1.089 imagens dermatoscópicas de melanoma do tronco posterior no ISIC,
medimos contraste (faixa de intensidade entre os percentis 2–98), nitidez (variância do Laplaciano),
ruído/textura fina e brilho médio, e escolhemos imagens que ficam nos extremos de critérios **diferentes**.
Referência (mediana das 1.087 imagens com ≥ 600 px): faixa = 125, variância do Laplaciano = 89,6, brilho = 152.

| Arquivo | Diagnóstico | Resolução | Licença | Problema de qualidade | Por que foi escolhida |
|---|---|---|---|---|---|
| `ISIC_0014049.jpg` | Melanoma invasivo | 4288×2848 | CC-0 | **Contraste muito baixo** (faixa = 34 níveis) | Lesão quase da cor da pele: testa a operação pontual (equalização). Tem régua em mm (artefato). |
| `ISIC_7236365.jpg` | Melanoma in situ | 3264×2448 | CC-0 | **Pelos densos** (textura/ruído estrutural alto) | Compara Gaussiano × mediana; mostra o aguçamento realçando pelos (realce excessivo). |
| `ISIC_0021531.jpg` | Melanoma invasivo | 3072×2304 | CC-0 | **Desfocada, bordas difusas** (entre as 1% menos nítidas) | Melhor caso para o aguçamento; equalização tende a exagerar aqui. |
| `ISIC_0112420.jpg` *(opcional)* | Melanoma in situ | 768×576 | CC-BY | **Muito escura** (brilho médio = 53) | Caso para correção gama com γ < 1. |

Atribuição exigida (CC-BY) — `ISIC_0112420`: Department of Dermatology, University of Athens, Andreas Syggros
Hospital of Skin and Venereal Diseases, Alexander Stratigos, Konstantinos Liopyris.
`ISIC_7236365`: Memorial Sloan Kettering Cancer Center (CC-0, citação opcional).

**Observação:** as imagens grandes devem ser redimensionadas (ex.: ~1024 px de largura) ao carregar no
notebook, pois a convolução implementada manualmente fica lenta em 4k. Registrar isso no relatório.
