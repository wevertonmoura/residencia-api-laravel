
<?php

use App\Http\Controllers\ArtigoController;
use App\Http\Controllers\AgenteController;
use App\Http\Controllers\AgendaController;
use App\Http\Controllers\TokenController;
use Illuminate\Support\Facades\Route;

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
| ROTAS DO PAINEL IA (v3) - NOVAS
|--------------------------------------------------------------------------
*/

// 1. GATILHO DA IA (Chama o Python Flask)
Route::post('/ia/gerar', [ArtigoController::class, 'dispararIA']);

// 2. ROTAS DA LIXEIRA
Route::get('/artigos/lixeira', [ArtigoController::class, 'indexLixeira']);
Route::post('/artigos/{id}/lixeira', [ArtigoController::class, 'moverParaLixeira']);
Route::post('/artigos/{id}/restaurar', [ArtigoController::class, 'restaurar']);
Route::delete('/artigos/{id}/permanente', [ArtigoController::class, 'excluirPermanente']);

// 3. ROTAS DE PUBLICAÇÃO (Aprovar/Desaprovar/Listar)
Route::get('/artigos/publicados', [ArtigoController::class, 'indexPublicados']);
Route::post('/artigos/{id}/aprovar', [ArtigoController::class, 'aprovar']);
Route::post('/artigos/{id}/desaprovar', [ArtigoController::class, 'desaprovar']);

// 4. RECURSO PADRÃO (Index, Store, Show, Update, Destroy)
Route::apiResource('artigos', ArtigoController::class);