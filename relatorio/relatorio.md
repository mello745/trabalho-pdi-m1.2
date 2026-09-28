# Relatório – Projeto M1.2: Operações Pontuais e Filtragem Espacial

## 1. Identificação

1. Universidade: Universidade do Vale do Itajaí (UNIVALI)
2. Curso: Ciência da Computação
3. Disciplina: Processamento de Imagens
4. Professor: Felipe Viel
5. Integrantes: Gustavo Corrêa de Mello, Heloisa Cavalcante Born e João Paulo Jorge Aimi
6. Data: 28/09/2026
7. Repositório: https://github.com/mello745/trabalho-pdi-m1.2

## 2. Enunciado do projeto

Desenvolver, em Python e sem funções prontas de filtragem ou de operações pontuais, uma pipeline de melhoria de
imagens médicas do conjunto ISIC (International Skin Imaging Collaboration). O grupo deve selecionar três melanomas
de uma mesma região anatômica, caracterizar seus problemas de qualidade, inserir ruído controlado e aplicar uma
operação pontual, uma suavização e um aguçamento. Pelo menos duas configurações da pipeline devem ser comparadas
visual e quantitativamente com duas métricas vistas em aula.

## 3. Contexto da aplicação

Imagens dermatoscópicas são usadas como entrada para etapas posteriores de análise computacional, como segmentação
e classificação de lesões de pele. Variações de contraste, ruído e definição das estruturas prejudicam tanto a
interpretação humana quanto esses métodos. O objetivo é melhorar a imagem sem introduzir artefatos. Os desafios
tratados são:

1. Variação de contraste: lesão e pele com tons muito próximos.
2. Ruído: interferências que mascaram informações.
3. Perda de detalhes: a suavização pode eliminar pequenas estruturas junto com o ruído.
4. Realce excessivo: o aguçamento pode intensificar ruído e artefatos.
5. Diferenças entre imagens: uma técnica boa em uma imagem pode ser inadequada em outra.

## 4. Seleção e caracterização das imagens

Foram consideradas as 1.089 imagens dermatoscópicas de melanoma do tronco posterior do ISIC (a região com mais
imagens). Para cada uma foram medidos contraste, nitidez e brilho, e foram escolhidas imagens nos extremos de
critérios diferentes:

1. ISIC_0014049 (melanoma invasivo, CC-0): contraste muito baixo. Média 128,4, desvio padrão 7,4, quase todos os
   pixels entre os tons 102 e 137; pele e lesão têm tons quase iguais.
2. ISIC_7236365 (melanoma in situ, CC-0): pelos densos cruzando a lesão. Contraste já alto (desvio 41,6), mas os
   pelos podem ser amplificados pelo realce.
3. ISIC_0021531 (melanoma invasivo, CC-0): bordas difusas, imagem levemente desfocada. Contraste intermediário
   (desvio 23,5).
4. ISIC_0112420 (melanoma in situ, CC-BY, Department of Dermatology, University of Athens): muito escura, usada
   apenas no teste com imagem nova.

As imagens são convertidas para tons de cinza pela fórmula `I = 0,299R + 0,587G + 0,114B`, implementada
manualmente (os pesos seguem a sensibilidade do olho humano, maior ao verde), e reduzidas para 1024 px de largura,
mantendo a proporção, porque a convolução manual seria lenta em 4288 px.

## 5. Desenvolvimento

O código está organizado por integrante em `src/pdi/` e é chamado pelos notebooks. A pipeline recebe uma lista de
etapas `(nome, função)`, aplica uma após a outra e guarda todos os estágios intermediários, para que cada um possa
ser exibido e medido:

```python
def executar(img, etapas):
    resultados = [("original", img)]
    atual = img
    for nome, funcao in etapas:
        atual = funcao(atual)
        resultados.append((nome, atual))
    return resultados
```

### 5.1 Inserção de ruído (Heloisa)

Foi adicionado ruído gaussiano, `I_degradada = I_original + N(0, σ²)`, com σ = 15, média zero e semente 42. A média
zero evita clarear ou escurecer a imagem, e a semente fixa permite reproduzir o mesmo ruído. Após a soma, os valores
são limitados a [0, 255] e arredondados. Os mesmos parâmetros são usados em todas as imagens e nas duas pipelines.

```python
gerador = np.random.default_rng(semente)
ruido = gerador.normal(loc=media, scale=sigma, size=imagem.shape)
imagem_ruidosa = np.clip(imagem.astype(np.float64) + ruido, 0, 255)
return np.round(imagem_ruidosa).astype(np.uint8)
```

### 5.2 Operação pontual (Gustavo)

Operações pontuais transformam cada pixel usando apenas o seu próprio valor, `s = T(r)`. Por isso são implementadas
como uma tabela de conversão (LUT) de 256 posições: monta-se a tabela "tom antigo → tom novo" e cada pixel é trocado
pelo valor da tabela.

