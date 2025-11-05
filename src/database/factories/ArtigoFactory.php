<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

class ArtigoFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array
     */
    public function definition()
    {
        return [
            'titulo' => $this->faker->sentence(6), // Gera um título com 6 palavras
            'conteudo' => $this->faker->paragraphs(3, true), // Gera 3 parágrafos de texto
            'acao_ticker' => $this->faker->randomElement(['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'MGLU3.SA']),
            'recomendacao' => $this->faker->randomElement(['Comprar', 'Vender', 'Manter']),
            'status' => 'rascunho',
        ];
    }
}
