<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ArtigoController;
use App\Http\Controllers\AgenteController;
use App\Http\Controllers\AgendaController;
use App\Http\Controllers\TokenController;

/*
|--------------------------------------------------------------------------
| ROTAS LEGADAS (Agenda/User)
|--------------------------------------------------------------------------
*/
Route::get('/agenda', [AgendaController::class, 'index']);
Route::post('/agenda', [AgendaController::class, 'criar']);
Route::get('/agenda/{id}', [AgendaController::class, 'visualizar']);
Route::put('/agenda/{id}', [AgendaController::class, 'atualizar']);
Route::delete('/agenda/{id}', [AgendaController::class, 'deletar']);
Route::post('/user', [TokenController::class, 'index']);

// ROTAS ANTIGAS
Route::apiResource('agentes', AgenteController::class);

/*
|--------------------------------------------------------------------------
| ROTAS DO PAINEL IA (AlphaNews)
|--------------------------------------------------------------------------
*/

// 1. ROTA CRÍTICA: Recebimento do Python
// O arquivo .env do Python procura exatamente '/api/receber-artigo'
Route::post('/receber-artigo', [ArtigoController::class, 'store']);

// 2. GATILHO DA IA (Painel -> Laravel -> Python)
Route::post('/ia/gerar', [ArtigoController::class, 'dispararIA']);

// 3. ROTAS DA LIXEIRA
Route::get('/artigos/lixeira', [ArtigoController::class, 'indexLixeira']);
Route::post('/artigos/{id}/lixeira', [ArtigoController::class, 'moverParaLixeira']);
Route::post('/artigos/{id}/restaurar', [ArtigoController::class, 'restaurar']);
Route::delete('/artigos/{id}/permanente', [ArtigoController::class, 'excluirPermanente']);

// 4. ROTAS DE PUBLICAÇÃO E PENDENTES
Route::get('/artigos/publicados', [ArtigoController::class, 'indexPublicados']);
// ROTA ADICIONADA: Busca artigos que a IA criou (status 'draft' ou 'pending')
Route::get('/artigos/pendentes', [ArtigoController::class, 'pendentes']);
Route::post('/artigos/{id}/aprovar', [ArtigoController::class, 'aprovar']);
Route::post('/artigos/{id}/desaprovar', [ArtigoController::class, 'desaprovar']);

// 5. RECURSO PADRÃO (Index, Store, Show, Update, Destroy)
// Esta deve ser a última rota para não sobrescrever as rotas específicas acima!
Route::apiResource('artigos', ArtigoController::class);