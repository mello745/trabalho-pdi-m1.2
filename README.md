# Projeto M1.2 – Operações Pontuais e Filtragem Espacial

**Universidade do Vale do Itajaí (UNIVALI)** · Ciência da Computação · Processamento de Imagens
**Professor:** Felipe Viel
**Equipe:** Gustavo Corrêa de Mello · Heloisa Cavalcante Born · João Paulo Jorge Aimi
**Entrega:** 28/09/2026 até 18:59 (sem atraso) — Slide + Relatório + Repositório/Código

Melhoria de imagens dermatoscópicas (ISIC – melanoma) com operações pontuais, suavização e
aguçamento **implementados do zero em Python/NumPy**, avaliada com PSNR e SSIM.

## Estrutura

```
trab-m1.2-pdi/
├── notebooks/          # notebook final (entrega principal)
├── src/pdi/            # funções de cada membro
│   ├── pipeline.py     # aplica as etapas em sequência (usado no notebook)
│   ├── gustavo/        # io_utils.py, operacoes_pontuais.py
│   ├── heloisa/        # ruido.py, convolucao.py, suavizacao.py
│   └── joao/           # agucamento.py, metricas.py
├── data/originais/     # as 3 imagens ISIC escolhidas (+ README com IDs e justificativa)
├── relatorio/          # relatório final
├── apresentacao/       # slides (10–15 min)
└── docs/               # checklist do enunciado e divisão de tarefas
```

## Como rodar

```bash
pip install -r requirements.txt
jupyter notebook notebooks/
```