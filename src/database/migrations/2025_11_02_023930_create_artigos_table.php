<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateArtigosTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        // Verifica se a tabela já existe para evitar erro
        if (!Schema::hasTable('artigos')) {
            Schema::create('artigos', function (Blueprint $table) {
                $table->id();
                
                // Dados Principais
                $table->string('ticker', 10); // Ex: PETR4.SA
                $table->string('titulo');
                $table->text('conteudo'); // Texto longo para a matéria
                
                // Metadados
                $table->string('recomendacao', 20); // Compra, Venda, Neutro
                
                // Controle de Estado (Sênior: Usamos ENUM para garantir integridade)
                // draft = Rascunho, published = Publicado, trash = Lixeira
                $table->enum('status', ['draft', 'published', 'trash'])->default('draft');
                
                $table->timestamps(); // created_at e updated_at
            });
        }
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('artigos');
    }
}