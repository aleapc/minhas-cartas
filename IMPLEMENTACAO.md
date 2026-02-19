# Relatório de Implementação - Site Minhas Cartas

**Projeto:** Site Silvano Corrêa - Minhas Cartas
**Data:** 18 de Fevereiro de 2026
**Repositório:** https://github.com/aleapc/minhas-cartas
**Site:** https://aleapc.github.io/minhas-cartas/

---

## 1. Visão Geral

Este relatório documenta a implementação completa do sistema de extração, indexação e navegação das cartas publicadas por Silvano Corrêa entre 1958 e 2025, compiladas em dois volumes.

### Objetivos Alcançados

- Extração automática de 1.408 imagens de cartas dos PDFs
- Processamento OCR para texto pesquisável em português
- Classificação automática por assuntos
- Interface web com filtros, busca e navegação temporal
- Integração de imagens de referência (autor, capas, carta JFK)

---

## 2. Configuração do Ambiente

### 2.1 Dependências Instaladas

| Ferramenta | Versão | Finalidade |
|------------|--------|------------|
| Python | 3.13 | Linguagem dos scripts |
| PyMuPDF (fitz) | - | Extração de imagens dos PDFs |
| Tesseract OCR | 5.5.0 | Reconhecimento óptico de caracteres |
| pytesseract | 0.3.13 | Interface Python para Tesseract |
| Pillow | 12.1.0 | Manipulação de imagens |

### 2.2 Configuração do Tesseract

- **Instalação:** Via instalador oficial (tesseract-ocr-w64-setup-5.5.0.20241111.exe)
- **Caminho:** `C:\Program Files\Tesseract-OCR\tesseract.exe`
- **Idiomas:** Português (por), Inglês (eng), OSD

---

## 3. Extração das Cartas

### 3.1 Script: `scripts/extrair_cartas.py`

**Funcionalidades:**
- Leitura dos PDFs usando PyMuPDF
- Filtro de imagens válidas (mínimo 200x200 pixels)
- Conversão para JPEG com qualidade 90%
- Nomenclatura padronizada: `vol{N}_p{XXX}_img{Y}.jpg`

**Resultados da Extração:**

| Volume | Páginas | Imagens Encontradas | Imagens Válidas |
|--------|---------|---------------------|-----------------|
| Volume 1 | 220 | 456 | 433 |
| Volume 2 | 364 | 1.037 | 975 |
| **Total** | **584** | **1.493** | **1.408** |

### 3.2 Estrutura de Arquivos Gerados

```
assets/cartas/
├── vol1/
│   ├── vol1_p001_img1.jpg
│   ├── vol1_p004_img1.jpg
│   └── ... (433 arquivos)
├── vol2/
│   ├── vol2_p001_img1.jpg
│   ├── vol2_p002_img1.jpg
│   └── ... (975 arquivos)
└── manifest.json
```

---

## 4. Processamento OCR

### 4.1 Script: `scripts/processar_ocr.py`

**Funcionalidades:**
- Processamento com Tesseract em português (PSM 6)
- Extração de ano via regex (padrões de data)
- Extração de data de publicação
- Classificação automática por assuntos

### 4.2 Classificação de Assuntos

O sistema identifica 12 categorias baseadas em palavras-chave:

| Assunto | Cartas | Palavras-chave (exemplos) |
|---------|--------|---------------------------|
| Política | 645 | governo, presidente, eleição, partido |
| Geral | 640 | (sem classificação específica) |
| Sociedade | 570 | sociedade, cidadão, direito, lei |
| Brasil | 466 | brasil, pátria, nação, brasileiro |
| Economia | 398 | inflação, dólar, emprego, PIB |
| Família | 396 | família, pai, mãe, filho, casamento |
| Ética | 252 | moral, valores, corrupção, honestidade |
| Trabalho | 190 | trabalho, emprego, profissão, empresa |
| Saúde | 144 | saúde, hospital, médico, doença |
| Educação | 119 | escola, universidade, ensino, professor |
| Cultura | 106 | arte, música, teatro, literatura |
| Religião | 93 | deus, igreja, fé, bíblia, oração |
| Meio Ambiente | 39 | natureza, ecologia, floresta, poluição |

