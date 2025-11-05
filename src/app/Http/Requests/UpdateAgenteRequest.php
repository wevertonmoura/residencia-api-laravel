<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule; // Importa a classe Rule

class UpdateAgenteRequest extends FormRequest
{
    /**
     * Determine se o usuário está autorizado a fazer esta solicitação.
     */
    public function authorize(): bool
    {
        // Deve ser true para permitir a atualização
        return true;
    }

    /**
     * Obtenha as regras de validação que se aplicam à solicitação.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array|string>
     */
    public function rules(): array
    {
        // Pega o ID do agente da rota (ex: /api/agentes/11)
        $agenteId = $this->route('agente')->id ?? null;

        return [
            'nome' => 'sometimes|required|string|max:100',
            'email' => [
                'sometimes',
                'required',
                'email',
                'max:150',
                // Regra crucial: Ignora o ID do próprio agente ao verificar se o email é único
                Rule::unique('agentes', 'email')->ignore($agenteId),
            ],
            'telefone' => 'nullable|string|max:20',
            'status' => 'nullable|string|in:ativo,inativo,ferias',
        ];
    }
}

