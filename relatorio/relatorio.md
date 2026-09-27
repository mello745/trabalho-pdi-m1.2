# Relatório – Projeto M1: Operações Pontuais e Filtragem Espacial

> Figuras e tabelas saem dos notebooks: `trabalho_m1.ipynb` (comparativo principal), `config1_pipeline.ipynb` e
> `config2_pipeline.ipynb`; as imagens finais ficam em `resultados/`.
> Versão final: exportar para PDF.

## 1. Identificação

- **Universidade:** Universidade do Vale do Itajaí (UNIVALI)
- **Curso:** Ciência da Computação
- **Disciplina:** Processamento de Imagens
- **Professor:** Felipe Viel
- **Trabalho:** Projeto M1 – Operações Pontuais e Filtragem Espacial
- **Integrantes:** Gustavo Corrêa de Mello · Heloisa Cavalcante Born · João Paulo Jorge Aimi
- **Data:** 28/09/2026
- **Repositório:** https://github.com/mello745/trabalho-pdi-m1.2

## 2. Enunciado do projeto

Desenvolver, em Python e sem funções prontas de filtragem ou de operações pontuais, um pipeline de melhoria de
imagens médicas do conjunto ISIC (International Skin Imaging Collaboration). O grupo deve selecionar três melanomas
de uma mesma região anatômica, caracterizar seus problemas de qualidade, inserir ruído controlado e aplicar, em
sequência, uma **operação pontual** (transformação de intensidade), uma **suavização** e um **aguçamento**. Pelo
menos duas configurações do pipeline (variando técnica, parâmetro ou ordem) devem ser comparadas visual e
quantitativamente com duas métricas vistas em aula, identificando a melhor configuração para cada imagem e os casos
em que alguma técnica se comportou de forma inadequada.

## 3. Contexto da aplicação

Imagens dermatoscópicas são usadas como entrada para etapas posteriores de análise computacional, como segmentação
e classificação de lesões de pele. Variações de iluminação, contraste, ruído e definição das estruturas interferem
tanto na interpretação humana quanto no desempenho desses métodos. Antes dessa etapa, é necessário avaliar se o
processamento melhora a qualidade **sem introduzir artefatos** que prejudiquem estruturas relevantes.

Os desafios tratados são:

1. **Variação de contraste** — lesão e pele com tons muito próximos;
2. **Ruído** — interferências que mascaram informações e prejudicam operações posteriores;
3. **Perda de detalhes** — a suavização pode eliminar pequenas estruturas junto com o ruído;
4. **Realce excessivo** — o aguçamento pode saturar ou intensificar ruído e artefatos;
5. **Diferenças entre imagens** — uma técnica boa em uma imagem pode ser inadequada em outra.

## 4. Seleção e caracterização das imagens

Foram consideradas as **1.089 imagens dermatoscópicas de melanoma do tronco posterior** do ISIC (a região com mais
imagens). Para cada uma foram medidos contraste (faixa entre os percentis 2 e 98), nitidez (variância do Laplaciano),
textura fina e brilho médio, e foram escolhidas imagens que ficam nos extremos de critérios **diferentes**:

| Imagem | Diagnóstico | Licença | Problema principal |
|---|---|---|---|
| ISIC_0014049 | Melanoma invasivo | CC-0 | **contraste muito baixo** |
| ISIC_7236365 | Melanoma in situ | CC-0 | **pelos densos** (ruído estrutural) |
| ISIC_0021531 | Melanoma invasivo | CC-0 | **bordas difusas** (levemente desfocada) |
| ISIC_0112420 *(teste extra)* | Melanoma in situ | CC-BY¹ | **muito escura** |

¹ Department of Dermatology, University of Athens, Andreas Syggros Hospital, A. Stratigos, K. Liopyris.

As imagens são convertidas para tons de cinza pela fórmula de luminância `I = 0,299R + 0,587G + 0,114B`
(implementada manualmente; os pesos seguem a sensibilidade do olho humano, maior ao verde) e reduzidas para 1024 px
de largura, mantendo a proporção, porque a convolução manual seria lenta em 4288 px.

| Imagem | Tamanho | Média | Desvio padrão | Faixa p2–p98 |
|---|---|---|---|---|
| ISIC_0014049 | 1024×680 | 128,4 | 7,4 | 102–137 |
| ISIC_7236365 | 1024×768 | 158,4 | 41,6 | 65–223 |
| ISIC_0021531 | 1024×768 | 160,2 | 23,5 | 80–185 |