### 4.3 Estatísticas do OCR

- **Cartas processadas:** 1.408
- **Cartas com ano identificado:** 587 (41,7%)
- **Cartas com data completa:** variável
- **Tempo de processamento:** ~15-20 minutos

---

## 5. Estrutura de Dados

### 5.1 Arquivo: `data/cartas.json`

**Tamanho:** 1,2 MB
**Estrutura:**

```json
{
  "cartas": [
    {
      "id": "vol1_p028_img1",
      "volume": 1,
      "pagina": 28,
      "ano": 1983,
      "data_publicacao": "15/06/1983",
      "imagem": "assets/cartas/vol1/vol1_p028_img1.jpg",
      "texto": "Conteúdo extraído via OCR...",
      "assuntos": ["Brasil", "Política"]
    }
  ]
}
```

### 5.2 Campos

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | string | Identificador único (vol_página_imagem) |
| volume | number | 1 ou 2 |
| pagina | number | Número da página no PDF |
| ano | number/null | Ano extraído do texto |
| data_publicacao | string/null | Data no formato dd/mm/yyyy |
| imagem | string | Caminho relativo da imagem |
| texto | string | Texto extraído via OCR |
| assuntos | array | Lista de assuntos identificados |

---

## 6. Interface Web

### 6.1 Página de Galeria (`cartas.html`)

**Componentes:**

1. **Header com Estatísticas**
   - Total de cartas
   - Anos cobertos (67 anos)
   - Cartas por volume

2. **Timeline de Décadas**
   - Todas
   - 1958-69
   - Anos 80
   - Anos 90
   - 2000s
   - 2010s
   - 2020s

3. **Filtros Laterais**
   - Volume (Todos, Vol 1, Vol 2)
   - Ano (De/Até)
   - Assuntos (checkboxes)

4. **Busca Textual**
   - Pesquisa no conteúdo OCR

5. **Grid de Cartas**
   - Miniaturas com hover
   - Badge de volume
   - Ano sobreposto
   - Assuntos no card

6. **Modal de Visualização**
   - Imagem ampliada
   - Metadados completos
   - Texto OCR
   - Navegação por setas

### 6.2 Arquivos da Interface

| Arquivo | Tamanho | Descrição |
|---------|---------|-----------|
| cartas.html | 8,2 KB | Estrutura HTML da galeria |
| css/cartas.css | 8,5 KB | Estilos específicos |
| js/cartas.js | 9,8 KB | Lógica de filtros e navegação |

### 6.3 Funcionalidades JavaScript

- Carregamento assíncrono do JSON
- Filtros em tempo real
- Paginação (24 cartas por página)
- Ordenação (página, ano, volume)
- Parâmetros na URL (`?volume=1&ano=1990`)
- Modal com navegação por teclado (setas, ESC)
- Estatísticas dinâmicas

---

## 7. Imagens de Referência

### 7.1 Imagens Extraídas/Utilizadas

| Arquivo | Origem | Uso |
|---------|--------|-----|
| capa-vol1.png | PDF Capa Vol 1 | Index, Volume 1 |
| capa-vol2.png | PDF Capa Vol 2 | Index, Volume 2 |
| silvano-correa.jpg | PDF Vol 2, p.10 | Página Sobre |
| carta-jfk.jpg | PDF Vol 2, p.10 | Destaque Index |

### 7.2 Carta do Presidente Kennedy

**Destaque especial na página inicial:**
- Data: 13 de janeiro de 1961
- Origem: United States Senate, Washington, D.C.
- Destinatário: Silvano Corrêa, Pittsburgh, Pennsylvania
- Contexto: Agradecimento pela mensagem de congratulações pela eleição presidencial

---

## 8. Atualizações no Site

### 8.1 Navegação

Adicionado link "Cartas" no menu de todas as páginas:
- index.html
- sobre.html
- volume1.html
- volume2.html
- contato.html

### 8.2 Página Inicial (index.html)

