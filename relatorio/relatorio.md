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
Tipo de ruído, parâmetros (σ, semente) e como foi controlado.

### 5.2 Operação pontual — **Gustavo**
Equalização / correção gama: fórmula, justificativa e efeito nas 3 imagens.

### 5.3 Suavização — **Heloisa**
Convolução, filtro Gaussiano / mediana: kernel, tamanho, tratamento de borda.

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
