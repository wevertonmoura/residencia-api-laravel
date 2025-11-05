<?php

namespace App\Http\Controllers;

use App\Models\Agente;
use App\Http\Resources\AgenteResource; // Importa o Resource
use App\Http\Requests\StoreAgenteRequest; // Importa o Request de criação
use App\Http\Requests\UpdateAgenteRequest; // Importa o Request de atualização
use Illuminate\Http\JsonResponse;

class AgenteController extends Controller
{
    /**
     * Exibir uma listagem do recurso.
     */
    public function index(): JsonResponse
    {
        $agentes = Agente::paginate(10);
        return AgenteResource::collection($agentes)->response();
    }

    /**
     * Armazene um recurso recém-criado no armazenamento.
     */
    public function store(StoreAgenteRequest $request): JsonResponse
    {
        $agente = Agente::create($request->validated());
        return (new AgenteResource($agente))
            ->response()
            ->setStatusCode(201);
    }

    /**
     * Exibir o recurso especificado.
     */
    public function show(Agente $agente): JsonResponse
    {
        return (new AgenteResource($agente))->response();
    }

    /**
     * Atualizar o recurso especificado no armazenamento.
     */
    public function update(UpdateAgenteRequest $request, Agente $agente): JsonResponse
    {
        $agente->update($request->validated());
        return (new AgenteResource($agente))->response();
    }

    /**
     * Remover o recurso especificado do armazenamento.
     */
    public function destroy(Agente $agente): JsonResponse
    {
        $agente->delete();
        return response()->json(null, 204);
    }
}
