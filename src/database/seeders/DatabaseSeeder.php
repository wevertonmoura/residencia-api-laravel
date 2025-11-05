<?php

namespace Database\Seeders;

use App\Models\Agente; // <-- Esta linha já deve existir
use App\Models\Artigo; // <-- 1. ADICIONE ESTA LINHA

use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        // Cria 10 Agentes usando a Factory (esta linha já deve existir)
        Agente::factory()->count(10)->create();
        
        // Cria 10 Artigos usando a Factory
        Artigo::factory()->count(10)->create(); // <-- 2. ADICIONE ESTA LINHA
    }
}