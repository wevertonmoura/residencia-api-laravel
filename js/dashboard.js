// CONFIG API
const API = 'http://127.0.0.1/api';

// --- CORREÇÃO DA DATA BRASILEIRA (RESOLVE "Invalid Date") ---
function formatDate(dataString) {
    if (!dataString) return "Data Indisponível";
    try {
        const data = new Date(dataString);
        if(isNaN(data.getTime())) return "Processando...";
        
        // Retorna a data e hora em formato brasileiro completo
        return data.toLocaleDateString('pt-BR', {
            day: '2-digit', month: '2-digit', year: 'numeric'
        }) + ' às ' + data.toLocaleTimeString('pt-BR', {
            hour: '2-digit', minute: '2-digit'
        });
    } catch (e) {
        return "Erro Data";
    }
}

// CORREÇÃO DO NOME DA AÇÃO (Ticker)
function getTicker(artigo) {
    return artigo.ticker || artigo.acao_ticker || 'N/A';
}

// Wrapper API
async function api(url, method='GET', body=null) {
    const opts = { method, headers: {'Content-Type':'application/json'} };
    if(body) opts.body = JSON.stringify(body);
    try {
        const res = await fetch(url, opts);
        if(!res.ok) throw new Error(`Erro ${res.status}`);
        if(res.status === 204) return true;
        return await res.json();
    } catch(e) {
        console.error(e);
        return null;
    }
}

// RENDERIZAÇÃO DOS CARDS (Usa a função formatDate)
function renderCard(a, type) {
    let btns = '';
    const tickerName = getTicker(a);
    const dataHoraFormatada = formatDate(a.created_at); // <-- USA A FUNÇÃO CORRIGIDA AQUI
    
    // Cores das Recomendações
    let recClass = "bg-slate-700 text-slate-300";
    if(a.recomendacao.includes('Compra')) recClass = "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20";
    if(a.recomendacao.includes('Venda')) recClass = "bg-red-500/10 text-red-400 border border-red-500/20";

    if(type === 'rascunho') {
        btns = `<button onclick="acao('${a.id}','aprovar')" class="flex-1 bg-blue-600 hover:bg-blue-500 text-white text-sm font-bold py-2 rounded transition-colors">Aprovar</button>
                <button onclick="acao('${a.id}','lixeira')" class="px-3 py-2 bg-slate-700 hover:bg-red-500/20 hover:text-red-400 text-slate-400 rounded transition-colors" title="Mover para Lixeira">🗑️</button>`;
    } else if (type === 'publicado') {
        btns = `<button onclick="acao('${a.id}','desaprovar')" class="w-full bg-slate-700 hover:bg-yellow-600/20 hover:text-yellow-400 text-slate-300 border border-slate-600 text-sm font-medium py-2 rounded transition-colors">↩ Reverter</button>`;
    } else { // Lixeira
        btns = `<button onclick="acao('${a.id}','restaurar')" class="flex-1 text-blue-400 hover:text-blue-300 font-medium text-sm border border-blue-900/50 rounded py-1">Restaurar</button>
                <button onclick="acao('${a.id}','permanente')" class="flex-1 text-red-500 hover:text-red-400 font-medium text-sm border border-red-900/50 rounded py-1 ml-2">Excluir</button>`;
    }

    return `<div class="bg-slate-800 p-5 rounded-xl border border-slate-700 shadow-sm hover:border-slate-600 transition-all group relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full ${type === 'rascunho' ? 'bg-yellow-500' : (type === 'publicado' ? 'bg-green-500' : 'bg-red-500')}"></div>
        <div class="flex justify-between items-start mb-3 pl-2">
            <span class="text-xs font-bold text-white bg-slate-700 px-2 py-1 rounded uppercase tracking-wider">${tickerName}</span>
            <span class="text-[10px] text-slate-500">${dataHoraFormatada}</span> 
        </div>
        <div class="pl-2 mb-4">
            <h4 class="text-white font-semibold leading-snug mb-2 group-hover:text-blue-400 transition-colors">${a.titulo}</h4>
            <span class="inline-block text-[10px] uppercase font-bold px-2 py-1 rounded ${recClass}">${a.recomendacao}</span>
        </div>
        <div class="flex gap-2 mt-auto pl-2 pt-3 border-t border-slate-700/50">${btns}</div>
    </div>`;
}