- **ISIC_0014049:** histograma estreito e alto; pele e lesão têm tons quase iguais.
- **ISIC_7236365:** contraste já alto, mas os pelos escuros cruzam a lesão e podem ser amplificados pelo realce.
- **ISIC_0021531:** contraste intermediário e lesão sem contorno nítido; a que mais depende do aguçamento.

*(Figura: originais + histogramas — `trabalho_m1.ipynb`, seção 1.)*

## 5. Desenvolvimento

O código está organizado por membro em `src/pdi/` e é chamado pelo notebook. A sequência de etapas é executada por
`pipeline.executar(imagem, etapas)`, que recebe uma lista de pares `(nome, função)`, aplica uma etapa após a outra e
guarda todos os estágios intermediários (para mostrar e medir cada um).

```python
def executar(img, etapas):
    resultados = [("original", img)]
    atual = img
    for nome, funcao in etapas:
        atual = funcao(atual)
        resultados.append((nome, atual))
    return resultados
```

### 5.1 Inserção de ruído — **Heloisa**

Para degradar as imagens de forma controlada, foi implementada a adição de **ruído Gaussiano**. Para cada pixel da imagem é gerado um valor aleatório segundo uma distribuição normal, que é somado à intensidade original:

`I_degradada = I_original + N(0, σ²)`

Nos experimentos foi utilizado `σ = 15`, com média igual a zero e `semente = 42`. A média zero evita introduzir intencionalmente um clareamento ou escurecimento global na imagem, enquanto a semente fixa permite reproduzir o mesmo ruído em novas execuções.

Após a soma, os valores são limitados ao intervalo `[0, 255]` e arredondados, evitando intensidades inválidas para imagens de 8 bits. A implementação foi realizada com NumPy, sem utilização de uma função pronta de adição de ruído.

Os mesmos parâmetros de ruído são utilizados nas três imagens para manter as comparações entre as configurações sob as mesmas condições.

Trecho principal da implementação:

```python
gerador = np.random.default_rng(semente)
ruido = gerador.normal(
    loc=media,
    scale=sigma,
    size=imagem.shape
)

imagem_ruidosa = imagem.astype(np.float64) + ruido
imagem_ruidosa = np.clip(imagem_ruidosa, 0, 255)
return np.round(imagem_ruidosa).astype(np.uint8)
```

### 5.2 Operação pontual — **Gustavo**

Operações pontuais transformam cada pixel usando **apenas o seu próprio valor** (`s = T(r)`), sem olhar a vizinhança.
Por isso podem ser implementadas como uma **tabela de conversão (LUT)** de 256 posições: monta-se a tabela
"tom antigo → tom novo" e depois cada pixel é trocado pelo valor da tabela. As duas técnicas usam a mesma função
auxiliar `aplicar_lut`.

**Histograma.** Implementado pelo pseudocódigo da aula: um vetor de 256 contadores, somando 1 na posição do valor de
cada pixel. É usado na equalização e em todas as figuras do trabalho.

**Equalização de histograma (configuração 1).** Usa a fração acumulada de pixels (CDF) para redistribuir os tons por
toda a faixa 0–255. Desconta-se a fração do tom mais escuro para que ele vire 0 e o mais claro vire 255:

`s = round(255 · (CDF(r) − CDF_min) / (1 − CDF_min))`

Se a imagem tiver um único tom, ela é devolvida sem alteração (não há contraste a espalhar). O resultado foi idêntico
ao `cv2.equalizeHist` nas quatro imagens (diferença máxima 0; OpenCV usado apenas para conferência).

**Correção gama (configuração 2).** `s = 255 · (r / 255)^γ`. Com γ < 1 a imagem clareia; com γ > 1 escurece; 0 e 255
não mudam. Foi escolhido **γ = 1,5**: as três imagens são claras (média 128–160), e γ > 1 abre a faixa dos tons claros,
onde estão pele e lesão. Um teste com γ = 0,8 **reduziu** o contraste final (ex.: desvio 38,9 contra 49,3 na
ISIC_7236365).

```python
def equalizar_histograma(img):
    h = histograma(img)
    total = img.size
    acumulada = np.zeros(256, dtype=np.float64)
    soma = 0
    for t in range(256):
        soma += h[t]
        acumulada[t] = soma / total
    minima = acumulada[h > 0][0]
    if minima == 1:
        return img.copy()
    tabela = np.round(255 * (acumulada - minima) / (1 - minima))
    tabela = np.clip(tabela, 0, 255).astype(np.uint8)
    return aplicar_lut(img, tabela)
```

**Efeito nas três imagens** (desvio padrão como medida de contraste):

