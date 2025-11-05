<?php

use App\Http\Controllers\AgenteController; // Importa o Controller do Agente
use App\Http\Controllers\ArtigoController; // Importa o Controller do Artigo
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Tokencontroller;
use App\Http\Controllers\AgendaController;

/*
|--------------------------------------------------------------------------
| Rotas de API
|--------------------------------------------------------------------------
| Rotas que já existiam no seu projeto.
*/

Route::get('/agenda', [AgendaController::class, 'index']);
Route::post('/agenda', [AgendaController::class, 'criar']);
Route::get('/agenda/{id}', [AgendaController::class, 'visualizar']);
Route::put('/agenda/{id}', [AgendaController::class, 'atualizar']);
Route::delete('/agenda/{id}', [AgendaController::class, 'deletar']);

Route::post('/user', [TokenController::class, 'index']);

Route::group(['middleware' => ['JWTToken']], function () {
    // Rotas protegidas
});

/*
|--------------------------------------------------------------------------
| Rota Padrão de API (Sanctum)
|--------------------------------------------------------------------------
*/
Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

/*
|--------------------------------------------------------------------------
| Rota de Teste
|--------------------------------------------------------------------------
*/
Route::get('/teste', function () {
    return response()->json([
        'status' => 'sucesso',
        'mensagem' => 'A API está funcionando!'
    ]);
});

/*
|--------------------------------------------------------------------------
| Rota dos Agentes (Do PDF)
|--------------------------------------------------------------------------
*/
Route::apiResource('agentes', AgenteController::class);

/*
|--------------------------------------------------------------------------
| Rota dos Artigos (PAINEL IA v2)
|--------------------------------------------------------------------------
*/

// O apiResource já cria:
// GET /artigos (para index - Rascunhos)
// DELETE /artigos/{id} (para destroy - Excluir)
// ...e outras que não estamos usando (store, update, show)
Route::apiResource('artigos', ArtigoController::class);

// --- Rotas Personalizadas para o Painel v2 ---

// Rota NOVA para listar os artigos PUBLICADOS
// (Aponta para o método 'indexPublicados' no seu Controller)
Route::get('/artigos/publicados', [ArtigoController::class, 'indexPublicados']);

// Rota NOVA para APROVAR um artigo
// (Aponta para o método 'aprovar' no seu Controller)
Route::post('/artigos/{id}/aprovar', [ArtigoController::class, 'aprovar']);

// Rota NOVA para DESAPROVAR um artigo
// (Aponta para o método 'desaprovar' no seu Controller)
Route::post('/artigos/{id}/desaprovar', [ArtigoController::class, 'desaprovar']);