# Roteiro da apresentação — Projeto M1

> Esqueleto criado para a branch `feat/born`. Slides 4–6 correspondem à parte da Heloisa e já estão preenchidos. Slides 7–10 devem ser finalizados depois da integração da pipeline, métricas e resultados.

## 1. Capa
- Projeto M1 – Operações Pontuais e Filtragem Espacial
- Melhoria de imagens dermatoscópicas do ISIC
- Gustavo Corrêa de Mello · Heloisa Born · João Paulo Jorge

## 2. Problema e conjunto de imagens
- ISIC_0014049 — contraste muito baixo
- ISIC_7236365 — pelos densos
- ISIC_0021531 — bordas difusas
- Objetivo: equilibrar contraste, redução de ruído e preservação/realce de detalhes.

## 3. Pipeline do trabalho
- Imagem original → ruído → operação pontual → suavização → aguçamento → métricas.
- Configuração 1 e configuração 2 serão comparadas visual e quantitativamente.

## 4. Ruído Gaussiano controlado — Heloisa
- `g(x,y) = f(x,y) + n(x,y)`
- `n(x,y) ~ N(0, 15²)`
- Média 0, sigma 15, semente 42.
- `clip` para `[0,255]` e retorno `uint8`.
- Reprodutibilidade: mesmos parâmetros e semente.

## 5. Convolução 2D manual — Heloisa
- Kernel Gaussiano 5×5, sigma 1.0, soma igual a 1.
- Validação de imagem 2D e kernel ímpar.
- Conversão para `float64`.
- Rotação do kernel em 180°.
- Zero padding.
- Deslizamento da janela, multiplicação elemento a elemento e soma.
- A mesma `conv2d_float` é utilizada pelo aguçamento do João.

## 6. Suavização: Gaussiano × Mediana — Heloisa
### Gaussiano
- 5×5, sigma 1.0.
- Kernel normalizado.
- Aplicado pela convolução manual.
- Adequado ao ruído Gaussiano inserido no experimento.

### Mediana
- Janela 3×3.
- Ordena a vizinhança e escolhe o valor central.
- Padding `edge`.
- Alternativa para comparar preservação de estruturas locais.

## 7. Aguçamento e métricas — João
- PREENCHER: técnica final, parâmetros, trecho importante do código.
- PREENCHER: PSNR e SSIM, fórmulas e interpretação.

## 8. Configuração 1 × Configuração 2
- VALIDAR com a pipeline final do grupo.
- Explicar a diferença como decisão técnica.

## 9. Resultados — Heloisa
- Para cada imagem: original × degradada × configuração 1 × configuração 2.
- Inserir tabela PSNR/SSIM gerada pelo notebook.

## 10. Análise, discussão e conclusão — Heloisa + João
- Melhor configuração para cada imagem.
- Trade-offs: contraste × ruído; suavização × detalhes; aguçamento × realce excessivo.
- Limitações e comportamentos inadequados.
- Conclusão: melhor compromisso entre contraste, ruído e detalhes.

## Apêndice — validações funcionais
- Ruído: erro absoluto médio observado ≈ 11,97 para sigma 15.
- Gaussiano: MAE 3,83 / 4,80 / 3,79.
- Mediana: MAE 4,97 / 5,57 / 4,93.
- Sobel: teste sintético com transição vertical produziu a linha de borda esperada.
- Observação: essas checagens não substituem PSNR/SSIM na comparação oficial.
