/**
 * Cartas - Sistema de navegação e filtros
 * Site Silvano Corrêa
 */

(function() {
    'use strict';

    // Configurações
    const CONFIG = {
        cartasPorPagina: 24,
        dataPath: 'data/cartas.json'
    };

    // Estado da aplicação
    let state = {
        cartas: [],
        cartasFiltradas: [],
        paginaAtual: 0,
        filtros: {
            volume: 'todos',
            anoInicio: null,
            anoFim: null,
            assuntos: [],
            busca: ''
        },
        cartaAtual: null
    };

    // Elementos DOM
    let els = {};

    // Inicialização
    document.addEventListener('DOMContentLoaded', init);

    async function init() {
        cacheElements();
        setupEventListeners();
        await carregarCartas();
    }

    function cacheElements() {
        els = {
            grid: document.getElementById('cartas-grid'),
            loading: document.getElementById('loading'),
            estadoVazio: document.getElementById('estado-vazio'),
            resultadosCount: document.getElementById('resultados-count'),
            btnCarregar: document.getElementById('btn-carregar'),
            inputBusca: document.getElementById('busca-texto'),
            btnBuscar: document.getElementById('btn-buscar'),
            selectAnoInicio: document.getElementById('ano-inicio'),
            selectAnoFim: document.getElementById('ano-fim'),
            selectOrdenar: document.getElementById('ordenar'),
            filtrosSidebar: document.getElementById('filtros-sidebar'),
            filtrosToggle: document.getElementById('filtros-toggle'),
            btnLimpar: document.getElementById('btn-limpar'),
            modal: document.getElementById('modal'),
            modalImg: document.getElementById('modal-img'),
            modalVolume: document.getElementById('modal-volume'),
            modalPagina: document.getElementById('modal-pagina'),
            modalAno: document.getElementById('modal-ano'),
            modalData: document.getElementById('modal-data'),
            modalAssuntos: document.getElementById('modal-assuntos'),
            modalTexto: document.getElementById('modal-texto'),
            modalClose: document.getElementById('modal-close'),
            modalPrev: document.getElementById('modal-prev'),
            modalNext: document.getElementById('modal-next'),
            assuntosLista: document.getElementById('assuntos-lista')
        };
    }

    function setupEventListeners() {
        // Busca
        els.btnBuscar?.addEventListener('click', () => {
            state.filtros.busca = els.inputBusca.value.trim().toLowerCase();
            aplicarFiltros();
        });

        els.inputBusca?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                state.filtros.busca = els.inputBusca.value.trim().toLowerCase();
                aplicarFiltros();
            }
        });

        // Filtro de Volume
        document.querySelectorAll('input[name="volume"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                state.filtros.volume = e.target.value;
                aplicarFiltros();
            });
        });

        // Filtro de Ano
        els.selectAnoInicio?.addEventListener('change', (e) => {
            state.filtros.anoInicio = e.target.value ? parseInt(e.target.value) : null;
            aplicarFiltros();
        });

        els.selectAnoFim?.addEventListener('change', (e) => {
            state.filtros.anoFim = e.target.value ? parseInt(e.target.value) : null;
            aplicarFiltros();
        });

        // Ordenação
        els.selectOrdenar?.addEventListener('change', ordenarCartas);

        // Carregar mais
        els.btnCarregar?.addEventListener('click', carregarMais);

        // Toggle filtros mobile
        els.filtrosToggle?.addEventListener('click', () => {
            els.filtrosSidebar?.classList.toggle('active');
        });

        // Limpar filtros
        els.btnLimpar?.addEventListener('click', limparFiltros);

        // Modal
        els.modalClose?.addEventListener('click', fecharModal);
        els.modal?.addEventListener('click', (e) => {
            if (e.target === els.modal) fecharModal();
        });
        els.modalPrev?.addEventListener('click', cartaAnterior);
        els.modalNext?.addEventListener('click', proximaCarta);

        // Teclado
        document.addEventListener('keydown', (e) => {
            if (!els.modal?.classList.contains('active')) return;
            if (e.key === 'Escape') fecharModal();
            if (e.key === 'ArrowLeft') cartaAnterior();
            if (e.key === 'ArrowRight') proximaCarta();
        });
    }

    async function carregarCartas() {
        try {
            els.loading.style.display = 'block';
            els.grid.style.display = 'none';

            const response = await fetch(CONFIG.dataPath);
            if (!response.ok) throw new Error('Erro ao carregar cartas');

            const data = await response.json();
            state.cartas = data.cartas || [];

            // Processar parâmetros da URL
            processarURLParams();

            // Popular filtros de ano e assuntos
            popularFiltroAno();
            popularFiltroAssuntos();

            // Aplicar filtros iniciais
            aplicarFiltros();

        } catch (error) {
            console.error('Erro ao carregar cartas:', error);
            els.loading.innerHTML = '<p>Erro ao carregar cartas. Tente novamente.</p>';
        }
    }

    function processarURLParams() {
        const params = new URLSearchParams(window.location.search);

        if (params.has('volume')) {
            const vol = params.get('volume');
            state.filtros.volume = vol;
            const radio = document.querySelector(`input[name="volume"][value="${vol}"]`);
            if (radio) radio.checked = true;
        }

        if (params.has('ano')) {
            const ano = parseInt(params.get('ano'));
            state.filtros.anoInicio = ano;
            state.filtros.anoFim = ano;
        }

        if (params.has('assunto')) {
            state.filtros.assuntos = [params.get('assunto')];
        }

        if (params.has('busca')) {
            state.filtros.busca = params.get('busca').toLowerCase();
            if (els.inputBusca) els.inputBusca.value = params.get('busca');
        }
    }

    function popularFiltroAno() {
        const anos = [...new Set(state.cartas.map(c => c.ano).filter(a => a))].sort();

        if (anos.length === 0) return;

        const anoMin = Math.min(...anos);
        const anoMax = Math.max(...anos);

        // Popular selects
        [els.selectAnoInicio, els.selectAnoFim].forEach(select => {
            if (!select) return;
            select.innerHTML = '<option value="">Todos</option>';
            for (let ano = anoMin; ano <= anoMax; ano++) {
                select.innerHTML += `<option value="${ano}">${ano}</option>`;
            }
        });

        // Aplicar valores dos filtros se existirem
        if (state.filtros.anoInicio && els.selectAnoInicio) {
            els.selectAnoInicio.value = state.filtros.anoInicio;
        }
        if (state.filtros.anoFim && els.selectAnoFim) {
            els.selectAnoFim.value = state.filtros.anoFim;
        }
    }

    function popularFiltroAssuntos() {
        // Coletar todos os assuntos únicos
        const assuntosSet = new Set();
        state.cartas.forEach(c => {
            if (c.assuntos) {
                c.assuntos.forEach(a => assuntosSet.add(a));
            }
        });

        const assuntos = [...assuntosSet].sort();

        if (!els.assuntosLista || assuntos.length === 0) return;

        els.assuntosLista.innerHTML = assuntos.map(assunto => `
            <div class="filtro-opcao">
                <input type="checkbox" id="assunto-${assunto}" value="${assunto}"
                    ${state.filtros.assuntos.includes(assunto) ? 'checked' : ''}>
                <label for="assunto-${assunto}">${assunto}</label>
            </div>
        `).join('');

        // Event listeners para checkboxes de assuntos
        els.assuntosLista.querySelectorAll('input[type="checkbox"]').forEach(cb => {
            cb.addEventListener('change', () => {
                state.filtros.assuntos = [...els.assuntosLista.querySelectorAll('input:checked')]
                    .map(c => c.value);
                aplicarFiltros();
            });
        });
    }

    function aplicarFiltros() {
        state.cartasFiltradas = state.cartas.filter(carta => {
            // Filtro de volume
            if (state.filtros.volume !== 'todos') {
                if (carta.volume !== parseInt(state.filtros.volume)) return false;
            }

            // Filtro de ano
            if (state.filtros.anoInicio && carta.ano < state.filtros.anoInicio) return false;
            if (state.filtros.anoFim && carta.ano > state.filtros.anoFim) return false;

            // Filtro de assuntos
            if (state.filtros.assuntos.length > 0) {
                const temAssunto = state.filtros.assuntos.some(a =>
                    carta.assuntos && carta.assuntos.includes(a)
                );
                if (!temAssunto) return false;
            }

            // Filtro de busca textual
            if (state.filtros.busca) {
                const texto = (carta.texto || '').toLowerCase();
                if (!texto.includes(state.filtros.busca)) return false;
            }

            return true;
        });

        // Ordenar
        ordenarCartas();

        // Resetar paginação
        state.paginaAtual = 0;

        // Renderizar
        renderizarCartas(true);
    }

    function ordenarCartas() {
        const ordem = els.selectOrdenar?.value || 'pagina';

        state.cartasFiltradas.sort((a, b) => {
            switch (ordem) {
                case 'ano-asc':
                    return (a.ano || 0) - (b.ano || 0);
                case 'ano-desc':
                    return (b.ano || 0) - (a.ano || 0);
                case 'volume':
                    return a.volume - b.volume || a.pagina - b.pagina;
                case 'pagina':
                default:
                    return a.volume - b.volume || a.pagina - b.pagina;
            }
        });

        if (els.selectOrdenar) {
            state.paginaAtual = 0;
            renderizarCartas(true);
        }
    }

    function renderizarCartas(limpar = false) {
        if (limpar) {
            els.grid.innerHTML = '';
        }

        els.loading.style.display = 'none';

        const inicio = state.paginaAtual * CONFIG.cartasPorPagina;
        const fim = inicio + CONFIG.cartasPorPagina;
        const cartasPagina = state.cartasFiltradas.slice(inicio, fim);

        if (state.cartasFiltradas.length === 0) {
            els.grid.style.display = 'none';
            els.estadoVazio.style.display = 'block';
            els.btnCarregar.style.display = 'none';
        } else {
            els.grid.style.display = 'grid';
            els.estadoVazio.style.display = 'none';

            cartasPagina.forEach((carta, index) => {
                const card = criarCardCarta(carta, inicio + index);
                els.grid.appendChild(card);
            });

            // Mostrar/ocultar botão carregar mais
            const temMais = fim < state.cartasFiltradas.length;
            els.btnCarregar.style.display = temMais ? 'inline-block' : 'none';
        }

        // Atualizar contador
        atualizarContador();
    }

    function criarCardCarta(carta, indice) {
        const card = document.createElement('article');
        card.className = 'carta-card';
        card.setAttribute('data-indice', indice);

        const anoDisplay = carta.ano || '?';
        const assuntosDisplay = (carta.assuntos || []).slice(0, 2);

        card.innerHTML = `
            <div class="carta-thumb">
                <img src="${carta.imagem}" alt="Carta ${carta.id}" loading="lazy">
                <div class="carta-overlay">
                    <span class="carta-volume vol${carta.volume}">Vol. ${carta.volume}</span>
                    <span class="carta-ano">${anoDisplay}</span>
                </div>
            </div>
            <div class="carta-info">
                <p class="carta-pagina">Página ${carta.pagina}</p>
                <div class="carta-assuntos">
                    ${assuntosDisplay.map(a => `<span class="carta-assunto">${a}</span>`).join('')}
                </div>
            </div>
        `;

        card.addEventListener('click', () => abrirModal(indice));

        return card;
    }

    function atualizarContador() {
        const exibidas = Math.min(
            (state.paginaAtual + 1) * CONFIG.cartasPorPagina,
            state.cartasFiltradas.length
        );
        els.resultadosCount.innerHTML = `Exibindo <strong>${exibidas}</strong> de <strong>${state.cartasFiltradas.length}</strong> cartas`;
    }

    function carregarMais() {
        state.paginaAtual++;
        renderizarCartas(false);
    }

    function limparFiltros() {
        state.filtros = {
            volume: 'todos',
            anoInicio: null,
            anoFim: null,
            assuntos: [],
            busca: ''
        };

        // Reset UI
        document.querySelector('input[name="volume"][value="todos"]').checked = true;
        if (els.selectAnoInicio) els.selectAnoInicio.value = '';
        if (els.selectAnoFim) els.selectAnoFim.value = '';
        if (els.inputBusca) els.inputBusca.value = '';

        els.assuntosLista?.querySelectorAll('input[type="checkbox"]').forEach(cb => {
            cb.checked = false;
        });

        // Limpar URL params
        window.history.replaceState({}, '', window.location.pathname);

        aplicarFiltros();
    }

    // Modal
    function abrirModal(indice) {
        state.cartaAtual = indice;
        const carta = state.cartasFiltradas[indice];

        if (!carta) return;

        els.modalImg.src = carta.imagem;
        els.modalVolume.textContent = `Volume ${carta.volume}`;
        els.modalPagina.textContent = carta.pagina;
        els.modalAno.textContent = carta.ano || 'Desconhecido';
        els.modalData.textContent = carta.data_publicacao || 'Desconhecida';

        // Assuntos
        els.modalAssuntos.innerHTML = (carta.assuntos || [])
            .map(a => `<span class="modal-assunto">${a}</span>`)
            .join('');

        // Texto OCR
        els.modalTexto.textContent = carta.texto || 'Texto não disponível';

        // Navegação
        els.modalPrev.disabled = indice === 0;
        els.modalNext.disabled = indice === state.cartasFiltradas.length - 1;

        els.modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function fecharModal() {
        els.modal.classList.remove('active');
        document.body.style.overflow = '';
        state.cartaAtual = null;
    }

    function cartaAnterior() {
        if (state.cartaAtual > 0) {
            abrirModal(state.cartaAtual - 1);
        }
    }

    function proximaCarta() {
        if (state.cartaAtual < state.cartasFiltradas.length - 1) {
            abrirModal(state.cartaAtual + 1);
        }
    }

})();