- Seção de destaque com carta do JFK
- Capas reais dos livros nos cards de volume
- Link direto para galeria de cartas

### 8.3 Página Sobre (sobre.html)

- Foto do autor Silvano Corrêa na sidebar

### 8.4 Páginas de Volume

- Imagem da capa ao lado da introdução
- Botão "Ver Cartas do Volume X" com filtro pré-aplicado

---

## 9. Estrutura Final do Projeto

```
Site SC/
├── index.html
├── sobre.html
├── volume1.html
├── volume2.html
├── cartas.html
├── contato.html
├── IMPLEMENTACAO.md
├── .gitignore
│
├── css/
│   ├── styles.css
│   └── cartas.css
│
├── js/
│   ├── main.js
│   └── cartas.js
│
├── data/
│   └── cartas.json (1,2 MB)
│
├── scripts/
│   ├── extrair_cartas.py
│   └── processar_ocr.py
│
├── assets/
│   ├── images/
│   │   ├── capa-vol1.png
│   │   ├── capa-vol2.png
│   │   ├── carta-jfk.jpg
│   │   └── silvano-correa.jpg
│   │
│   └── cartas/
│       ├── manifest.json
│       ├── vol1/ (433 imagens)
│       └── vol2/ (975 imagens)
│
└── PDFs originais (não versionados)
    ├── SILAVANO CORRÊA _LIVRO_01_ARQUIVO_FINAL.pdf
    ├── SILAVANO CORRÊA _LIVRO_01_CAPA.pdf
    ├── SILVANO CORRÊA _ VOLUME 2_ ARQUIVO FINAL.pdf
    └── SILVANO CORRÊA _ VOLUME 2_ ARQUIVO FINAL_CAPA.pdf
```

---

## 10. Commits Realizados

### Commit 1: `ccb0d27`
**Mensagem:** Adicionar galeria de cartas com extração OCR e destaque JFK

- 1.421 arquivos adicionados
- Extração completa das imagens
- Processamento OCR
- Interface da galeria
- Destaque carta JFK

### Commit 2: `7364dbd`
**Mensagem:** Melhorar galeria com timeline, estatísticas e imagens de referência

- 12 arquivos alterados
- Header com estatísticas
- Timeline por décadas
- Capas reais dos livros
- Foto do autor

---

## 11. Tecnologias Utilizadas

### Backend (Scripts Python)
- **PyMuPDF (fitz):** Manipulação de PDFs
- **Pillow:** Processamento de imagens
- **pytesseract:** Interface para OCR
- **Tesseract OCR:** Motor de reconhecimento

### Frontend
- **HTML5:** Estrutura semântica
- **CSS3:** Estilos com variáveis CSS, Grid, Flexbox
- **JavaScript (ES6+):** Vanilla JS, sem frameworks
- **Fetch API:** Carregamento assíncrono de dados

### Hospedagem
- **GitHub Pages:** Hospedagem estática gratuita

---

## 12. Melhorias Futuras Sugeridas

1. **Qualidade do OCR**
   - Pré-processamento de imagens (contraste, binarização)
   - Treinamento de modelo específico para tipografia antiga

2. **Busca Avançada**
   - Busca por proximidade de palavras
   - Destacar termos encontrados no texto

3. **Metadados**
   - Extração manual/assistida de datas não identificadas
   - Categorização refinada dos assuntos

4. **Performance**
   - Lazy loading de imagens
   - Compressão adicional das imagens
   - Paginação no servidor (se necessário)

5. **Acessibilidade**
   - Atributos ARIA completos
   - Navegação por teclado aprimorada
   - Alto contraste

---

## 13. Conclusão

A implementação foi concluída com sucesso, permitindo que os visitantes do site naveguem por mais de 60 anos de correspondências publicadas por Silvano Corrêa. O sistema de filtros e busca facilita encontrar cartas específicas por período, volume ou tema, enquanto o destaque para a carta do presidente Kennedy adiciona um elemento histórico de grande valor ao site.

---

*Relatório gerado automaticamente durante a implementação.*
*Co-Authored-By: Claude Opus 4.5*
