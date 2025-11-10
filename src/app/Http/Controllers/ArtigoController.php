<?php

namespace App\Http\Controllers;

use App\Models\Artigo; 
use App\Http\Resources\ArtigoResource;
use App\Http\Requests\StoreArtigoRequest;
use App\Http\Requests\UpdateArtigoRequest;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request; // Não se esqueça de importar Request!

class ArtigoController extends Controller
{
    /**
     * Exibir uma listagem do recurso (Lista de RASCUNHOS).
     */
    public function index(): JsonResponse
    {
        // Filtra pelo status 'rascunho'
        $artigos = Artigo::where('status', 'rascunho')->get(); 
        return ArtigoResource::collection($artigos)->response();
    }

    // --- MÉTODOS NOVOS PARA O PAINEL V2 ---

    /**
     * MÉTODO NOVO: Listar artigos publicados.
     */
    public function indexPublicados(): JsonResponse
    {
        // Filtra pelo status 'publicado'
        $artigos = Artigo::where('status', 'publicado')->get(); 
        return ArtigoResource::collection($artigos)->response();
    }

    /**
     * MÉTODO NOVO: Aprovar um artigo (muda status para 'publicado').
     */
    public function aprovar(Request $request, $id): JsonResponse
    {
        $artigo = Artigo::find($id);
        if (!$artigo) {
            return response()->json(['message' => 'Artigo não encontrado'], 404);
        }

        $artigo->status = 'publicado';
        $artigo->save();
        return (new ArtigoResource($artigo))->response();
    }

    /**
     * MÉTODO NOVO: Desaprovar um artigo (muda status para 'rascunho').
     */
    public function desaprovar(Request $request, $id): JsonResponse
    {
        $artigo = Artigo::find($id);
        if (!$artigo) {
            return response()->json(['message' => 'Artigo não encontrado'], 404);
        }

        $artigo->status = 'rascunho';
        $artigo->save();
        return (new ArtigoResource($artigo))->response();
    }

    // --- MÉTODOS PADRÃO (Ajustados para o Painel) ---

    public function destroy(Artigo $artigo): JsonResponse
    {
        // O método destroy já é chamado pelo Route::apiResource
        $artigo->delete();
        return response()->json(null, 204);
    }
    
    // Deixamos os métodos show, store, update aqui se você precisar deles...
    public function show(Artigo $artigo): JsonResponse
    {
        return (new ArtigoResource($artigo))->response();
    }
    public function store(StoreArtigoRequest $request): JsonResponse
    {
        $artigo = Artigo::create($request->validated());
        return (new ArtigoResource($artigo))->response()->setStatusCode(201);
    }
    public function update(UpdateArtigoRequest $request, Artigo $artigo): JsonResponse
    {
        $artigo->update($request->validated());
        return (new ArtigoResource($artigo))->response();
    }
}