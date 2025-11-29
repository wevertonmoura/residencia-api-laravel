<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\Str; // NECESSÁRIO para gerar o resumo

class ArtigoResource extends JsonResource
{
    /**
     * Transforma o recurso em um array.
     *
     * @param \Illuminate\Http\Request $request
     * @return array<string, mixed>
     */
    public function toArray($request): array
    {
        // Garante que pegamos o ticker independente do nome da coluna no banco
        $tickerName = $this->ticker ?? $this->acao_ticker;
        
        // --- Geração do Resumo (Melhoria UX Sênior) ---
        // Pega as primeiras 150 caracteres do conteúdo (removendo tags HTML)
        $summary = $this->conteudo ? Str::limit(strip_tags($this->conteudo), 150, '...') : 'Conteúdo indisponível.';
        
        // Mantemos o campo 'motivo_revisao' como null para evitar que o frontend quebre
        // se ele for referenciado em qualquer código JavaScript antigo (boa prática defensiva).
        $motivoRevisao = $this->motivo_revisao ?? null;
        
        return [
            'id' => $this->id,
            'titulo' => $this->titulo,
            // Mantemos 'conteudo' completo para o modal "Veja Mais"
            'conteudo' => $this->conteudo, 
            
            // NOVO: Resumo para exibição compacta no dashboard
            'resumo' => $summary, 
            
            'recomendacao' => $this->recomendacao,
            'status' => $this->status,
            'ticker' => $tickerName,
            
            // Compatibilidade de fluxo de trabalho (sem quebrar o JS se o campo for lido)
            'motivo_revisao' => $motivoRevisao, 
            
            // --- CORREÇÃO DO FUSO HORÁRIO (ISO 8601) ---
            // Usamos toIso8601String() para ser mais robusto no JavaScript.
            'created_at' => $this->created_at ? $this->created_at->toIso8601String() : null,
            'updated_at' => $this->updated_at ? $this->updated_at->toIso8601String() : null,
        ];
    }
}