// Navegação de Abas
function showTab(tabName) {
    document.getElementById('tab-painel').classList.add('hidden');
    document.getElementById('tab-lixeira').classList.add('hidden');
    document.getElementById(`tab-${tabName}`).classList.remove('hidden');
    document.getElementById('page-title').textContent = tabName === 'lixeira' ? 'Lixeira' : 'Visão Geral';
    if(tabName === 'lixeira') loadLixeira(); else loadAll();
}

// Carga de Dados
async function loadAll() {
    document.getElementById('global-loader').classList.remove('hidden');
    const rasc = await api(`${API}/artigos`);
    const pub = await api(`${API}/artigos/publicados`);
    document.getElementById('global-loader').classList.add('hidden');

    if(rasc && rasc.data) {
        document.getElementById('list-rascunhos').innerHTML = rasc.data.map(a => renderCard(a, 'rascunho')).join('') || '<p class="text-slate-500 italic text-sm">Sem rascunhos.</p>';
        document.getElementById('count-rascunhos').textContent = rasc.data.length;
    }
    if(pub && pub.data) {
        document.getElementById('list-publicados').innerHTML = pub.data.map(a => renderCard(a, 'publicado')).join('') || '<p class="text-slate-500 italic text-sm">Nada publicado.</p>';
        document.getElementById('count-publicados').textContent = pub.data.length;
    }
}

async function loadLixeira() {
    document.getElementById('global-loader').classList.remove('hidden');
    const lix = await api(`${API}/artigos/lixeira`);
    document.getElementById('global-loader').classList.add('hidden');
    if(lix && lix.data) {
        document.getElementById('list-lixeira').innerHTML = lix.data.map(a => renderCard(a, 'lixeira')).join('') || '<p class="text-slate-500 italic col-span-full text-center py-10">Lixeira vazia.</p>';
    }
}

// Ações (Backend)
async function acao(id, tipo) {
    if(tipo === 'permanente' && !confirm('Isso apaga do banco de dados para sempre. Continuar?')) return;
    let endpoint = '';
    let method = 'POST';

    if(tipo === 'aprovar') endpoint = `${API}/artigos/${id}/aprovar`;
    if(tipo === 'desaprovar') endpoint = `${API}/artigos/${id}/desaprovar`;
    if(tipo === 'lixeira') endpoint = `${API}/artigos/${id}/lixeira`;
    if(tipo === 'restaurar') endpoint = `${API}/artigos/${id}/restaurar`;
    if(tipo === 'permanente') { endpoint = `${API}/artigos/${id}/permanente`; method = 'DELETE'; }

    await api(endpoint, method);
    if(document.getElementById('tab-lixeira').classList.contains('hidden')) loadAll(); else loadLixeira();
}

// Modal
function abrirModalGerar() { document.getElementById('modal-gerar').classList.remove('hidden'); }
function fecharModal() { document.getElementById('modal-gerar').classList.add('hidden'); }
function toggleSelect(enable) {
    const sel = document.getElementById('select-ticker');
    sel.disabled = !enable;
    if(enable) sel.focus();
}

// Disparo IA
async function dispararIA() {
    const scope = document.querySelector('input[name="scope"]:checked').value;
    let payload = { tickers: 'all' };
    let msg = "Iniciando análise da carteira completa...";

    if (scope === 'single') {
        const ticker = document.getElementById('select-ticker').value;
        payload = { tickers: [ticker] };
        msg = `Iniciando análise para ${ticker}...`;
    }

    fecharModal();
    alert(`🤖 ${msg}\n\nAguarde alguns instantes e clique em ATUALIZAR.`);
    try {
        await api(`${API}/ia/gerar`, 'POST', payload);
        setTimeout(loadAll, 5000);
    } catch(e) { alert("Erro ao contatar agentes."); }
}

// Início
loadAll();