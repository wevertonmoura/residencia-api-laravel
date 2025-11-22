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
        Schema::create('artigos', function (Blueprint $table) {
            $table->id();
            $table->string('titulo', 255); 
            $table->text('conteudo'); 
            
            // --- MUDANÇA AQUI ---
            // Mudamos de 'acao_ticker' para 'ticker' para padronizar com o Python e o Model
            $table->string('ticker', 20); 
            // --------------------

            $table->string('recomendacao', 50); 
            
            // Coluna do Fator Humano
            $table->string('status', 50)->default('rascunho'); 
            
            $table->timestamps(); 
        });
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