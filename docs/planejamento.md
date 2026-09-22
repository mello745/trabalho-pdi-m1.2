# Divisão de tarefas e cronograma

Cada membro é **dono** de um bloco (implementa + escreve a seção do relatório + faz os slides dele)
e **revisor** de outro bloco (lê o código, roda no notebook e precisa conseguir explicá-lo).
Isso atende ao item 8: todos devem dominar todas as partes.

Bibliotecas **só** para: ler/salvar imagem, operações de array do NumPy e plotar gráficos.
É **proibido** usar `cv2.GaussianBlur`, `cv2.medianBlur`, `cv2.equalizeHist`, `cv2.filter2D`,
`cv2.Laplacian`, `cv2.Sobel`, `scipy.ndimage.*`, `skimage.filters/exposure/metrics` etc.
Todo mundo precisa saber explicar **todo** o código.

| Membro | Dono de | Revisa | Arquivos |
|---|---|---|---|
| **Gustavo Mello** | Seleção das imagens ISIC, operações pontuais, montagem do notebook final, repositório | Métricas (João Paulo) | `gustavo/`, `data/`, `notebooks/` |
| **Heloisa Born** | Ruído controlado, convolução, suavização (Gaussiano + mediana) | Operações pontuais (Gustavo) | `heloisa/` |
| **João Paulo Jorge** | Aguçamento (Laplaciano / Sobel / High-Boost), métricas (PSNR + SSIM) | Suavização (Heloisa) | `joao/` |

### Tarefas compartilhadas
| Entregável | Responsável principal | Apoio |
|---|---|---|
| Caracterização inicial das imagens (histogramas + problemas) | Gustavo | Heloisa |
| Rodar as duas configurações no notebook + tabela de métricas | João Paulo | todos |
| Relatório — introdução, enunciado, contexto | Gustavo | — |
| Relatório — desenvolvimento (cada um escreve sua parte) | todos | — |
| Relatório — resultados e discussão | Heloisa | João Paulo |
| Slides (template + montagem final) | Heloisa | todos |
| Ensaio da apresentação cronometrado (10–15 min) | todos | — |

## Cronograma (entrega 28/09/2026 às 18:59)

| Data | Meta |
|---|---|
| **Ter 22/09** | Estrutura pronta. Escolher categoria ISIC + região anatômica e as 3 imagens (Gustavo). Fechar decisões em `DECISOES_TECNICAS.md` |
| **Qua 23/09** | `convolucao.py`, `ruido.py`, `operacoes_pontuais.py`, `metricas.py` implementados e testados no notebook |
| **Qui 24/09** | `suavizacao.py`, `agucamento.py` prontos; notebook rodando do início ao fim |
| **Sex 25/09** | Rodar as configurações 1 e 2, gerar figuras e tabela de métricas. Revisão cruzada do código |
| **Sáb 26/09** | Relatório (rascunho completo) + slides |
| **Dom 27/09** | Revisão final, repositório público, ensaio da apresentação, teste com imagem aleatória |
| **Seg 28/09** | Postar Slide + Relatório + link do repositório **antes das 18:59** |

## Combinados
- Não subir código com funções prontas de filtragem (ver README).
- Parâmetros (σ do ruído, tamanho de kernel, γ, k...) ficam em variáveis no topo da célula do notebook, com nome claro.
- Figuras e métricas saem sempre do notebook, nunca editadas à mão.
- Antes de marcar algo como pronto no checklist, o revisor roda e aprova.
