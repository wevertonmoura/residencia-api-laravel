<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class ArtigoResource extends JsonResource
{
    public function toArray($request): array
    {
        $tickerName = $this->ticker ?? $this->acao_ticker;
        
        return [
            'id' => $this->id,
            'titulo' => $this->titulo,
            'conteudo' => $this->conteudo,
            'recomendacao' => $this->recomendacao,
            'status' => $this->status,
            'ticker' => $tickerName,
            
            // --- CORREÇÃO DO FUSO HORÁRIO (ADICIONANDO O 'Z' - UTC) ---
            'created_at' => $this->created_at ? $this->created_at->format('Y-m-d H:i:s') . 'Z' : null,
            'updated_at' => $this->updated_at ? $this->updated_at->format('Y-m-d H:i:s') . 'Z' : null,
            // ---------------------------------------------------------
        ];
    }
}