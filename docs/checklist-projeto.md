# Checklist do enunciado (Trabalho M1)

Tudo que o PDF exige, item a item. Marcar `[x]` quando pronto e revisado por outro membro.

## Regras gerais
- [ ] Grupo de 2 a 3 pessoas (Gustavo, Heloisa, João Paulo)
- [ ] Entrega até **28/09/2026 18:59** — não aceita atraso
- [ ] Implementação em **Python**, sem funções prontas de filtragem / operações pontuais
- [ ] Sistema entregue **funcionando** (notebook roda do início ao fim em máquina limpa com `requirements.txt`)
- [ ] Deve processar **qualquer imagem** na hora da apresentação (trocar o caminho da imagem numa célula do notebook e rodar de novo)
- [ ] Repositório **público** e mantido aberto após a entrega (link no relatório)
- [ ] Postar no material da disciplina: **Slide + Relatório + Repositório/Código**
- [ ] Apresentação de **10 a 15 min**; todos apresentam e todos respondem perguntas

## Conteúdo obrigatório da solução (relatório e slides)
- [ ] Identificação dos autores e do trabalho
- [ ] Enunciado do projeto
- [ ] Explicação e contexto da aplicação (imagens médicas → etapa posterior de análise computacional)
- [ ] Desenvolvimento
- [ ] Códigos importantes da implementação
- [ ] Resultados obtidos
- [ ] Análise e discussão dos resultados (inclusive problemas)

## Fluxo do processamento
1. [ ] **Seleção das imagens** — ISIC, **3 melanomas da mesma região anatômica**, sequência
       diferente dos outros grupos; imagens com diferenças de contraste / ruído / definição;
       **justificar** a escolha (registrar IDs em `data/originais/README.md`)
2. [ ] **Caracterização inicial** — mostrar originais + histogramas e apontar os problemas de qualidade de cada uma
3. [ ] **Inserção de ruído** — ruído artificial controlado em cada original; **registrar parâmetros**
       (tipo, σ / densidade, semente) e manter igual para todas as comparações
4. [ ] **Operação pontual** — equalização de histograma, correção gama ou outra justificada;
       explicar por que é adequada e **comparar o efeito nas 3 imagens**
5. [ ] **Suavização** — Gaussiano, mediana ou outra justificada
6. [ ] **Aguçamento** — Laplaciano, Sobel, High-Boost ou outra; o resultado final **não pode ser só bordas**:
       combinar com a imagem (ex.: `f - c·∇²f`, high-boost)
7. [ ] **Segunda configuração** — mudar uma técnica, parâmetro ou ordem e repetir (configuração 1 × configuração 2, feito direto no notebook)
8. [ ] **Métricas** — escolher **2** das vistas em aula (MSE, RMSE, PSNR, SSIM, GMSD), **justificar**, e comparar
       original × degradada × processada 1 × processada 2
9. [ ] **Discussão** — melhor configuração **para cada imagem** + casos em que uma técnica se comportou mal
       (perda de detalhe, realce excessivo, amplificação de ruído, saturação)

> A ordem pode mudar se houver justificativa técnica — registrar em `DECISOES_TECNICAS.md`.

## Desafios que a discussão deve abordar
- [ ] Variação de contraste
- [ ] Presença de ruído
- [ ] Perda de detalhes pela suavização
- [ ] Realce excessivo pelo aguçamento
- [ ] Técnica boa em uma imagem e ruim em outra

## Critérios de avaliação (o que o professor vai olhar)
- Qualidade, organização e clareza do código
- Adequação da escolha das imagens e justificativa técnica
- Qualidade da apresentação e do material
- Domínio técnico ao explicar as operações e ao responder perguntas
- Interpretação das diferenças entre as configurações
- Uso adequado das métricas e interpretação
- Linearidade e clareza da explicação
- Exposição das decisões técnicas, parâmetros e limitações
- Qualidade do relatório e da discussão
