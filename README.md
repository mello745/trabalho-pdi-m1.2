# Projeto M1.2 - Operações Pontuais e Filtragem Espacial

**Universidade do Vale do Itajaí (UNIVALI)**
Curso: Ciência da Computação
Disciplina: Processamento de Imagens
Professor: Felipe Viel

---

## Integrantes

- Gustavo Corrêa de Mello
- Heloisa Cavalcante Born
- João Paulo Jorge Aimi

---

## Descrição

Pipeline de melhoria de imagens dermatoscópicas de melanoma do conjunto ISIC,
usando operações pontuais e filtragem espacial. O projeto insere ruído
controlado, aplica transformação de intensidade, suavização e aguçamento, e
compara duas configurações da pipeline com as métricas PSNR e SSIM.

Todos os algoritmos de filtragem, de operações pontuais e de métricas foram
implementados do zero, conforme exigido pelo enunciado.

---

## Estrutura do projeto

```
trabalho-pdi-m1.2/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/pdi/                      # Implementações (lógica do projeto)
│   ├── __init__.py
│   ├── pipeline.py               # Executa as etapas em sequência
│   ├── gustavo/
│   │   ├── io_utils.py           # Carregamento, conversão para cinza, exibição
│   │   └── operacoes_pontuais.py # Histograma, equalização, correção gama
│   ├── heloisa/
│   │   ├── ruido.py              # Ruído gaussiano controlado
│   │   ├── convolucao.py         # Convolução manual e kernel gaussiano
│   │   └── suavizacao.py         # Filtro gaussiano e filtro da mediana
│   └── joao/
│       ├── agucamento.py         # Laplaciano, Sobel e high-boost
│       └── metricas.py           # MSE, PSNR e SSIM
│
├── notebooks/
│   ├── trabalho_m1.ipynb         # Notebook de entrega (comparativo)
│   ├── config1_pipeline.ipynb    # Configuração 1 completa
│   └── config2_pipeline.ipynb    # Configuração 2 completa
│
├── data/originais/               # Imagens ISIC escolhidas + justificativa
│
├── resultados/                   # Imagens finais geradas pelos notebooks
│
├── relatorio/
│   └── relatorio.md
│
└── apresentacao/                 # Slides e roteiro
```

O código fica em `src/` e os notebooks apenas importam, executam e exibem. Essa
separação evita conflitos de merge no Git, que são frequentes quando várias
pessoas editam o mesmo arquivo `.ipynb`.

---

## Pipelines comparadas

| Etapa | Configuração 1 | Configuração 2 |
|-------|----------------|----------------|
| 1 | Ruído gaussiano (σ = 15) | Ruído gaussiano (σ = 15) |
| 2 | Equalização de histograma | Filtro da mediana 3×3 |
| 3 | Filtro gaussiano 5×5 | Correção gama (γ = 1,5) |
| 4 | High-boost (k = 1,5) | High-boost (k = 1,5) |

A configuração 1 realça o contraste antes de remover o ruído; a configuração 2
remove o ruído primeiro. A análise completa está em `notebooks/trabalho_m1.ipynb`
e em `relatorio/relatorio.md`.

---

## Como executar

**1. Clonar o repositório**

```bash
git clone https://github.com/mello745/trabalho-pdi-m1.2.git
cd trabalho-pdi-m1.2
```

**2. Criar e ativar o ambiente virtual**

Linux / macOS:
```bash
python -m venv venv
source venv/bin/activate
```

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Instalar as dependências**

```bash
pip install -r requirements.txt
```

**4. Executar o notebook**

```bash
jupyter notebook notebooks/trabalho_m1.ipynb
```

As imagens já estão no repositório, em `data/originais/`. Para testar com outra
imagem, altere `IMAGEM_TESTE` na última seção do notebook.

---

## Mapa dos itens do enunciado

| Item | Descrição | Arquivo |
|------|-----------|---------|
| 1 | Seleção das imagens e justificativa | `data/originais/README.md` |
| 2 | Caracterização inicial | `notebooks/trabalho_m1.ipynb` |
| 3 | Inserção de ruído controlado | `src/pdi/heloisa/ruido.py` |
| 4 | Operação pontual (equalização e gama) | `src/pdi/gustavo/operacoes_pontuais.py` |
| 5 | Suavização (gaussiano e mediana) | `src/pdi/heloisa/suavizacao.py` |
| 6 | Aguçamento (high-boost) | `src/pdi/joao/agucamento.py` |
| 7 | Segunda configuração da pipeline | `notebooks/config2_pipeline.ipynb` |
| 8 | Métricas PSNR e SSIM | `src/pdi/joao/metricas.py` |
| 9 | Discussão dos resultados | `relatorio/relatorio.md` |

---

## Restrições do trabalho

Conforme o item 4 das instruções do enunciado:

> A implementação deverá ser desenvolvida em Python. O uso de funções de
> filtragem ou operações pontuais prontas de bibliotecas não será aceito.

Na prática, para este projeto:

**Permitido**
- NumPy para manipulação de matrizes
- Matplotlib para exibição
- Pillow apenas para leitura, escrita e redimensionamento de imagens

**Proibido**
- `cv2.filter2D`, `cv2.GaussianBlur`, `cv2.medianBlur`
- `cv2.equalizeHist`, `cv2.Sobel`, `cv2.Laplacian`
- `scipy.ndimage.convolve` e equivalentes
- `skimage.metrics` (PSNR e SSIM prontos)

Todos os integrantes devem saber explicar qualquer parte da implementação. O
professor pode escolher um representante do grupo para apresentar.

---

## Dataset

International Skin Imaging Collaboration (ISIC): https://www.isic-archive.com

Melanomas dermatoscópicos do tronco posterior: `ISIC_0014049`, `ISIC_7236365` e
`ISIC_0021531` (CC-0), e `ISIC_0112420` (CC-BY, usada no teste com imagem nova).
