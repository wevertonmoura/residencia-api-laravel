// --- CONFIGURAÇÃO DE ENDPOINTS (ARQUITETURA HÍBRIDA) ---
const LARAVEL_API = 'http://127.0.0.1/api';       // Para ler/salvar artigos (Porta 80)
const PYTHON_API  = 'http://127.0.0.1:5000/gerar'; // Para gerar inteligência (Porta 5000)

// Variável global para armazenar os artigos e evitar erros de aspas/caracteres especiais no HTML
let artigosCache = []; 

// --- UTILITÁRIOS ---

function formatDate(dataString) {
    if (!dataString) return "Data Indisponível";
    try {
        const data = new Date(dataString);
        if(isNaN(data.getTime())) return "Processando...";
        
        return data.toLocaleDateString('pt-BR', {
            day: '2-digit', month: '2-digit', year: 'numeric'
        }) + ' às ' + data.toLocaleTimeString('pt-BR', {
            hour: '2-digit', minute: '2-digit'
        });
    } catch (e) {
        return "Erro Data";
    }
}

function getTicker(artigo) {
    return artigo.ticker || artigo.acao_ticker || 'N/A';
}

async function apiLaravel(endpoint, method='GET', body=null) {
    const url = `${LARAVEL_API}${endpoint}`;
    const opts = { 
        method, 
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        } 
    };
    
    if(body) opts.body = JSON.stringify(body);
    
    try {
        const res = await fetch(url, opts);
        if(!res.ok) throw new Error(`Erro Laravel: ${res.status}`);
        if(res.status === 204) return true;
        return await res.json();
    } catch(e) {
        console.error("Falha na comunicação com Laravel:", e);
        return null; 
    }
}

// --- RENDERIZAÇÃO ---

function getTagColors(recomendacao) {
    const tag = recomendacao ? recomendacao.toUpperCase() : 'NEUTRO';
    switch (tag) {
        case 'COMPRA':
            return { bg: 'bg-compra/20 text-compra border-compra', colorClass: 'compra' };
        case 'VENDA':
            return { bg: 'bg-venda/20 text-venda border-venda', colorClass: 'venda' };
        case 'NEUTRO':
        default:
            return { bg: 'bg-neutro/20 text-neutro border-neutro', colorClass: 'neutro' };
    }
}

function renderCard(a, type) {
    let controlButtons = '';
    const tickerName = getTicker(a);
    const dataHora = formatDate(a.updated_at || a.created_at);
    const colors = getTagColors(a.recomendacao);
    const isUnderReview = type === 'rascunho' && a.motivo_revisao;

    // Adição de métrica de Views para artigos publicados (Simulação)
    const viewsElement = (type === 'publicado') ? `
        <span class="text-xs font-medium text-compra flex items-center gap-1">
            <i class="ph-bold ph-chart-line"></i> ${(Math.floor(Math.random() * (15000 - 500 + 1)) + 500 / 1000).toFixed(1)}K Views
        </span>` : `
        <span class="text-[10px] text-slate-500">${dataHora}</span>
    `;
    
    // Configuração dos Botões de CONTROLE (PUBLICAR/DESPUBLICAR)
    if(type === 'rascunho') {
        controlButtons = `
            <button onclick="aprovarArtigo('${a.id}')" class="flex-1 bg-compra hover:bg-emerald-500 text-white text-xs font-bold py-2 rounded transition shadow-lg shadow-emerald-900/20">PUBLICAR</button>
            <button onclick="moverParaLixeira('${a.id}')" class="px-3 py-2 bg-slate-700 hover:bg-venda/20 hover:text-venda text-slate-400 rounded transition" title="Descartar">🗑️</button>
        `;
    } else if (type === 'publicado') {
        controlButtons = `<button onclick="despublicarArtigo('${a.id}')" class="w-full bg-venda hover:bg-red-600 text-white text-xs font-medium py-2 rounded border border-venda transition">🔴 DESPUBLICAR</button>`;
    } else { // Lixeira
        controlButtons = `
            <button onclick="restaurarArtigo('${a.id}')" class="flex-1 text-brand-400 hover:text-brand-300 font-medium text-xs border border-brand-500/30 rounded py-1.5 hover:bg-brand-500/10 transition">Restaurar</button>
            <button onclick="excluirPermanente('${a.id}')" class="flex-1 text-red-500 hover:text-red-400 font-medium text-xs border border-red-500/30 rounded py-1.5 ml-2 hover:bg-red-500/10 transition">Excluir</button>
        `;
    }
    
    // --- ESTRUTURA FINAL DO CARD (COMPACTA) ---
    return `
    <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700 shadow-sm hover:border-${colors.colorClass} transition-all group relative overflow-hidden flex flex-col h-full">
        <div class="absolute top-0 left-0 w-1 h-full ${type === 'rascunho' ? 'bg-neutro' : (type === 'publicado' ? 'bg-compra' : 'bg-venda')}"></div>
        
        <div class="flex justify-between items-start mb-2 pl-3">
            <div class="flex items-center gap-2">
                 <span class="text-[10px] font-bold text-white bg-slate-700 px-2 py-0.5 rounded uppercase tracking-wider shadow-sm">${tickerName}</span>
                 <span class="inline-block text-[10px] uppercase font-bold px-2 py-1 rounded border ${colors.bg}">${a.recomendacao || 'Análise'}</span>
            </div>
            ${viewsElement}
        </div>
        
        <div class="pl-3 flex-1">
            <h4 class="text-white font-extrabold text-lg leading-snug mb-1 transition-colors line-clamp-2">${a.titulo}</h4>
            <p class="text-sm text-slate-400 mb-2 line-clamp-2">${a.resumo || a.conteudo || "Clique em veja mais para ler a análise completa."}</p>
            
            ${isUnderReview ? `<span class="text-xs font-medium text-red-400 flex items-center gap-1" title="${a.motivo_revisao}"><i class="ph-bold ph-warning"></i> Revisão Necessária</span>` : `<p class="text-xs text-slate-500">ID: ${a.id}</p>`}
        </div>
        
        <div class="flex gap-2 mt-auto pl-3 py-1 border-t border-slate-700/50 items-center">
            
            <button 
                class="text-brand-400 hover:text-brand-300 font-semibold transition-colors text-sm flex items-center gap-1 mr-4"
                onclick="abrirModalConteudo('${a.id}')"
            >
                <i class="ph-bold ph-eye"></i> Veja Mais
            </button>
            
            <div class="flex flex-1 gap-2">
                 ${controlButtons}
            </div>
        </div>
    </div>`;
}

