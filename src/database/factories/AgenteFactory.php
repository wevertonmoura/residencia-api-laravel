<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

class AgenteFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array
     */
    public function definition()
    {
      return [
            'nome' => $this->faker->name,
            'email' => $this->faker->unique()->safeEmail,
            'telefone' => $this->faker->phoneNumber,
            'status' => $this->faker->randomElement(['ativo', 'inativo', 'ferias']),
        ];
    }
}
