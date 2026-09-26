# Relatório – Projeto M1: Operações Pontuais e Filtragem Espacial

> Rascunho do relatório. Cada seção indica o que precisa ser escrito e quem é o responsável.
> Figuras e tabelas saem do notebook (`notebooks/trabalho_m1.ipynb`).
> Versão final: exportar para PDF.

## 1. Identificação
**Responsável:** Gustavo
Universidade, curso, disciplina, professor, nomes dos integrantes, título do trabalho, data e link do repositório.

## 2. Enunciado do projeto
**Responsável:** Gustavo
Resumo do que foi pedido: pipeline de melhoria de imagens do ISIC com operação pontual, suavização,
aguçamento, duas configurações e avaliação por métricas.

## 3. Contexto da aplicação
**Responsável:** Gustavo
Por que melhorar imagens dermatoscópicas antes de uma análise computacional; desafios
(contraste, ruído, perda de detalhes, realce excessivo, diferenças entre imagens).

## 4. Seleção e caracterização das imagens
**Responsável:** Gustavo
IDs ISIC, região anatômica, justificativa da escolha, originais + histogramas e os problemas de cada uma.

## 5. Desenvolvimento
Explicar cada técnica (fórmula, parâmetros, por que foi escolhida) com o trecho de código mais importante.

### 5.1 Inserção de ruído — **Heloisa**

Para degradar as imagens de forma controlada, foi implementada a adição de **ruído Gaussiano**. Para cada pixel da imagem é gerado um valor aleatório segundo uma distribuição normal, que é somado à intensidade original:

`I_degradada = I_original + N(0, σ²)`

Nos experimentos foi utilizado `σ = 15`, com média igual a zero e `semente = 42`. A média zero evita introduzir intencionalmente um clareamento ou escurecimento global na imagem, enquanto a semente fixa permite reproduzir o mesmo ruído em novas execuções.

Após a soma, os valores são limitados ao intervalo `[0, 255]`, evitando intensidades inválidas para imagens de 8 bits. A implementação foi realizada com NumPy, sem utilização de uma função pronta de adição de ruído.

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
```

### 5.2 Operação pontual — **Gustavo**
Equalização / correção gama: fórmula, justificativa e efeito nas 3 imagens.

### 5.3 Suavização — **Heloisa**

A etapa de suavização tem como objetivo reduzir o ruído artificial inserido anteriormente, buscando preservar o máximo possível dos detalhes relevantes da imagem. Foram implementados dois métodos: **filtro Gaussiano** e **filtro de mediana**.

#### Convolução

Para permitir a aplicação dos filtros espaciais, foi implementada uma função própria de convolução 2D. Para cada posição da imagem, uma vizinhança com o mesmo tamanho do kernel é selecionada. O kernel é rotacionado em 180 graus, os elementos correspondentes são multiplicados e os produtos são somados para gerar o novo valor do pixel.

Foi utilizado padding com zeros na convolução para preservar as dimensões da imagem de saída. O resultado é calculado em `float64`, pois alguns kernels utilizados posteriormente, como Laplaciano e Sobel, podem gerar valores negativos.

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
Laplaciano / Sobel / High-Boost e como a informação de borda foi combinada com a imagem.

### 5.5 Configurações testadas — **todos**
O que muda entre a configuração 1 e a 2 (técnica, parâmetro ou ordem) e por quê.

## 6. Métricas
**Responsável:** João Paulo
Métricas escolhidas (ex.: PSNR e SSIM), fórmulas e justificativa da escolha.

## 7. Resultados
**Responsável:** Heloisa
Figuras original × degradada × config 1 × config 2 e tabela de métricas para cada imagem.

## 8. Análise e discussão
**Responsável:** Heloisa + João Paulo
Melhor configuração para cada imagem, casos em que alguma técnica se comportou mal,
problemas encontrados e limitações das métricas.

## 9. Conclusão
**Responsável:** todos
Principais aprendizados e qual combinação teve o melhor compromisso entre contraste, ruído e detalhes.

## Referências
Slides da disciplina, ISIC Archive, Gonzalez & Woods, Wang et al. (2004) – SSIM.