// --- FUNÇÕES DE MODAL DE CONTEÚDO ---

function abrirModalConteudo(id) {
    // Busca o artigo dentro do cache global usando o ID
    const artigo = artigosCache.find(item => String(item.id) === String(id));
    
    if (!artigo) {
        alert("Erro: Conteúdo do artigo não encontrado. Tente atualizar a página.");
        return;
    }

    const modal = document.getElementById('modal-visualizar-artigo');
    const tituloElement = document.getElementById('modal-titulo');
    const corpoElement = document.getElementById('modal-corpo-conteudo');

    if (!modal || !tituloElement || !corpoElement) {
        alert("Erro: Elementos do modal não encontrados no HTML.");
        return;
    }

    // Preenche o modal
    tituloElement.innerText = artigo.titulo;
    
    // Tratamento básico de Markdown para o conteúdo (Quebras de linha e Negritos)
    const textoFormatado = (artigo.conteudo || "")
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    corpoElement.innerHTML = `<div class="prose prose-invert max-w-none">${textoFormatado}</div>`;
    
    // Exibe o modal
    modal.classList.remove('hidden'); 
    document.body.classList.add('overflow-hidden');
}

function fecharModalConteudo() {
    const modal = document.getElementById('modal-visualizar-artigo');
    if (modal) modal.classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
}

// --- RESTANTE DA LÓGICA ---

function emptyState(msg) {
    return `<div class="col-span-full py-8 text-center border-2 border-dashed border-slate-800 rounded-xl">
        <p class="text-slate-500 text-sm font-medium">${msg}</p>
    </div>`;
}

function showTab(tabName) {
    document.getElementById('tab-painel').classList.add('hidden');
    document.getElementById('tab-lixeira').classList.add('hidden');
    
    const target = document.getElementById(`tab-${tabName}`);
    target.classList.remove('hidden');
    
    document.getElementById('page-title').textContent = tabName === 'lixeira' ? 'Lixeira' : 'Dashboard Financeiro';
    
    document.getElementById('nav-painel').classList.remove('bg-brand-500/10', 'text-brand-500', 'border-brand-500/20');
    document.getElementById('nav-lixeira').classList.remove('bg-brand-500/10', 'text-brand-500', 'border-brand-500/20');
    document.getElementById('nav-painel').classList.add('text-slate-400', 'hover:bg-slate-800');
    document.getElementById('nav-lixeira').classList.add('text-slate-400', 'hover:bg-slate-800');
    document.getElementById(`nav-${tabName}`).classList.add('bg-brand-500/10', 'text-brand-500', 'border-brand-500/20');
    document.getElementById(`nav-${tabName}`).classList.remove('text-slate-400', 'hover:bg-slate-800');
    
    if(tabName === 'lixeira') loadLixeira(); else loadAll();
}

