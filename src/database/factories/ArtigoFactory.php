<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Artigo>
 */
class ArtigoFactory extends Factory
{
    /**
     * Define o estado padrão do modelo.
     *
     * @return array<string, mixed>
     */
    public function definition()
    {
        // Estes métodos (sentence, paragraphs) vão automaticamente
        // usar o idioma 'faker_locale' ('pt_BR') que definimos no config/app.php
        
        return [
            // Gera um título em Português (ex: "O rápido cão castanho.")
            'titulo' => $this->faker->sentence(6), 
            
            // Gera 3 parágrafos de texto em Português
            'conteudo' => $this->faker->paragraphs(3, true), // O 'true' retorna como string única
            
            // Dados aleatórios para o resto
            'acao_ticker' => $this->faker->randomElement(['ITUB4.SA', 'VALE3.SA', 'MGLU3.SA', 'PETR4.SA']),
            'recomendacao' => $this->faker->randomElement(['Comprar', 'Vender', 'Manter']),
            
            // Define o status padrão
            'status' => 'rascunho',
        ];
    }
}