| Imagem | Original | Equalizada | Gama γ = 1,5 |
|---|---|---|---|
| ISIC_0014049 | 7,4 | 75,0 | 7,6 |
| ISIC_7236365 | 41,6 | 73,8 | 47,3 |
| ISIC_0021531 | 23,5 | 74,4 | 25,8 |

A equalização dá o maior ganho de contraste, mas de forma agressiva: na ISIC_0014049 transforma a textura da pele em
manchas, e o histograma fica "em pente", porque ela não cria tons novos, só redistribui os existentes. O gama é suave e
previsível, mas o ganho é pequeno na imagem de contraste mais baixo.

### 5.3 Suavização — **Heloisa**

A etapa de suavização tem como objetivo reduzir o ruído artificial inserido anteriormente, buscando preservar o máximo possível dos detalhes relevantes da imagem. Foram implementados dois métodos: **filtro Gaussiano** e **filtro de mediana**.

#### Convolução

Para permitir a aplicação dos filtros espaciais, foi implementada uma função própria de convolução 2D. Para cada posição da imagem, uma vizinhança com o mesmo tamanho do kernel é selecionada. O kernel é rotacionado em 180 graus, os elementos correspondentes são multiplicados e os produtos são somados para gerar o novo valor do pixel.

Foi utilizado padding do tipo edge na convolução, repetindo os valores mais próximos das bordas para preservar as dimensões da imagem de saída sem introduzir valores artificiais iguais a zero. O resultado é calculado em `float64`, pois alguns kernels utilizados posteriormente, como Laplaciano e Sobel, podem gerar valores negativos.

#### Filtro Gaussiano

O kernel Gaussiano é calculado manualmente a partir da distribuição Gaussiana e depois normalizado para que a soma dos seus elementos seja igual a 1.

Nos testes foi utilizado um kernel de tamanho **5 × 5**, com `σ = 1.0`. O filtro Gaussiano realiza uma média ponderada da vizinhança, dando maior peso aos pixels próximos ao centro.

#### Filtro de mediana

Também foi implementado um filtro de mediana com janela **3 × 3**. Para cada pixel, os nove valores da vizinhança são ordenados e o valor central é utilizado como novo valor do pixel.

Neste filtro, as bordas são tratadas repetindo os valores mais próximos (`padding` do tipo `edge`), evitando a introdução de zeros artificiais na vizinhança.

Os dois filtros foram implementados sem utilização de funções prontas de filtragem.

Trechos principais da implementação:

```python
# Filtro Gaussiano
kernel = gauss_create(sigma=sigma, size=tamanho)
resultado = conv2d_float(imagem, kernel)

# Mediana
valores_ordenados = np.sort(regiao.flatten())
indice_central = len(valores_ordenados) // 2
resultado[i, j] = valores_ordenados[indice_central]
```

### 5.4 Aguçamento — **João Paulo**

Foram implementadas três técnicas, todas sobre a convolução manual da seção 5.3:

- **Sobel:** magnitude do gradiente `√(Gx² + Gy²)`. Gera **apenas as bordas**; é usado no notebook só para visualizar
  a informação de alta frequência, não como resultado final (o enunciado não aceita uma imagem só de bordas).
- **Laplaciano:** kernel `[[0,−1,0],[−1,4,−1],[0,−1,0]]` (centro positivo), com `saída = f + c·∇²f`. Somar o Laplaciano
  à imagem realça as transições sem perder o restante da imagem.
- **High-boost (escolhido para as duas configurações):** `máscara = f − borrada`, `saída = f + k·máscara`, com borramento
  Gaussiano 3×3 (σ = 1) e **k = 1,5**. A borrada é mantida em `float64` para a máscara não perder diferenças pequenas,
  que são justamente os detalhes. O ganho `k` controla quanto detalhe é somado, e o borramento interno torna o
  high-boost menos sensível ao ruído que o Laplaciano puro.

```python
kernel = gauss_create(sigma=sigma, size=tamanho)
borrada = conv2d_float(img, kernel)
mascara = img.astype(np.float64) - borrada
saida = img.astype(np.float64) + k * mascara
return np.clip(np.round(saida), 0, 255).astype(np.uint8)
```

### 5.5 Configurações testadas — **todos**

| Etapa | Configuração 1 | Configuração 2 |
|---|---|---|
| 1 | ruído Gaussiano (σ = 15, semente 42) | ruído Gaussiano (σ = 15, semente 42) |
| 2 | equalização de histograma | **mediana 3×3** |
| 3 | Gaussiano 5×5, σ = 1 | **correção gama γ = 1,5** |
| 4 | high-boost k = 1,5 | high-boost k = 1,5 |

