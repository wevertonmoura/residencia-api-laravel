<?php

namespace App\Http\Resources;

use Illuminate\Http\Request; // <-- ADICIONE ESTA LINHA
use Illuminate\Http\Resources\Json\JsonResource;

class ArtigoResource extends JsonResource
{
    /**
     * Transforme o recurso em uma matriz.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array|\Illuminate\Contracts\Support\Arrayable|\JsonSerializable
     */
    public function toArray($request): array // <-- REMOVA O 'Request' DAQUI
    {
        return [
            'id' => $this->id,
            'titulo' => $this->titulo,
            'conteudo' => $this->conteudo,
            'acao_ticker' => $this->acao_ticker,
            'recomendacao' => $this->recomendacao,
            'status' => $this->status,
            'criado_em' => $this->created_at->format('Y-m-d H:i:s'),
            'atualizado_em' => $this->updated_at->format('Y-m-d H:i:s'),
        ];
    }
}