async function loadAll() {
    toggleLoader(true);
    
    const [pendentesResponse, pubResponse] = await Promise.all([
        apiLaravel('/artigos/pendentes'), 
        apiLaravel('/artigos/publicados') 
    ]);

    toggleLoader(false);

    if (!pendentesResponse && !pubResponse) {
        document.getElementById('list-rascunhos').innerHTML = emptyState('Erro ao conectar à API Laravel.');
        return;
    }

    const pendenteData = pendentesResponse?.data || pendentesResponse || [];
    const publicadoData = pubResponse?.data || pubResponse || [];

    // ATUALIZA O CACHE: Junta todos os artigos para o "Veja Mais" funcionar em qualquer lugar
    artigosCache = [...pendenteData, ...publicadoData];

    // Renderiza Rascunhos
    const rascContainer = document.getElementById('list-rascunhos');
    rascContainer.innerHTML = pendenteData.length ? pendenteData.map(a => renderCard(a, 'rascunho')).join('') : emptyState('Sem artigos pendentes.');
    document.getElementById('count-rascunhos').textContent = pendenteData.length; 

    // Renderiza Publicados
    const pubContainer = document.getElementById('list-publicados');
    pubContainer.innerHTML = publicadoData.length ? publicadoData.map(a => renderCard(a, 'publicado')).join('') : emptyState('Nenhum artigo publicado.');
    document.getElementById('count-publicados').textContent = publicadoData.length;
}

async function loadLixeira() {
    toggleLoader(true);
    const lixResponse = await apiLaravel('/artigos/lixeira');
    toggleLoader(false);

    const lixeiraData = lixResponse?.data || lixResponse || [];
    
    // Adiciona itens da lixeira ao cache também para permitir visualização
    artigosCache = [...artigosCache, ...lixeiraData];

    const lixContainer = document.getElementById('list-lixeira');
    lixContainer.innerHTML = lixeiraData.length ? lixeiraData.map(a => renderCard(a, 'lixeira')).join('') : emptyState('Lixeira vazia.');
}

// --- AÇÕES DO LARAVEL ---

async function aprovarArtigo(id) {
    if (!confirm('Confirmar publicação no Portal?')) return;
    toggleLoader(true);
    const result = await apiLaravel(`/artigos/${id}/aprovar`, 'POST');
    toggleLoader(false);
    if (result) await loadAll();
}

async function despublicarArtigo(id) {
    const motivo = prompt('Informe o motivo da despublicação:');
    if (!motivo) return;
    toggleLoader(true);
    const result = await apiLaravel(`/artigos/${id}/desaprovar`, 'POST', { motivo_revisao: motivo }); 
    toggleLoader(false);
    if (result) await loadAll();
}

async function moverParaLixeira(id) {
    if (!confirm('Mover artigo para a Lixeira?')) return;
    toggleLoader(true);
    const result = await apiLaravel(`/artigos/${id}/lixeira`, 'POST');
    toggleLoader(false);
    if(result) await loadAll();
}

async function restaurarArtigo(id) {
    if (!confirm('Restaurar artigo para Rascunho?')) return;
    toggleLoader(true);
    const result = await apiLaravel(`/artigos/${id}/restaurar`, 'POST');
    toggleLoader(false);
    if(result) await loadLixeira();
}

async function excluirPermanente(id) {
    if (!confirm('ATENÇÃO: Apagar permanentemente?')) return;
    toggleLoader(true);
    const result = await apiLaravel(`/artigos/${id}/permanente`, 'DELETE'); 
    toggleLoader(false);
    if(result) await loadLixeira();
}

// --- DISPARO DE I.A. (PYTHON) ---

async function dispararIA() {
    const scope = document.querySelector('input[name="scope"]:checked').value;
    const tickerSelect = document.getElementById('select-ticker');
    
    const payload = {
        scope: scope,
        ticker: (scope === 'single') ? tickerSelect.value : null
    };

    fecharModal();
    alert(`🤖 Comando enviado para a API Python! Os agentes estão trabalhando em segundo plano.`);

    try {
        const response = await fetch(PYTHON_API, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) startPolling();
        else alert("Erro ao contatar os agentes. Verifique se 'api.py' está rodando na porta 5000.");
    } catch(e) { 
        alert("Falha de conexão com a API Python. Verifique o terminal."); 
    }
}

function startPolling() {
    let attempts = 0;
    const interval = setInterval(() => {
        attempts++;
        loadAll();
        if (attempts >= 12) clearInterval(interval);
    }, 5000);
}

// --- AUXILIARES UI ---

function abrirModalGerar() { document.getElementById('modal-gerar').classList.remove('hidden'); }
function fecharModal() { document.getElementById('modal-gerar').classList.add('hidden'); }

function toggleSelect(enable) {
    const sel = document.getElementById('select-ticker');
    sel.disabled = !enable;
    enable ? sel.classList.remove('opacity-50') : sel.classList.add('opacity-50');
}

function toggleLoader(show) {
    const loader = document.getElementById('global-loader');
    if(loader) show ? loader.classList.remove('hidden') : loader.classList.add('hidden');
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    showTab('painel'); 
});