A configuração 2 muda a **ordem** (suaviza antes da operação pontual), a **técnica de suavização** e a **operação
pontual**. A hipótese testada é que realçar o contraste de uma imagem ainda ruidosa amplifica o ruído, e que suavizar
antes evita isso. As duas configurações partem da mesma imagem degradada (mesma semente), o que torna a comparação
justa.

## 6. Métricas

**Responsável:** João Paulo

Foram escolhidas duas das métricas vistas em aula, ambas com a imagem original (sem ruído) como referência:

- **PSNR** (Peak Signal-to-Noise Ratio): `PSNR = 10·log10(255² / MSE)`, com `MSE = média((f − g)²)`. Medido em dB,
  quanto maior melhor (≥ 20 dB é considerado bom). É a métrica clássica para avaliar **remoção de ruído**.
- **SSIM** (Structural Similarity): compara médias, variâncias e covariâncias locais,
  `SSIM = ((2μxμy + C1)(2σxy + C2)) / ((μx² + μy² + C1)(σx² + σy² + C2))`, de −1 a 1 (1 = idênticas). Mede a
  **preservação da estrutura**, sendo sensível à perda de detalhe pela suavização e a artefatos do aguçamento.

As duas são complementares: uma mede erro de intensidade e a outra estrutura. A implementação do SSIM usa janelas
uniformes 7×7 e as identidades `var(x) = E[x²] − E[x]²` e `cov(x,y) = E[xy] − E[x]E[y]`, calculando apenas médias
locais.

## 7. Resultados

**Responsável:** Heloisa

*(Figuras: `resultados/<imagem>_degradada.png`, `_config1.png`, `_config2.png`; estágios completos em `config1_pipeline.ipynb` e `config2_pipeline.ipynb`; lado a lado em `trabalho_m1.ipynb`, seção 7.)*

PSNR (dB) / SSIM de cada estágio, com a original como referência:

| Estágio | ISIC_0014049 | ISIC_7236365 | ISIC_0021531 |
|---|---|---|---|
| Degradada | 24,60 / 0,240 | 24,61 / 0,401 | 24,60 / 0,232 |
| C1 – equalizada | 11,08 / 0,022 | 14,32 / 0,227 | 11,58 / 0,035 |
| C1 – suavizada (Gaussiano) | 19,11 / 0,205 | 15,68 / 0,617 | 14,41 / 0,276 |
| **C1 – final (high-boost)** | 17,51 / 0,119 | 15,52 / 0,513 | 14,10 / 0,168 |
| C2 – suavizada (mediana) | 32,22 / 0,664 | 30,87 / 0,741 | 32,31 / 0,662 |
| C2 – gama | 16,60 / 0,599 | 18,03 / 0,666 | 17,75 / 0,569 |
| **C2 – final (high-boost)** | 16,37 / 0,357 | 17,57 / 0,464 | 17,38 / 0,320 |

Teste extra com a imagem escura ISIC_0112420 (`trabalho_m1.ipynb`, seção 10): degradada 24,94 / 0,397;
configuração 1 final 10,18 / 0,375; configuração 2 final 19,01 / 0,459.

Visualmente, a configuração 1 produz contraste muito maior e a lesão fica bem destacada, mas o fundo fica granulado;
a configuração 2 é limpa e fiel à original, com ganho de contraste pequeno.

## 8. Análise e discussão

**Responsável:** Heloisa + João Paulo

**Melhor configuração por imagem:**

- **ISIC_0021531 (bordas difusas): configuração 2.** Maior PSNR e SSIM; a lesão fica com contorno mais definido sem
  granulação. Na configuração 1 a equalização escurece os cantos (vinheta do dermatoscópio) e o ruído aparece em todo o fundo.
- **ISIC_7236365 (pelos densos): configuração 2.** A configuração 1 tem SSIM maior (0,513 × 0,464), porque a equalização
  reforça os pelos, estruturas fortes também presentes na original, mas o erro de intensidade é muito maior (15,5 × 17,6 dB)
  e os pelos ficam ainda mais escuros. A configuração 2 é o melhor compromisso.
- **ISIC_0014049 (baixo contraste): nenhuma é ideal.** A configuração 2 preserva a imagem (melhor SSIM), mas o gama quase
  não aumenta o contraste (desvio 7,4 → 7,6). A configuração 1 é a única que torna a lesão realmente visível, mas amplifica
  o ruído (SSIM 0,119). Aqui melhorar o contraste e reduzir o ruído entram em conflito.

