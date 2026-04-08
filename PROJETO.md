# silvanocorrea.com.br — Documentação do Projeto

> **Documento de referência** para o Claude Desktop e para registro histórico.
> Mantenha este arquivo atualizado a cada alteração significativa no projeto.

---

## 1. Identidade do Projeto

| Campo | Valor |
|---|---|
| **Site** | https://www.silvanocorrea.com.br |
| **Autor** | Silvano Correa |
| **Gestor técnico** | Alexandre Correa (filho do Silvano) |
| **Última atualização deste doc** | Abril de 2026 |

---

## 2. Infraestrutura

### 2.1 Repositório GitHub
| Campo | Valor |
|---|---|
| **URL** | https://github.com/aleapc/minhas-cartas |
| **Owner** | aleapc |
| **Branch principal** | `master` |
| **Acesso** | Conta GitHub do Alexandre |

### 2.2 Hospedagem — Vercel
| Campo | Valor |
|---|---|
| **Projeto** | `minhas-cartas` |
| **Organização** | `alexandre-correas-projects` |
| **URL do painel** | https://vercel.com/alexandre-correas-projects/minhas-cartas |
| **URL de deployments** | https://vercel.com/alexandre-correas-projects/minhas-cartas/deployments |
| **Deploy automático** | Sim — cada push em `master` gera um novo deployment |
| **Promoção para produção** | Manual — clicar em "Deployment Actions" → "Promote to Production" |

### 2.3 Domínio
| Campo | Valor |
|---|---|
| **Domínio** | silvanocorrea.com.br |
| **www** | www.silvanocorrea.com.br |
| **Configurado em** | Vercel (DNS apontando para Vercel) |

---

## 3. Estrutura de Arquivos

```
minhas-cartas/
├── index.html              ← Portal de entrada (página principal) — PODE EDITAR
├── sete-vidas.html         ← Página do livro "As Sete Vidas de Silvano" — PODE EDITAR
├── cartas-home.html        ← Página inicial de Minhas Cartas — ⛔ NÃO MODIFICAR
├── cartas.html             ← Leitor das cartas — ⛔ NÃO MODIFICAR
├── volume1.html            ← Volume 1 das cartas — ⛔ NÃO MODIFICAR
├── volume2.html            ← Volume 2 das cartas — ⛔ NÃO MODIFICAR
├── sobre.html              ← Sobre o Autor — ⛔ NÃO MODIFICAR
├── contato.html            ← Contato — ⛔ NÃO MODIFICAR
├── css/
│   └── styles.css          ← Folha de estilos global (header, nav, footer, tipografia)
├── assets/
│   └── images/
│       ├── capa-vol1.png           ← Capa Volume 1 de Minhas Cartas
│       ├── capa-vol2.png           ← Capa Volume 2 de Minhas Cartas (se existir)
│       └── capa-sete-vidas.jpg     ← Capa do livro As Sete Vidas de Silvano
└── PROJETO.md              ← Este arquivo de documentação
```

> **Regra crítica:** Nunca modificar `cartas-home.html`, `cartas.html`, `volume1.html`, `volume2.html`, `sobre.html`, `contato.html`. Apenas `index.html` e `sete-vidas.html` são editáveis.

---

## 4. Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| HTML5 semântico | Estrutura das páginas |
| CSS3 (inline em `<style>` no `index.html`) | Estilos do portal (hero, cards, botões) |
| `css/styles.css` | Estilos globais: header fixo, nav, tipografia |
| Google Fonts | **Playfair Display** (títulos) + **Source Sans Pro** (corpo) |
| Vercel | Hospedagem e CDN |
| GitHub | Controle de versão e editor online |

---

## 5. Componentes do Portal (index.html)

### 5.1 Header
- Classe: `.main-header`
- Posição: `fixed` no topo
- Altura: **73px**
- Contém logo "Silvano Correa" + navegação com links para: Minhas Cartas, Sete Vidas, Sobre o Autor, Contato
- **Atenção:** Por ser `position: fixed`, o hero precisa de `padding-top: calc(73px + espaço visual)` para não ficar escondido atrás do header.

### 5.2 Hero
```css
.portal-hero {
    background: linear-gradient(160deg, #1a2744 0%, #2a3f6f 100%);
    color: #fff;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: calc(73px + 2.5rem) 2rem 2.5rem;
}
.portal-hero-inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
}
.portal-hero h1 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(1.4rem, 2.8vw, 2.2rem);
    font-weight: 700;
    color: #fff !important;
    margin-bottom: .6rem;
    max-width: 100%;
    overflow-wrap: break-word;
}
```
HTML do hero:
```html
<section class="portal-hero">
    <div class="portal-hero-inner">
        <h1>Bem-vindo às Obras de Silvano Correa</h1>
        <hr class="hero-divider">
        <p class="tagline">Escritor, idealista e cronista do cotidiano brasileiro.<br>
        Explore suas duas obras disponíveis ao leitor.</p>
    </div>
</section>
```

### 5.3 Cards das Obras
- Seção `.cards-section` com fundo `#f8f4ee`
- Grid de 2 colunas (`grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))`)
- Cada card tem: capa, título, subtítulo, descrição, botões de ação

### 5.4 Rodapé
```html
<footer class="portal-footer">
    <p>&copy; 2026 Silvano Correa. Todos os direitos reservados.</p>
</footer>
```

---

## 6. Obras Publicadas

### 6.1 Minhas Cartas — Coletânea de Cartas ao Jornal
| Campo | Valor |
|---|---|
| **Descrição** | Cartas publicadas no Estadão entre 1958 e 2025 |
| **Página interna** | `cartas-home.html` |
| **Volume 1 (Kindle)** | https://www.amazon.com.br/dp/B0GPFH9VQ3 |
| **Volume 2 (Kindle)** | https://www.amazon.com.br/dp/B0GPFNKYLN |
| **Status** | ✅ Publicado e à venda na Amazon |