1. Histograma: vetor de 256 contadores, somando 1 na posição do valor de cada pixel (pseudocódigo da aula).
2. Equalização de histograma, usada nas duas pipelines: redistribui os tons pela faixa 0–255 usando a fração
   acumulada de pixels (CDF), descontando a do tom mais escuro para que ele vire 0:
   `s = round(255 · (CDF(r) − CDF_min) / (1 − CDF_min))`. Uma imagem de tom único é devolvida sem alteração. O
   resultado foi idêntico ao `cv2.equalizeHist` nas quatro imagens (OpenCV usado apenas para conferência).
3. Correção gama, `s = 255 · (r/255)^γ`: também foi implementada, mas as duas pipelines usam a equalização, para que
   a única diferença entre elas seja a ordem das etapas.

```python
minima = acumulada[h > 0][0]
if minima == 1:
    return img.copy()
tabela = np.round(255 * (acumulada - minima) / (1 - minima))
tabela = np.clip(tabela, 0, 255).astype(np.uint8)
return aplicar_lut(img, tabela)
```

Aplicada nas originais, a equalização elevou o desvio padrão de 7,4 para 75,0 (ISIC_0014049), de 41,6 para 73,8
(ISIC_7236365) e de 23,5 para 74,4 (ISIC_0021531). O ganho é grande, mas agressivo: o histograma fica "em pente",
porque a equalização não cria tons novos, só redistribui os existentes.

### 5.3 Suavização (Heloisa)

Foi implementada uma convolução 2D própria: para cada pixel, a vizinhança do tamanho do kernel é multiplicada pelo
kernel rotacionado em 180° e os produtos são somados. As bordas usam padding `edge` (repetem o pixel mais próximo),
e o resultado é calculado em `float64`, pois o Laplaciano e o Sobel geram valores negativos.

1. Filtro Gaussiano (usado nas duas pipelines): kernel 5×5 com σ = 1, calculado manualmente e normalizado para somar 1.
   Faz uma média ponderada que dá mais peso aos pixels próximos do centro.
2. Filtro da mediana 3×3: também implementado (ordena os 9 valores da vizinhança e usa o central), mas não entrou nas
   pipelines finais. Comparado isoladamente na mesma imagem degradada, o Gaussiano teve PSNR de 31,7 a 35,3 dB contra
   30,9 a 32,3 dB da mediana, o esperado para ruído gaussiano (a mediana é indicada para ruído impulsivo).

```python
kernel = gauss_create(sigma=sigma, size=tamanho)
resultado = conv2d_float(imagem, kernel)
```

### 5.4 Aguçamento (João Paulo)

1. Sobel: magnitude do gradiente `√(Gx² + Gy²)`. Gera apenas as bordas, então é usado só para visualizar a informação
   de alta frequência, não como resultado final.
2. Laplaciano: `saída = f + c·∇²f`, com kernel de centro positivo.
3. High-boost (usado nas duas pipelines): `saída = f + k·(f − borrada)`, com borramento Gaussiano 3×3 e k = 1,5. Soma o
   detalhe à imagem inteira, atendendo à exigência de que o resultado não seja só bordas. A imagem borrada é mantida
   em `float64` para não perder diferenças pequenas.

```python
borrada = conv2d_float(img, gauss_create(sigma=sigma, size=tamanho))
saida = img.astype(np.float64) + k * (img.astype(np.float64) - borrada)
return np.clip(np.round(saida), 0, 255).astype(np.uint8)
```

### 5.5 Pipelines comparadas

Pipeline 1, seguindo a ordem do enunciado:

1. Ruído gaussiano (σ = 15, semente 42)
2. Equalização de histograma
3. Filtro Gaussiano 5×5
4. High-boost (k = 1,5)

Pipeline 2, a mesma sequência na ordem inversa depois do ruído:

1. Ruído gaussiano (σ = 15, semente 42)
2. High-boost (k = 1,5)
3. Filtro Gaussiano 5×5
4. Equalização de histograma

As técnicas e os parâmetros são idênticos; só a ordem muda. Assim qualquer diferença no resultado pode ser atribuída
à ordem. As duas partem da mesma imagem degradada (mesma semente).

## 6. Métricas (João Paulo)

Foram escolhidas duas métricas vistas em aula, com a imagem original sem ruído como referência:

1. PSNR: `10·log10(255² / MSE)`, em dB, quanto maior melhor. Mede o erro pixel a pixel e é a métrica clássica para
   avaliar remoção de ruído.
2. SSIM: compara médias, variâncias e covariâncias locais, de −1 a 1. Mede a preservação da estrutura, sendo sensível
   à perda de detalhe e a artefatos do aguçamento.

Uma mede erro de intensidade e a outra estrutura, por isso se complementam. O SSIM foi implementado com janelas
uniformes 7×7, calculando só médias locais (`var = E[x²] − E[x]²`, `cov = E[xy] − E[x]E[y]`).

## 7. Resultados

Valores finais (PSNR em dB e SSIM), com a imagem degradada como ponto de partida:

