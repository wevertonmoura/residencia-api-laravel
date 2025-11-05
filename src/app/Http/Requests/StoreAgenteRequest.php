<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreAgenteRequest extends FormRequest
{
    /**
     * Determine se o usuário esta autorizado para fazer esta requisição.
     */
    public function authorize(): bool
    {
        // Altera para true para permitir a requisição na API
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
            'nome' => 'required|string|max:100',
            // Correção: 'unique' e 'max' separados por |
            'email' => 'required|email|unique:agentes,email|max:150',
            'telefone' => 'nullable|string|max:20',
            // Correção: 'nullable' e 'string' separados por |
            'status' => 'nullable|string|in:ativo,inativo,ferias',
        ];
    }
}
