<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Artigo extends Model
{
    use HasFactory;

    protected $table = 'artigos';

    // Lista de campos que podem ser gravados no banco
    protected $fillable = [
        'ticker',
        'titulo',
        'conteudo',
        'recomendacao',
        'status'
    ];
}