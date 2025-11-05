<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Artigo extends Model
{
    use HasFactory;

    /**
     * Os atributos que são preenchíveis em massa (mass assignable).
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'titulo',
        'conteudo',
        'acao_ticker',
        'recomendacao',
        'status',
    ];
}