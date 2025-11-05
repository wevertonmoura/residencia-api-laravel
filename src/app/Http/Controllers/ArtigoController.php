<?php

namespace App\Http\Controllers;

// 1. Importa tudo que precisamos
use App\Models\Artigo;
use App\Http\Resources\ArtigoResource;
use App\Http\Requests\StoreArtigoRequest;
use App\Http\Requests\UpdateArtigoRequest;
use Illuminate\Http\JsonResponse;

class ArtigoController extends Controller
{
    /**
     * Exibir uma listagem do recurso (Listar todos os Artigos).
     *
     * **** ALTERAÇÃO FEITA AQUI: ****
     * Trocamos 'paginate(10)' por 'all()' para enviar TODOS os artigos
     * de uma vez para o painel de revisão (corrigindo o bug do rascunho).
     */
    public function index(): JsonResponse
    {
        $artigos = Artigo::all(); // <--- MUDANÇA AQUI
        
        // Usamos 'collection' para formatar a lista
        return ArtigoResource::collection($artigos)->response();
    }

    /**
     * Armazene um recurso recém-criado (Salvar um novo Artigo).
     */
    public function store(StoreArtigoRequest $request): JsonResponse
    {
        $artigo = Artigo::create($request->validated());
        return (new ArtigoResource($artigo))
            ->response()
            ->setStatusCode(201);
    }

    /**
     * Exibir o recurso especificado (Ver um Artigo).
     */
    public function show(Artigo $artigo): JsonResponse
    {
        return (new ArtigoResource($artigo))->response();
    }

    /**
     * Atualizar o recurso especificado (Atualizar um Artigo).
     */
    public function update(UpdateArtigoRequest $request, Artigo $artigo): JsonResponse
    {
        $artigo->update($request->validated());
        return (new ArtigoResource($artigo))->response();
    }

    /**
     * Remover o recurso especificado (Deletar um Artigo).
     */
    public function destroy(Artigo $artigo): JsonResponse
    {
        $artigo->delete();
        return response()->json(null, 204);
    }
}