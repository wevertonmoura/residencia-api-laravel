<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UpdateArtigoRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     *
     * @return bool
     */
    /**
     * Determine se o usuário esta autorizado para fazer esta requisição.
     */
    public function authorize(): bool
    {
        // Altere para true para permitir a requisição na API
        return true;
    }

    /**
     * Obtenha as regras de validação que se aplicam à solicitação (request).
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array|string>
     */
    public function rules(): array
    {
        return [
            // 'sometimes' significa que o campo só é validado se estiver presente
            'titulo' => 'sometimes|required|string|max:255',
            'conteudo' => 'sometimes|required|string',
            'acao_ticker' => 'sometimes|required|string|max:20',
            'recomendacao' => 'sometimes|required|string|max:50',
            'status' => 'sometimes|string|in:rascunho,aprovado,rejeitado',
        ];
    }
    }