### 6.2 As Sete Vidas de Silvano — Autobiografia
| Campo | Valor |
|---|---|
| **Descrição** | Autobiografia — da Baía de Guanabara às páginas do Estadão |
| **Página interna** | `sete-vidas.html` |
| **Capa** | `assets/images/capa-sete-vidas.jpg` |
| **Preço KDP** | R$ 45,00 |
| **Status (abril/2026)** | 🟡 Em revisão no KDP — ainda não publicado |
| **Link Amazon atual** | Busca genérica (temporário): `amazon.com.br/s?k=As+Sete+Vidas+de+Silvano+Correa` |
| **Ação pendente** | Quando publicar: substituir o link pelo ASIN direto (`amazon.com.br/dp/[ASIN]`) em `index.html` e `sete-vidas.html` |

---

## 7. Paleta de Cores

| Nome | Hex | Uso |
|---|---|---|
| Azul escuro | `#1a2744` | Header, footer, fundo hero, textos primários |
| Azul médio | `#2a3f6f` | Gradiente do hero |
| Laranja Amazon | `#ff9900` | Botões primários, divisor do hero |
| Bege claro | `#f8f4ee` | Fundo da seção de cards |
| Branco | `#ffffff` | Cards, textos sobre fundo escuro |
| Cinza texto | `#555555` | Parágrafos descritivos |

---

## 8. Fontes

| Fonte | Pesos | Uso |
|---|---|---|
| Playfair Display | 400, 700, italic | Títulos (h1, h2), logo |
| Source Sans Pro | 300, 400, 600 | Corpo de texto, botões, nav |

Carregadas via Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Source+Sans+Pro:wght@300;400;600&display=swap" rel="stylesheet">
```

---

## 9. Workflow para Alterações

### Passo a passo para editar e publicar

1. **Abrir o editor GitHub:**
   `https://github.com/aleapc/minhas-cartas/edit/master/[nome-do-arquivo].html`

2. **Aguardar 4 segundos** para o editor CodeMirror (CM6) carregar completamente.

3. **Localizar e editar** via JavaScript no console (método preferido):
```javascript
const view = document.querySelector('.cm-content').cmTile.view;
const text = view.state.doc.toString();
const from = text.indexOf('texto a substituir');
const to = from + 'texto a substituir'.length;
view.dispatch({ changes: { from, to, insert: 'novo texto' } });
```

4. **Fazer o commit:**
```javascript
// Clicar em "Commit changes..."
[...document.querySelectorAll('button')]
  .find(b => b.textContent.trim() === 'Commit changes...')
  .click();

// Confirmar no dialog
const dialog = document.querySelector('dialog[open]');
[...dialog.querySelectorAll('button')]
  .find(b => b.textContent.trim() === 'Commit changes')
  .click();
```

5. **Acessar Vercel deployments:**
   `https://vercel.com/alexandre-correas-projects/minhas-cartas/deployments`

6. **Promover para produção:**
```javascript
// Clicar no botão de ações do primeiro deployment
document.querySelectorAll('button[aria-label="Deployment Actions"]')[0].click();
// Aguardar 1s, depois clicar em "Promote to Production"
setTimeout(() => {
  [...document.querySelectorAll('[role="menuitem"]')]
    .find(i => i.textContent.includes('Promote to Production'))
    .click();
}, 1000);
// Confirmar no dialog
const dialog = document.querySelector('dialog[open]');
[...dialog.querySelectorAll('button')]
  .find(b => b.textContent.trim() === 'Promote to Production')
  .click();
```

7. **Aguardar ~8 segundos** e verificar se o status mudou para "Ready / Production".

8. **Verificar no site ao vivo:** https://www.silvanocorrea.com.br

---

## 10. Histórico de Alterações

| Data | Arquivo | Alteração |
|---|---|---|
| Fev/2026 | `index.html` | Criação do portal (landing page) com hero e cards das obras |
| Fev/2026 | `sete-vidas.html` | Criação da página da autobiografia |
| Fev–Mar/2026 | `index.html` | Múltiplos ajustes no hero: centralização vertical, font-size responsivo, padding para header fixo |
| Mar/2026 | `index.html` | Refatoração do hero: substituição de `.container` por `.portal-hero-inner` com flexbox próprio |
| Mar/2026 | `index.html` | Título do hero em uma linha única (removido `<br>`); font-size `clamp(1.4rem, 2.8vw, 2.2rem)` |
| Mar/2026 | `index.html` | Adicionado `padding-top: calc(73px + 2.5rem)` para compensar header fixo de 73px |
| Abr/2026 | `index.html` | Rodapé corrigido de © 2025 para © 2026 |

---

## 11. Ação Pendente (Prioritária)

### Quando "As Sete Vidas de Silvano" for publicado na Amazon:

1. Verificar no KDP: https://kdp.amazon.com (conta do Silvano) — aguardar status "Live"
2. Copiar o ASIN do livro (ex: `B0XXXXXX`)
3. Editar `index.html`: substituir o link do botão "Comprar no Kindle" do card Sete Vidas:
   - **De:** `https://www.amazon.com.br/s?k=As+Sete+Vidas+de+Silvano+Correa`
   - **Para:** `https://www.amazon.com.br/dp/[ASIN]`
4. Editar `sete-vidas.html`: fazer a mesma substituição no botão de compra da página do livro
5. Fazer commit e promover para produção no Vercel

---

*Documento gerado em abril de 2026. Atualizar sempre que houver mudanças significativas na infraestrutura ou no conteúdo do site.*
