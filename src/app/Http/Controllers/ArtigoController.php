<?php

namespace App\Http\Controllers;

use App\Models\Artigo;
use App\Http\Resources\ArtigoResource;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Http; // <--- NOVO: Necessário para chamar o Python

class ArtigoController extends Controller
{
    /**
     * Exibir uma listagem do recurso (Lista de RASCUNHOS).
     */
    public function index(): JsonResponse
    {
        $artigos = Artigo::where('status', 'rascunho')
                         ->orderBy('created_at', 'desc')
                         ->get();
                         
        return ArtigoResource::collection($artigos)->response();
    }

    /**
     * MÉTODO CRUCIAL: Onde o Python entrega o artigo.
     */
    public function store(Request $request): JsonResponse
    {
        Log::info('🤖 API (store) recebeu requisição do Python:', $request->all());

        try {
            $artigo = Artigo::create([
                'titulo'       => $request->titulo,
                'conteudo'     => $request->conteudo,
                'recomendacao' => $request->recomendacao,
                // Garante compatibilidade de nomes
                'ticker'       => $request->ticker ?? $request->acao_ticker, 
                'status'       => 'rascunho'
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
        $artigos = Artigo::where('status', 'publicado')
                         ->orderBy('updated_at', 'desc')
                         ->get();
        return ArtigoResource::collection($artigos)->response();
    }

    public function aprovar(Request $request, $id): JsonResponse
    {
        $artigo = Artigo::find($id);
        if (!$artigo) return response()->json(['message' => 'Não encontrado'], 404);

        $artigo->status = 'publicado';
        $artigo->save();
        return (new ArtigoResource($artigo))->response();
    }

    public function desaprovar(Request $request, $id): JsonResponse
    {
        $artigo = Artigo::find($id);
        if (!$artigo) return response()->json(['message' => 'Não encontrado'], 404);

        $artigo->status = 'rascunho';
        $artigo->save();
        return (new ArtigoResource($artigo))->response();
    }

    // --- NOVOS MÉTODOS: LIXEIRA & GESTÃO ---

    /**
     * Lista itens que foram descartados
     */
    public function indexLixeira(): JsonResponse
    {
        $artigos = Artigo::where('status', 'lixeira')
                         ->orderBy('updated_at', 'desc')
                         ->get();
        return ArtigoResource::collection($artigos)->response();
    }

    /**
     * Soft Delete: Move para a lixeira em vez de apagar
     */
    public function moverParaLixeira($id): JsonResponse
    {
        $artigo = Artigo::find($id);
        if (!$artigo) return response()->json(['message' => 'Não encontrado'], 404);
        
        $artigo->status = 'lixeira';
        $artigo->save();
        return response()->json(['message' => 'Movido para lixeira']);
    }

    /**
     * Restaura da lixeira para rascunho
     */
    public function restaurar($id): JsonResponse
    {
        $artigo = Artigo::find($id);
        if (!$artigo) return response()->json(['message' => 'Não encontrado'], 404);

        $artigo->status = 'rascunho';
        $artigo->save();
        return response()->json(['message' => 'Restaurado com sucesso']);
    }
    
    /**
     * Hard Delete: Apaga do banco de dados para sempre
     */
    public function excluirPermanente($id): JsonResponse
    {
        $artigo = Artigo::find($id);
        if ($artigo) {
            $artigo->delete();
        }
        return response()->json(null, 204);
    }

    // --- NOVO MÉTODO: GATILHO DA IA (CHAMA O FLASK) ---

    public function dispararIA(Request $request): JsonResponse
    {
        // Recebe { tickers: ['PETR4.SA'] } ou { tickers: 'all' } do Front-end
        $payload = $request->all();

        try {
            // Chama o container Python na porta 5000
            // 'invasores_agentes' é o nome do serviço no docker-compose
      
            $response = Http::post('http://172.18.0.4:5000/gerar', $payload);
            
            return response()->json([
                'message' => 'Solicitação enviada aos agentes!',
                'python_response' => $response->json()
            ]);
        } catch (\Exception $e) {
            Log::error('Erro ao chamar Python Flask: ' . $e->getMessage());
            return response()->json(['error' => 'Erro de comunicação com os Agentes. Verifique se o container Python está rodando.'], 500);
        }
    }

    // --- MÉTODOS PADRÃO ---

    public function show(Artigo $artigo): JsonResponse
    {
        return (new ArtigoResource($artigo))->response();
    }

    public function update(Request $request, Artigo $artigo): JsonResponse
    {
        $artigo->update($request->all());
        return (new ArtigoResource($artigo))->response();
    }
    
    // Mantemos o destroy padrão caso alguma rota antiga use
    public function destroy(Artigo $artigo): JsonResponse
    {
        $artigo->delete();
        return response()->json(null, 204);
    }
}