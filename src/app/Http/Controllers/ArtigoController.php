<?php

namespace App\Http\Controllers;

use App\Models\Artigo;
use App\Http\Resources\ArtigoResource;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Http;
use Illuminate\Routing\Controller;

class ArtigoController extends Controller
{
    /**
     * Exibir uma listagem do recurso (Lista de RASCUNHOS).
     */
    public function index(): JsonResponse
    {
        $artigos = Artigo::where('status', 'draft')
                         ->orderBy('created_at', 'desc')
                         ->get();
                         
        return ArtigoResource::collection($artigos)->response();
    }

    /**
     * Retorna artigos com status 'draft' (Rascunho) ou 'pending' (Pendente).
     * Endpoint para a coluna 'Pendentes de Aprovação'.
     */
    public function pendentes(): JsonResponse
    {
        $artigos = Artigo::where('status', 'draft')
                         ->orWhere('status', 'pending')
                         ->orderBy('updated_at', 'desc')
                         ->get();
        
        return ArtigoResource::collection($artigos)->response();
    }

    /**
     * Onde o Python entrega o artigo.
     */
    public function store(Request $request): JsonResponse
    {
        Log::info('🤖 API (store) recebeu requisição do Python:', $request->all());

        try {
            $artigo = Artigo::create([
                'titulo'       => $request->titulo,
                'conteudo'     => $request->conteudo,
                'recomendacao' => $request->recomendacao,
                'ticker'       => $request->ticker ?? $request->acao_ticker, 
                'status'       => 'draft', // Padronizado para 'draft'
                // REMOVIDO: 'motivo_revisao'
            ]);

            Log::info('✅ Artigo salvo com sucesso! ID: ' . $artigo->id);
            return (new ArtigoResource($artigo))->response()->setStatusCode(201);

        } catch (\Exception $e) {
            Log::error('❌ Erro ao salvar artigo no Banco: ' . $e->getMessage());
            return response()->json(['error' => 'Falha ao salvar: ' . $e->getMessage()], 500);
        }
    }

    // --- MÉTODOS DE PUBLICAÇÃO ---

    public function indexPublicados(): JsonResponse
    {
        $artigos = Artigo::where('status', 'published')
                         ->orderBy('updated_at', 'desc')
                         ->get();
        return ArtigoResource::collection($artigos)->response();
    }

    /**
     * Aprovar/Publicar o Artigo.
     * REMOVIDO: A lógica para limpar 'motivo_revisao'.
     */
    public function aprovar(Request $request, $id): JsonResponse
    {
        $artigo = Artigo::find($id);
        if (!$artigo) return response()->json(['message' => 'Não encontrado'], 404);

        $artigo->status = 'published';
        // $artigo->motivo_revisao = null; // REMOVIDO
        $artigo->save();
        return (new ArtigoResource($artigo))->response();
    }

    /**
     * Desaprovar/Despublicar o Artigo.
     * REMOVIDO: A lógica para capturar e salvar 'motivo_revisao'.
     */
    public function desaprovar(Request $request, $id): JsonResponse
    {
        $artigo = Artigo::find($id);
        if (!$artigo) return response()->json(['message' => 'Não encontrado'], 404);

        $artigo->status = 'draft'; // Volta para Rascunho/Pendente
        
        // CÓDIGO REMOVIDO: Lógica de captura e salvamento de 'motivo_revisao'
        
        $artigo->save();
        return (new ArtigoResource($artigo))->response();
    }

    // --- MÉTODOS DE LIXEIRA & GESTÃO ---

    public function indexLixeira(): JsonResponse
    {
        $artigos = Artigo::where('status', 'trash')
                         ->orderBy('updated_at', 'desc')
                         ->get();
        return ArtigoResource::collection($artigos)->response();
    }

    public function moverParaLixeira($id): JsonResponse
    {
        $artigo = Artigo::find($id);
        if (!$artigo) return response()->json(['message' => 'Não encontrado'], 404);
        
        $artigo->status = 'trash'; // Padronizado
        $artigo->save();
        return response()->json(['message' => 'Movido para lixeira']);
    }

    /**
     * Restaurar o Artigo.
     * REMOVIDO: A lógica para limpar 'motivo_revisao'.
     */
    public function restaurar($id): JsonResponse
    {
        $artigo = Artigo::find($id);
        if (!$artigo) return response()->json(['message' => 'Não encontrado'], 404);

        $artigo->status = 'draft'; // Volta para rascunho
        // $artigo->motivo_revisao = null; // REMOVIDO
        $artigo->save();
        return response()->json(['message' => 'Restaurado com sucesso']);
    }
    
    public function excluirPermanente($id): JsonResponse
    {
        $artigo = Artigo::find($id);
        if ($artigo) {
            $artigo->delete();
        }
        return response()->json(null, 204);
    }

    // --- PROXY PARA O PYTHON (MANTIDO) ---
    public function dispararIA(Request $request): JsonResponse
    {
        $payload = $request->all();

        try {
            $urlPython = 'http://host.docker.internal:5000/gerar'; 
            
            $response = Http::timeout(60)->post($urlPython, $payload);
            
            return response()->json([
                'message' => 'Solicitação enviada aos agentes!',
                'python_response' => $response->json()
            ]);
        } catch (\Exception $e) {
            Log::error('Erro ao chamar Python Flask: ' . $e->getMessage());
            return response()->json(['error' => 'Erro de comunicação com os Agentes.'], 500);
        }
    }
}