**Onde as técnicas se comportaram mal:**

1. **Equalização logo após o ruído:** estica diferenças de 1–2 tons para dezenas de tons, inclusive as do ruído. É o pior
   estágio em todas as imagens (SSIM 0,022–0,227), e o Gaussiano aplicado depois não desfaz o estrago. Suavizar antes
   (configuração 2) manteve o SSIM entre 0,66 e 0,74 após a suavização: **a ordem importa**.
2. **Aguçamento amplifica o ruído residual:** o high-boost reduz o SSIM em todas as imagens (ex.: ISIC_0021531,
   configuração 2: 0,569 → 0,320), porque o ruído restante está justamente em `f − borrada` (realce excessivo).
3. **γ fixo em imagem escura:** na ISIC_0112420, o γ = 1,5 escurece ainda mais uma imagem já escura e a lesão quase se
   confunde com o fundo; nela a equalização revela muito mais estrutura. Uma técnica boa em uma imagem é ruim em outra:
   o γ deveria ser escolhido por imagem (γ < 1 para imagens escuras).
4. **Mediana contra ruído Gaussiano:** comparados isoladamente na mesma imagem degradada, o **Gaussiano 5×5 venceu a
   mediana 3×3 nas três imagens** (PSNR 31,7–35,3 × 30,9–32,3 dB; SSIM 0,80–0,83 × 0,66–0,74). Era o esperado: o ruído
   inserido é Gaussiano, e a mediana é indicada para ruído impulsivo. Portanto a configuração 2 vence **apesar** do
   filtro, graças à ordem; a combinação ideal seria o Gaussiano aplicado antes da operação pontual.

**Problemas encontrados durante o desenvolvimento:**

- A primeira versão da convolução usava padding de zeros, criando uma moldura escura no Gaussiano e bordas brancas
  falsas no aguçamento; foi trocada por padding `edge`.
- Conversões `astype(uint8)` sem arredondar truncavam os valores e escureciam a imagem em ~0,5 tom em média
  (ruído e Gaussiano); passou-se a usar `np.round` antes da conversão.
- A equalização sem descontar a CDF mínima transformava uma imagem de tom único em branco; foi corrigida.
- O SSIM inicial montava uma matriz de todas as janelas (> 1 GB de memória em 1024 px); foi reescrito com médias locais.

**Limitações:**

- PSNR e SSIM medem **fidelidade à original**. Operações pontuais mudam as intensidades de propósito, então sempre
  derrubam as métricas, mesmo quando a lesão fica mais visível; por isso a análise visual é indispensável.
- O SSIM usa janela uniforme 7×7 (o artigo original usa Gaussiana 11×11, σ = 1,5); os valores absolutos podem diferir
  de bibliotecas prontas, mas a comparação entre configurações é válida.
- As imagens foram reduzidas para 1024 px, o que as suaviza levemente antes de todo o processamento.

## 9. Conclusão

**Responsável:** todos

O melhor compromisso entre contraste, ruído e detalhes foi obtido pela **configuração 2** (mediana → gama →
high-boost) em duas das três imagens (ISIC_7236365 e ISIC_0021531), principalmente por remover o ruído **antes** da
operação pontual. As métricas não apontam um vencedor absoluto: a configuração 1 teve PSNR final maior na
ISIC_0014049 e SSIM final maior na ISIC_7236365. A equalização de histograma foi a técnica com maior ganho de contraste, mas, aplicada a uma imagem ruidosa,
amplificou o ruído de forma que as etapas seguintes não conseguiram corrigir. O experimento mostrou que a ordem das
etapas pesa tanto quanto a escolha das técnicas, que parâmetros fixos (como o γ) não servem para todas as imagens, e
que métricas com referência precisam ser lidas junto com a análise visual quando há transformações de intensidade.
Como continuação, sugere-se testar suavização → equalização → high-boost e escolher o γ automaticamente a partir da
média de intensidade de cada imagem.

## Referências

- Slides da disciplina de Processamento de Imagens (UNIVALI): Operações Pontuais e Filtros Espaciais; Métricas de Qualidade.
- ISIC Archive – International Skin Imaging Collaboration. https://www.isic-archive.com
- GONZALEZ, R. C.; WOODS, R. E. *Processamento Digital de Imagens*. 3. ed. São Paulo: Pearson, 2010.
- WANG, Z. et al. Image quality assessment: from error visibility to structural similarity. *IEEE Transactions on
  Image Processing*, v. 13, n. 4, p. 600–612, 2004.