1. ISIC_0014049: degradada 24,60 e 0,240; pipeline 1 17,51 e 0,119; pipeline 2 11,22 e 0,038.
2. ISIC_7236365: degradada 24,61 e 0,401; pipeline 1 15,52 e 0,513; pipeline 2 14,85 e 0,473.
3. ISIC_0021531: degradada 24,60 e 0,232; pipeline 1 14,10 e 0,168; pipeline 2 11,98 e 0,113.
4. ISIC_0112420 (teste): degradada 24,94 e 0,397; pipeline 1 10,18 e 0,375; pipeline 2 9,37 e 0,339.

Estágios intermediários mais relevantes:

1. Pipeline 1, logo após a equalização: SSIM de 0,022, 0,227 e 0,035.
2. Pipeline 2, logo após o high-boost: SSIM de 0,063, 0,177 e 0,059.
3. Pipeline 2, após o Gaussiano: PSNR de 32,55, 31,25 e 32,64 dB e SSIM de 0,679, 0,767 e 0,677, o melhor estágio
   de todo o trabalho.

Visualmente, as duas pipelines deixam a lesão muito mais visível que a original, mas a pipeline 2 fica mais
saturada e mais granulada.

## 8. Análise e discussão (Heloisa e João Paulo)

A pipeline 1 venceu nas três imagens e nas duas métricas, e também no teste com a imagem escura. Como as técnicas
são as mesmas, a diferença vem só da ordem:

1. Equalização no início (pipeline 1): estica o ruído junto com o contraste e o SSIM despenca, mas o Gaussiano
   seguinte recupera parte da estrutura, e o high-boost final atua sobre uma imagem já suavizada.
2. Aguçamento no início (pipeline 2): o high-boost realça o ruído junto com os detalhes, e o Gaussiano logo depois
   quase desfaz esse aguçamento. O trabalho do high-boost é desperdiçado.
3. Equalização no final (pipeline 2): estica o ruído que sobrou e não há nenhuma etapa depois para corrigir. É por
   isso que a pipeline 2 perde, mesmo tendo o melhor estágio intermediário.
4. Técnica boa em uma imagem e ruim em outra: na ISIC_0014049 a equalização é a única forma de tornar a lesão
   visível, mas também é onde mais amplifica o ruído, porque o contraste original é mínimo.

Problemas encontrados durante o desenvolvimento e como foram resolvidos:

1. Imagens em formatos diferentes (paleta, transparência, CMYK) quebravam o carregamento: padronização para RGB
   antes de redimensionar e converter para cinza.
2. Processamento lento em imagens de até 4288 px: redimensionamento para 1024 px.
3. Moldura escura no Gaussiano e bordas brancas falsas no aguçamento, causadas por padding de zeros na convolução:
   troca para padding `edge`.
4. Imagens escurecendo meio tom (ruído com média 127,4 em vez de 128), porque `astype(uint8)` corta as casas
   decimais: uso de `np.round` antes da conversão.
5. SSIM com valores sem sentido, porque `img * img` em `uint8` estoura: conversão para `float64` antes.
6. SSIM usando mais de 1 GB de memória: reescrito com médias locais (1.384 MB para 61 MB, mesmo resultado).
7. Equalização deixava uma imagem de tom único toda branca: inclusão da `CDF_min`.

Limitações:

1. PSNR e SSIM medem fidelidade à original. A equalização muda as intensidades de propósito e sempre derruba as
   métricas, mesmo quando a lesão fica mais visível; por isso a análise visual é indispensável.
2. O SSIM usa janela uniforme 7×7 (o artigo original usa Gaussiana 11×11); os valores absolutos podem diferir de
   bibliotecas prontas, mas a comparação entre as pipelines é válida.
3. O redimensionamento para 1024 px suaviza levemente todas as imagens antes do processamento.

## 9. Conclusão

A pipeline 1, na ordem proposta pelo enunciado, teve o melhor resultado em todas as imagens. Como as duas pipelines
usam exatamente as mesmas técnicas e parâmetros, o experimento mostra que a ordem das etapas é uma decisão tão
importante quanto a escolha das técnicas: a equalização precisa de uma suavização depois dela e não deve ser a
última etapa, e aguçar antes de suavizar é trabalho desperdiçado. Como continuação, sugere-se testar suavização,
equalização e high-boost nessa ordem, removendo o ruído antes de realçar o contraste.

## Referências

1. Slides da disciplina de Processamento de Imagens (UNIVALI): Operações Pontuais e Filtros Espaciais; Métricas de
   Qualidade.
2. ISIC Archive – International Skin Imaging Collaboration. https://www.isic-archive.com
3. GONZALEZ, R. C.; WOODS, R. E. Processamento Digital de Imagens. 3. ed. São Paulo: Pearson, 2010.
4. WANG, Z. et al. Image quality assessment: from error visibility to structural similarity. IEEE Transactions on
   Image Processing, v. 13, n. 4, p. 600–612, 2004.
